import copy
poly_crc32_normal=0x104c11db7
crc32_table_normal=[]
for byte in range(256):
    operator=copy.copy(byte)
    operator<<=24
    for bit in range(8):
        if (operator & 0x80000000) != 0:
            operator <<= 1
            operator ^= poly_crc32_normal
        else:
            operator <<= 1
    crc32_table_normal.append(operator)
to_print = list(map(hex, crc32_table_normal))
print(to_print)