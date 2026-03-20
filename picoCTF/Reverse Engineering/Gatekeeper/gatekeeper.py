from pwn import *

context.log_level = 69

target = remote("green-hill.picoctf.net", 50760)

target.recvuntil(b": ")
target.sendline(b"69a")

target.recvuntil(b"granted: ")
flag = "".join(target.recvall().decode()[::-1].split("pi_co_ctf"))

print(flag)