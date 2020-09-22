def save_into_file(values: list, keys: list = [], width: int = 15, pts: int = 3, file=0):
    if not keys:
        for i in range(len(values)):
            keys.append(i)

    if len(values) != len(keys):
        raise ValueError('len(values) != len(keys)')

    if file == 0:
        file = open('output.txt', 'w')
    elif type(file) == type(str):
        file = open(file, 'w')

    file.write('\n')

    vertical_line = ('+' + '-' * width) * len(values) + '+'
    file.write(vertical_line + '\n')

    line = '|'
    for i in range(len(keys)):
        line += '{:^{width}}|'.format(keys[i], width=width)
    file.write(line + '\n')

    file.write(vertical_line + '\n')

    for j in range(len(values[0])):
        line = '|'
        for i in range(len(values)):
            line += '{:>{width}.{pts}f}|'.format(float(values[i][j]), width=width, pts=pts)
        file.write(line + '\n')
        file.write(vertical_line + '\n')

    file.write('\n')

    file.close()
