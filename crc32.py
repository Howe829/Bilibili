import itertools
table = []
table_reverse = []

def init_tables(poly, reverse=True):
    global table, table_reverse
    table = []
    # build CRC32 table
    for i in range(256):
        for j in range(8):
            if i & 1:
                i >>= 1
                i ^= poly
            else:
                i >>= 1
        table.append(i)
    assert len(table) == 256, "table is wrong size"
    # build reverse table
    if reverse:
        table_reverse = []
        found_none = set()
        found_multiple = set()
        for i in range(256):
            found = []
            for j in range(256):
                if table[j] >> 24 == i:
                    found.append(j)
            table_reverse.append(tuple(found))
            if not found:
                found_none.add(i)
            elif len(found) > 1:
                found_multiple.add(i)
        assert len(table_reverse) == 256, "reverse table is wrong size"
        if found_multiple:
            print('WARNING: Multiple table entries have an MSB in {0}'.format(
                rangess(found_multiple)))
        if found_none:
            print('ERROR: no MSB in the table equals bytes in {0}'.format(
                rangess(found_none)))
def rangess(i):
    return ', '.join(map(lambda x: '[{0},{1}]'.format(*x), ranges(i)))


def ranges(i):
    for kg in itertools.groupby(enumerate(i), lambda x: x[1] - x[0]):
        g = list(kg[1])
        yield g[0][1], g[-1][1]

def calc(data, accum=0):
    accum = ~accum
    for b in data:
        accum = table[(accum ^ b) & 0xFF] ^ ((accum >> 8) & 0x00FFFFFF)
    accum = ~accum
    return accum & 0xFFFFFFFF

def findReverse(desired, accum):
    solutions = set()
    accum = ~accum
    stack = [(~desired,)]
    while stack:
        node = stack.pop()
        for j in table_reverse[(node[0] >> 24) & 0xFF]:
            if len(node) == 4:
                a = accum
                data = []
                node = node[1:] + (j,)
                for i in range(3, -1, -1):
                    data.append((a ^ node[i]) & 0xFF)
                    a >>= 8
                    a ^= table[node[i]]
                solutions.add(tuple(data))
            else:
                stack.append(((node[0] ^ table[j]) << 8,) + node[1:] + (j,))
    return solutions

def rewind(accum, data):
    if not data:
        return (accum,)
    stack = [(len(data), ~accum)]
    solutions = set()
    while stack:
        node = stack.pop()
        prev_offset = node[0] - 1
        for i in table_reverse[(node[1] >> 24) & 0xFF]:
            prevCRC = (((node[1] ^ table[i]) << 8) |
                       (i ^ data[prev_offset])) & 0xFFFFFFFF
            if prev_offset:
                stack.append((prev_offset, prevCRC))
            else:
                solutions.add((~prevCRC) & 0xFFFFFFFF)
    return solutions

if __name__ == '__main__':
    init_tables(0xEDB88320, True)
    r=findReverse(0x9c857fd1,0x00000000)
    print(r)