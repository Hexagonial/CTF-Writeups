# Tap into Hash
Challenge Description:
> Can you make sense of this source code file and write a function that will decode the given encrypted file content?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Do you know what blockchains are? If so, you know that hashing is used in blockchains.
</details>
<details>
<summary>Hint 2</summary>

> Download the encrypted flag file and the source file and reverse engineer the source file.
</details>

## Procedure
Knowing how blockchain works at a basic level will make this challenge less daunting, but in the end you don't need to know about blockchain to solve it. It did help me in parsing what the `main()` function was doing, though. 

We are given the source code for generating a dummy blockchain, which generates a blockchain of length 5, converts it to a string (delimited by `-` between each block), sandwiches a chosen string (argv[1]) in the middle of the blockchain, and encrypts the result using a random key string. We are given both the key and the encrypted blockchain string and need to extract the flag.

The first probable step is to decrypt the blockchain since that will reveal the string sandwiched in the middle of the blockchain, and the string has a good chance of being the flag. So let's look at the `encrypt()` function and implement a `decrypt` function that does the opposite.
```py
def encrypt(plaintext, inner_txt, key):
    midpoint = len(plaintext) // 2

    first_part = plaintext[:midpoint]
    second_part = plaintext[midpoint:]
    modified_plaintext = first_part + inner_txt + second_part
    block_size = 16
    plaintext = pad(modified_plaintext, block_size)
    key_hash = hashlib.sha256(key).digest()

    ciphertext = b''

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        cipher_block = xor_bytes(block, key_hash)
        ciphertext += cipher_block

    return ciphertext
```
Conveniently enough, it looks like encryption (after padding and string insertion) does not change the length of the string between the plaintext and ciphertext variants, and leaves the ciphertext at a length that fits the block size (since all that's being done is XOR operations). Therefore, we can ignore all the padding/string insertion/midpoint calculation activity at the beginning of the `encrypt` function and simply implement `decrypt` that does the opposite of the rest.
```py
def decrypt(ciphertext, key):
    block_size = 16
    key_hash = hashlib.sha256(key).digest()

    plaintext = b''

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        plain_block = xor_bytes(block, key_hash)
        plaintext += plain_block
    
    return plaintext
```
Decrypting the encrypted blockchain gives us the flag in the middle of the plaintext blockchain.
```
$ python3 tap-into-hash.py
hammy{u win - hammy}
```

## Solution
1. Implement a `decrypt` function that performs the opposite of the `encrypt` function.
2. Decrypt the given encrypted blockchain with the given key.

## Key Takeaways
Although it wasn't needed in the end, I watched a good refresher video on how blockchain works. Maybe this knowledge will be helpful later on