def simplify(ext):
    new_p = []
    new_z = []
    new_c = []

    for i in range(len(ext[0])):
        if ext[0][i] in new_p and ext[1][i] in new_z:
            a = new_p.index(ext[0][i])

            if new_z[a] == ext[1][i]:
                new_c[a] += 1
        else:
            new_p.append(ext[0][i])
            new_z.append(ext[1][i])
            new_c.append(1)

    return new_p, new_z, new_c

##res = ([], [])
##for i in range(5):
##    res = simplify(next_y(res))
##
##    for i in range(len(res[0])):
##        print("{}/{} * x ^ {} + ".format(res[2][i], res[1][i], res[0][i]), end="")
##    print("\n")

def next_y(prev):
    new_p = []
    new_z = []

    for i in range(len(prev[0])):
        for j in range(len(prev[0])):
            p = prev[0][i] + prev[0][j] + 1

            if p in new_p:
                new_z[new_p.index(p)] += (prev[1][i] * prev[1][j] / p)
            else:
                new_p.append(p)
                new_z.append(prev[1][i] * prev[1][j] / p)

    return [3] + new_p, [1.0/3.0] + new_z

def picar(x, n=1):
    y = 0

    coefs = ([], [])
    for i in range(n):
        coefs = next_y(coefs)

##    print(coefs)
    print(max(coefs[0]))

    for i in range(len(coefs[0])):
        y += (x ** coefs[0][i]) * coefs[1][i]

    return y

#print(next_y(([], [])))

print(picar(2.0, 10))
