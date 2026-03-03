
enc = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽"
flag = ''

for i in range(0, len(enc)):
    # Convert the character to an integer
    charInt = ord(enc[i])

    # Separate the upper and lower 8 bytes of the integer
    upperBytes = charInt >> 8
    lowerBytes = charInt & 0xff

    # Convert the upper and lower chunks to characters
    flag += chr(upperBytes) + chr(lowerBytes)

print(flag)
