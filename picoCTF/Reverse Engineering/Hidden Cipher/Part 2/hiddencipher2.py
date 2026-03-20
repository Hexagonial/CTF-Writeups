from pwn import *

context.log_level = 69

target = remote("crystal-peak.picoctf.net", 58525)

target.recvuntil(b"is ")
answer = eval(target.recvuntil(b"?", drop=True).decode())
target.sendline(str(answer).encode())

target.recvuntil(b"values:")
encoded_values = eval("[" + target.recvall().strip().decode() + "]")

for i in range(len(encoded_values)):
    original_byte = int(encoded_values[i]) // answer
    print(chr(original_byte), end="")

print()