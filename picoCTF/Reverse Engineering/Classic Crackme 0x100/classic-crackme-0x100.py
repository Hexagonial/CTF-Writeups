input = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
output = "addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj"
expected = "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze"

alphabet = "abcdefghijklmnopqrstuvwxyz"
answer = ""

for i in range(len(input)):
    # Get the current character of the input
    inchar = ord(input[i])

    # Get the corresponding character in the output
    outchar = ord(output[i])

    # See how much the input was rotated down the alphabet
    diff = outchar-inchar

    # Rotate the same amount backwards in the corresponding character of the expected value
    answer += alphabet[(alphabet.index(expected[i]) - diff) % 26]

print(answer)