from auto_shema import *
from pregened_shema import *

def main():
    print("0 - auto-gen-shema\n1 - prepared-shema")
    key = int(input(">>"))
    if key == 0:
        pass
        auto_shema()
    elif key == 1:
        prepared_shema()
    else:
        exit(1)


if __name__ == '__main__':
    main()