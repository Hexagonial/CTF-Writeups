from pwn import *

target = remote("verbal-sleep.picoctf.net", 64149)
#target = process(["python3", "source.py"])
ciphertext = target.recvall().decode().strip()
L = eval(ciphertext)

result = ""
for i in range(len(L)-2):
    element = L[i]
    print(chr(int(element[0], 16)) + chr(int(element[-1], 16)), end="")

print(chr(int(L[-2][0], 16)) + chr(int(L[-1][0], 16)))