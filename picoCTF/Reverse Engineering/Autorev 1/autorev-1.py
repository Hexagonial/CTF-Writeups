from pwn import *
# import os

context.log_level = 69

target = remote("mysterious-sea.picoctf.net", 54640)

# Generate the binary by translating the raw bytes into actual bytes and writing to a file.
def generate_binary(raw):
    bin = open("bin", "wb")
    to_write = b""
    for i in range (0, len(raw), 2):
        byte = int(raw[i:i+2], 16).to_bytes(1, "little")
        to_write += byte
    bin.write(to_write)
    bin.close()
    # os.system("chmod +x bin")

# Get the secret from the generated binary.
def get_secret():
    gdb_process = process(["gdb", "bin"])

    # REPLACE ➤ WITH WHATEVER PROMPT YOUR GDB GIVES YOU. I use gef which uses that arrow
    gdb_process.recvuntil("➤".encode())

    # Each generated binary is the same except with a different 4-byte secret.
    # The secret is constant and is therefore built into an instruction in main.
    # You can find the constant at main+11
    gdb_process.sendline(b"x/wx *main+11")
    gdb_process.recvuntil(b"11>:")

    secret = int(gdb_process.recvline().strip(), 16)
    gdb_process.close()

    return secret

# 20 binaries
for i in range(20):
    print("Reversing binary #" + str(i+1) + "...")

    # Receive the raw binary bytes, and convert them to actual bytes
    target.recvuntil(b"bytes:\n")
    raw = target.recvline().strip().decode()
    generate_binary(raw)

    # Secret is at main+11

    target.recvuntil(b"secret?:")
    target.sendline(str(get_secret()).encode())

target.recvuntil(b"Correct!")
print(target.recvall().decode())