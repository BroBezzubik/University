from random import choice
def generate_shema(count=26):
    list1 = list(range(count))
    list2 = list(range(count))

    shema_front = {}
    shema_back = {}
    while len(list1) > 0 and len(list2) > 0:
        element1 = choice(list1)
        list1.remove(element1)
        list2.remove(element1)
        element2 = choice(list2)
        list1.remove(element2)
        list2.remove(element2)
        shema_front[element1] = element2
        shema_front[element2] = element1
        shema_back[element1] = element2
        shema_back[element2] = element1

    return shema_front, shema_back
