
def switchBits(b, p1, p2):
    mask1 = 1 << p1
    mask2 = 1 << p2
    bit1 = b & mask1
    bit2 = b & mask2
    rest = b & ~(mask1 | mask2)
    shift = p2 - p1
    result = (bit1 << shift) | (bit2 >> shift) | rest

    return result

expected = [0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4, 0xF0,
            0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86, 0xD0, 0xA5, 0x45, 0x96,
            0x27, 0xB5, 0x77, 0x94, 0xC1, 0x95, 0xE0, 0xA4, 0xA5, 0x95, 0xF0,
            0xE0]

result = ''

for c in expected:
    b = c
    b = switchBits(b, 6, 7)
    b = switchBits(b, 2, 5)
    b = switchBits(b, 3, 4)
    b = switchBits(b, 0, 1)
    b = switchBits(b, 4, 7)
    b = switchBits(b, 5, 6)
    b = switchBits(b, 0, 3)
    b = switchBits(b, 1, 2)
    result = result + chr(int(b))

print(result)