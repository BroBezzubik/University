from lxml import etree


def get_init(path='data.xml'):
    with open(path) as f:
        xml = f.read()

    root = etree.fromstring(xml)
    elems = root.getchildren()

    R = float(elems[0].text)
    Ck = float(elems[1].text)
    Lk = float(elems[2].text)
    Rk = float(elems[3].text)
    Uc0 = float(elems[4].text)
    I0 = float(elems[5].text)
    Le = float(elems[6].text)

    t_stop = float(elems[7].text)
    t_step = float(elems[8].text)

    n_pow = int(elems[9].text)

    return R, Ck, Lk, Rk, Uc0, I0, Le, t_stop, t_step, n_pow
