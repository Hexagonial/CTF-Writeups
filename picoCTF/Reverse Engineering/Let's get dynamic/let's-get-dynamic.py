
# I was too lazy to separate all the constants into individual bytes
constants_part_1 = [
    0x08D4EC402F479F0D,
    0x5E9538A3D9225F42,
    0xB54A06A329AE5FDF,
    0x45CA76A14C8B955C,
    0x8B4061A7C49FC7B8,
    0xC3E34692E550E8AA
]

constants_part_2 = [
    0x6787AE145035E46E,
    0x1DEB17D1F5553C3D,
    0xEE3C31DD459B33E8,
    0x3BF408DB71DDEC66,
    0xE01922F6C7DD80D4,
    0x82BB489CBF50E1A1
]

flag = ""

# Each constant is made of 8 bytes, and we iterate over 6 constants.
# For each constant:
for i in range(6):
    # For each byte index in the constant:
    for j in range(8):
        # Get the byte we are currently on
        byte1 = (constants_part_1[i] >> (8*j)) & 0xFF
        byte2 = (constants_part_2[i] >> (8*j)) & 0xFF

        # Perform flag[i] = constants_part_2[i] ^ constants_part_1[i] ^ index ^ 19
        flag += chr(byte2 ^ byte1 ^ (8*i+j) ^ 19)

print(flag)