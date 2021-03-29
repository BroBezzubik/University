import math

Rzm = 4430
Rh = 6000
f = 49
Uf = 211

def w(f=49):
    result = 2 * math.pi * f
    return result

def Ih_16(Ce):
    Uf = 211
    Rh = 6000
    W = w()
    print(Ce)
    result = 3 * Uf * W * Ce / math.sqrt( 1 + 9 * pow(Rh,2) * pow(W, 2) * pow(Ce,2))
    print("blabla", result)
    return result

def Ih(Re):
    Uf = 211
    Rh = 6000
    Ce=0
    result = Uf / (Rh + Re / 3)
    print(result)

def Ih_8(Rh):
    Re = 100
    Ce = 0
    result = Uf / Rh
    print(result)

def Ih_14(Rh):
    Re = 100
    result = Uf / (Rh + Re / 3)
    print(result)


def Ih_19(Rh):
    Rzm = 100
    R0 = 4
    result = Uf * (Rzm + math.sqrt(3) * R0) / (Rh * (Rzm + R0))
    print(result)

def Ih_21(Rh):
    Rzm = 100
    result = math.sqrt(3) * Uf / (Rh + Rzm)
    print(result)


def main():
    #for el in [1, 2.5, 10, 25, 100]:
    #    Ih(el)

    #for el in [0, 0.02, 0.1, 0.25, 1, 2.5]:
    #    Ih_16(el)

    #for el in [1, 5, 10]:
    #    Ih_14(el)

    for el in [1, 5, 10]:
        Ih_21(el)
    
main()
