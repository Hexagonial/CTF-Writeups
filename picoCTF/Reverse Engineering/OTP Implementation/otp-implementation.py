
enc_flag = 0x8747ec551f7b75123badcba2f3feda371db6e57995bebc50b165d307156b2a547bb67e56262615fabf068468859e0d234739
expected = b"pnbopoejdmapflhkefabijeajpcijdniefahigichdmhekgohnhdkfdjbgapnhndlcbeglloaogkokbiffbhomgpminjpgieieme"

"""
The final loop of main adds 0x61 to each element of mystery, so subtract 0x61 from each byte of expected
"""

def subtract_a(c: int):
    return c - 0x61

mystery = list(map(subtract_a, expected))

"""
jumble returns a value according to these rules:
- If 2 * (ord(input_buffer[i])) <= 0xf, return 2 * (ord(input_buffer[i]))
    - Values 0-7 will return 2 * (ord(input_buffer[i]))
- Else, return 2 * (ord(input_buffer[i])) + 1
    - Values 8-f will return 2 * (ord(input_buffer[i])) + 1
"""

def jumble(c: int):
    double = 2 * c
    if double <= 0xf:
        return double
    return double+1

"""
1. mystery[0] = jumble(input_buffer[0]) & 0xf
2. mystery[i] = jumble(input_buffer[i])+mystery[i-1] & 0xf for i > 0
"""

key = [-1]*100

# 1. mystery[0] = jumble(input_buffer[0]) & 0xf
key[0] = 0xf

# 2. mystery[i] = jumble(input_buffer[i])+mystery[i-1] & 0xf for i > 0
for i in range(len(mystery)-1, 0, -1):
    # Only hexadecimal digits are valid input characters, brute force them until we find one that makes the calculation add up xdd
    for j in range(0, 16):
        if mystery[i] == (jumble(j) + mystery[i-1]) & 0xf:
            key[i] = j
            break

key = ''.join(hex(key[i])[2:] for i in range(len(key)))
print("Key: " + key)
key = int(key, 16)
flag = hex(enc_flag ^ key)[2:]
flag = "Flag: " + "".join(chr(int(flag[i:i+2], 16)) for i in range(0, len(flag), 2))

print(flag)