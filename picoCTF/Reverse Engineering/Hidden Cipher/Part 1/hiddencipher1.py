encrypted_flag = "235a201d702015483b1d412b265d3313501f0c072d135f0d2002302d5011305120100a452e"
secret = b"S3Cr3t"

for i in range(0, len(encrypted_flag), 2):
    curr_byte = int(encrypted_flag[i:i+2], 16)
    print(chr(curr_byte ^ secret[(i//2) % 6]), end="")

print()