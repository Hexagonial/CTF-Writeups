
constants = [
0xe1, 0xa7, 0x1e, 0xf8, 
0x75, 0x23, 0x7b, 0x61, 
0xb9, 0x9d, 0xfc, 0x5a, 
0x5b, 0xdf, 0x69, 0xd2, 
0xfe, 0x1b, 0xed, 0xf4, 
0xed, 0x67, 0xf4
]

# Convert all bytes to one concatenated binary string
binary_string = ""
for b in constants:
    binary_string += bin(b)[2:].zfill(8)

# Insert a 0 after every 7th bit and prepend a bit to the start of the string
binary_string = "0" + "0".join(binary_string[i:i+7] for i in range(0, len(binary_string), 7))

# Split the string into groups of 8 and convert each group to a character of the flag
binary_string = " ".join(binary_string[i:i+8] for i in range(0, len(binary_string), 8))
binary_split = binary_string.split(" ")[:-1]
result = ""
for s in binary_split:
    result += chr(int(s, 2))
print(result)