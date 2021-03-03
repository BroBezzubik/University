#include <asm/io.h>
#include <linux/cdev.h> // for char device
#include <linux/device.h> // for creating device file
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/input.h> // for input device
#include <linux/interrupt.h>
#include <linux/ioport.h>
#include <linux/kdev_t.h> // for creating device file
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/slab.h> // for kmalloc, kfree
#include <linux/spinlock.h>
#include <linux/uaccess.h> // for user access

#include "my_vdev.h"

MODULE_DESCRIPTION(MODULE_NAME);
MODULE_AUTHOR("BroBezzubik");
MODULE_LICENSE("GPL");

static const struct file_operations vdev_fops = {
  .owner = THIS_MODULE,
  .open = vdev_open,
  .release = vdev_release,
  .write = vdev_write,
};

/*********************************** TASKLET ************************************/
static int is_key_pressed(u8 scancode)
{
  return !(scancode & SCANCODE_RELEASED_MASK);
}

static int scancode_to_ascii(u8 scancode)
{
  static char* row1 = "1234567890";
  static char* row2 = "qwertyuiop";
  static char* row3 = "asdfghjkl";
  static char* row4 = "zxcvbnm";

  scancode &= ~SCANCODE_RELEASED_MASK;
  if (scancode >= 0x02 && scancode <= 0x0b)
    return *(row1 + scancode - 0x02);
  if (scancode >= 0x10 && scancode <= 0x19)
    return *(row2 + scancode - 0x10);
  if (scancode >= 0x1e && scancode <= 0x26)
    return *(row3 + scancode - 0x1e);
  if (scancode >= 0x2c && scancode <= 0x32)
    return *(row4 + scancode - 0x2c);
  if (scancode == 0x39)
    return ' ';
  if (scancode == 0x1c)
    return '\n';
  return '?';
}

void mouse_tasklet_handler(unsigned long arg)
{
  struct vdev* data = (struct vdev*)arg;
  int pressed;

  pressed = is_key_pressed(data->buf[1]);

  if (pressed) {
    if (data->buf[0] == SCANCODE_LALT_MASK) {
      char ch = scancode_to_ascii(data->buf[1]);

      if (ch == data->map[0]) {
        input_report_rel(mouse_dev, REL_Y, -data->spd);
        input_sync(mouse_dev);
      } else if (ch == data->map[1]) {
        input_report_rel(mouse_dev, REL_Y, data->spd);
        input_sync(mouse_dev);
      } else if (ch == data->map[2]) {
        input_report_rel(mouse_dev, REL_X, -data->spd);
        input_sync(mouse_dev);
      } else if (ch == data->map[3]) {
        input_report_rel(mouse_dev, REL_X, data->spd);
        input_sync(mouse_dev);
      } else if (ch == data->map[4]) {
        input_report_key(mouse_dev, BTN_LEFT, 1);
        input_sync(mouse_dev);
      } else if (ch == data->map[5]) {
        input_report_key(mouse_dev, BTN_RIGHT, 1);
        input_sync(mouse_dev);
      }
    }
  } else {
    if (data->buf[0] == SCANCODE_LALT_MASK) {
      char ch = scancode_to_ascii(data->buf[1]);

      if (ch == data->map[4]) {
        input_report_key(mouse_dev, BTN_LEFT, 0);
        input_sync(mouse_dev);
      } else if (ch == data->map[5]) {
        input_report_key(mouse_dev, BTN_RIGHT, 0);
        input_sync(mouse_dev);
      }
    }
  }
}

// Interupt
static inline u8 i8042_read_data(void)
{
  u8 val;
  val = inb(I8042_DATA_REG);
  return val;
}

static void put_scancode(struct vdev* data, u8 scancode)
{
  char ch = 0;

  ch = scancode_to_ascii(scancode);

  if (data->buf[0] != SCANCODE_LALT_MASK
      || (ch == data->map[0] && ch == data->map[1]
          && ch == data->map[2] && ch == data->map[3])) {
    data->buf[0] = data->buf[1];
  }

  data->buf[1] = scancode;
  //pr_info("VDEV: [0]: 0x%x, [1]: 0x%x", data->buf[0], data->buf[1]);
}

irqreturn_t kbd_interrupt_handler(int irq_no, void* dev_id)
{
  u8 scancode = i8042_read_data();

  struct vdev* data = (struct vdev*)dev_id;

  spin_lock(&data->lock);
  put_scancode(data, scancode);
  spin_unlock(&data->lock);

  tasklet_schedule(mouse_tasklet);

  // Report the interrupt as not handled
  // so that the original driver can
  // process it
  return IRQ_NONE;
}

// Driver functions
static int vdev_open(struct inode* inode, struct file* file)
{
  struct vdev* data = container_of(inode->i_cdev, struct vdev, cdev);

  file->private_data = data;
  pr_info("VDEV: Device file opened\n");

  return 0;
}

static int vdev_release(struct inode* inode, struct file* file)
{
  pr_info("VDEV: Device file closed\n");
  return 0;
}

static ssize_t vdev_write(struct file* file, const char __user* user_buffer,
    size_t count, loff_t* offset)
{
  struct vdev* data = (struct vdev*)file->private_data;
  size_t size = BUF_SIZE < count ? BUF_SIZE : count;
  char* buf;
  char cmd;

  if ((buf = (char*)kmalloc(size, GFP_KERNEL)) == NULL) {
    pr_err("VDEV: kmalloc failed");
    return -EFAULT;
  }

  if (copy_from_user(buf, user_buffer, size)) {
    pr_err("VDEV: copy_from_user failed\n");
    kfree(buf);
    return -EFAULT;
  }

  // Get cmd from user
  memcpy(&cmd, buf, sizeof(char));
  cmd = cmd - '0';

  switch (cmd) {
  case CMD_MAP:
    memcpy(&data->map, buf + 2, 6);
    break;
  case CMD_SPD:
    kstrtol(buf + 2, 10, (long int*)&data->spd);
    break;
  default:
    pr_info("VDEV: User config malformed");
    break;
  }

  kfree(buf);
  return size;
}

static int __init vdev_init(void)
{
  int err;
  dev_t devnum;

  // Register char device
  if (VDEV_MAJOR) {
    devnum = MKDEV(VDEV_MAJOR, VDEV_MINOR);
    err = register_chrdev_region(devnum, VDEV_DEV_COUNT, MODULE_NAME);
  } else {
    err = alloc_chrdev_region(&devnum, VDEV_MINOR, VDEV_DEV_COUNT, MODULE_NAME);
  }

  if (err != 0) {
    pr_err("VDEV: register_region failed: %d\n", err);
    goto out;
  }

 // Request I/O ports
  if (request_region(I8042_DATA_REG + 1, 1, MODULE_NAME) == NULL) {
    err = -EBUSY;
    goto out_unregister;
  }
  if (request_region(I8042_STATUS_REG + 1, 1, MODULE_NAME) == NULL) {
    err = -EBUSY;
    goto out_unregister;
  }

  // Spinblock and def confing
  spin_lock_init(&devs[0].lock);
  devs[0].map[0] = 'w'; // UP
  devs[0].map[1] = 's'; // DOWN
  devs[0].map[2] = 'a'; // LEFT
  devs[0].map[3] = 'd'; // RIGHT
  devs[0].map[4] = 'j'; // BTNLEFT
  devs[0].map[5] = 'k'; // BTNRIGHT
  devs[0].spd = 10;

  // Register IRQ handler for kb
  err = request_irq(
      I8042_KBD_IRQ,          // IRQ line
      kbd_interrupt_handler,
      IRQF_SHARED,            // share interrupt line with other vdev driver (i8042)
      MODULE_NAME,            // use this to show dev in /proc/interrupts
      &devs[0]);              // for share interrupt, dev_id can't be NULL
  if (err != 0) {
    pr_err("VDEV: request_irq failed: %d\n", err);
    goto out_release_regions;
  }

  // Add char device to system
  cdev_init(&devs[0].cdev, &vdev_fops);
  err = cdev_add(&devs[0].cdev, devnum, VDEV_DEV_COUNT);
  if (err != 0) {
    pr_err("VDEV: cdev_add failed: %d\n", err);
    goto out_release_regions;
  }

  // Create struct class and device file
  if ((dev_class = class_create(THIS_MODULE, MODULE_NAME)) == NULL) {
    err = -1;
    pr_err("VDEV: class_create failed\n");
    goto out_cdev_del;
  }

  if ((device_create(dev_class, NULL, devnum, NULL, MODULE_NAME)) == NULL) {
    err = -1;
    pr_err("VDEV: device_create failed\n");
    goto out_class_destroy;
  }

  // allocate mouse device
  mouse_dev = input_allocate_device();
  if (mouse_dev == NULL) {
    err = -1;
    pr_err("VDEV: input_dev registered failed\n");
    goto out_device_destroy;
  }

  // Init mouse device
  mouse_dev->name = MODULE_NAME;
  mouse_dev->phys = MODULE_NAME;
  mouse_dev->id.bustype = BUS_VIRTUAL;
  mouse_dev->id.vendor = 0x0000;
  mouse_dev->id.product = 0x0000;
  mouse_dev->id.version = 0x0000;

  set_bit(EV_REL, mouse_dev->evbit);
  set_bit(REL_X, mouse_dev->relbit);
  set_bit(REL_Y, mouse_dev->relbit);
  set_bit(EV_KEY, mouse_dev->evbit);
  set_bit(BTN_LEFT, mouse_dev->keybit);
  set_bit(BTN_RIGHT, mouse_dev->keybit);

  // Register mouse device in system
  err = input_register_device(mouse_dev);
  if (err != 0) {
    pr_err("VDEV: input_register_device failed\n");
    goto out_input_free_device;
  }

  // Init tasklet mouse
  if ((mouse_tasklet = kmalloc(sizeof(struct tasklet_struct), GFP_KERNEL)) == NULL) {
    err = -1;
    pr_err("VDEV: kmalloc failed");
    goto out_input_unregister_device;
  }
  tasklet_init(mouse_tasklet, mouse_tasklet_handler, (unsigned long)&devs[0]);

  pr_notice("VDEV: Driver %s loaded\n", MODULE_NAME);
  return 0;

// TO GO tags
out_input_unregister_device:
  input_unregister_device(mouse_dev);

out_input_free_device:
  input_free_device(mouse_dev);

out_device_destroy:
  device_destroy(dev_class, devnum);

out_class_destroy:
  class_destroy(dev_class);

out_cdev_del:
  cdev_del(&devs[0].cdev);

out_release_regions:
  release_region(I8042_STATUS_REG + 1, 1);
  release_region(I8042_DATA_REG + 1, 1);

out_unregister:
  unregister_chrdev_region(devnum, VDEV_DEV_COUNT);

out:
  return err;
}

static void __exit vdev_exit(void)
{
  dev_t devnum = MKDEV(VDEV_MAJOR, VDEV_MINOR);

  // Delete char device from system
  cdev_del(&devs[0].cdev);

  // Free IRQ
  free_irq(I8042_KBD_IRQ, &devs[0]);

  // Release I/O keybourd ports
  release_region(I8042_STATUS_REG + 1, 1);
  release_region(I8042_DATA_REG + 1, 1);

  // Unregister char device
  unregister_chrdev_region(devnum, VDEV_DEV_COUNT);

  // Destroy struct class and device file
  device_destroy(dev_class, devnum);
  class_destroy(dev_class);

  // Undregister input device
  input_unregister_device(mouse_dev);

  // Free input device
  input_free_device(mouse_dev);

  pr_notice("VDEV: Driver %s unloaded\n", MODULE_NAME);
}

module_init(vdev_init);
module_exit(vdev_exit);