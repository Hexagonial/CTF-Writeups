
# I find it easier to implement the reverse of a function when I have the original function to refer to.
def encrypt(plaintext_flag: bytes):
    if len(plaintext_flag) != 24: 
        print("Error: Flag must be exactly 24 bytes.")
        exit()

    result = ""
    for i in range(8):
        char = chr(plaintext_flag[i])
        result += char
    for i in range(8, 23):
        char = plaintext_flag[i]
        if i & 1 != 0:
            char = chr(char - 2)
        else:
            char = chr(char + 5)
        result += char
    result += chr(plaintext_flag[23])

    return result

def decrypt(ciphertext_flag: bytes):
    result = ""
    for i in range(8):
        result += chr(ciphertext_flag[i])
    for i in range(8, 23):
        char = ciphertext_flag[i]
        if i & 1 != 0:
            char = chr(char + 2)
        else:
            char = chr(char - 5)
        result += char
    result += chr(ciphertext_flag[-1])
    return result

rev_this = open("./rev_this", "rb").read().strip()
print(decrypt(rev_this))
