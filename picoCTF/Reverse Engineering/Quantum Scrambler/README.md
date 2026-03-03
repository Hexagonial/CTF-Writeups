# Quantum Scrambler
Challenge Description:
> We invented a new cypher that uses "quantum entanglement" to encode the flag. Do you have what it takes to decode it?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author. <br><b>DISCLAIMER: Hint 2 pretty much gives away the solution, but hints 1 and 3 are quite helpful without giving away anything.</b>
<details>
<summary>Hint 1</summary>

> Run eval on the cypher to interpret it as a python object
</details>
<br><details>
<summary>Hint 2</summary>

> Print the outer list one object per line
</details>
<br><details>
<summary>Hint 3</summary>

> Feed in a known plaintext through the scrambler
</details>

## Procedure
The easiest way to approach a soft-cryptography problem like this is to copy the ciphertext generator and run your own plaintext through it. Clearly the flag is quite long and produces a whole load of baloney so let's run a shorter, more structured plaintext through it: `abcdefg`

I modified the source code for two things:
1. Color-formatted print statements to see the transformations done by `scramble` more easily
2. To be able to pass in our own plaintext to `get_flag` without having to modify the flag.txt file
```py
# Returns a list of all the flag characters in hex (string)
def get_flag(flag = open('flag.txt', 'r').read()):
  flag = flag.strip()
  hex_flag = []
  for c in flag:
    hex_flag.append([str(hex(ord(c)))])

  return hex_flag

test = get_flag("abcdefg")
print(scramble(test))
exit()
```
```
[['0x61', '0x62'], ['0x63', [], '0x64'], ['0x65', [['0x61', '0x62']], '0x66'], ['0x67', [['0x61', '0x62'], ['0x63', [], '0x64']]]]
```
By looking at the ciphertext output, we can try to piece the plaintext back together. It looks like we can piece it back together by reading only the first and last elements of each subarray in the ciphertext, except the last subarray in which we only read the first element. We can test this theory on a longer plaintext `hammy{u win - hammy}`.
```
$ python3 source.py | python3 quantum-scrambler.py 
...
hammy{u win - hammy}
```
So that's all we have to do with the target machine's ciphertext.

Note: With shorter plaintexts apparently we only need to make the exception for the last subarray, but at some point when the plaintext gets longer the exception needs to be made for the last two subarrays. The working exploit made the exception for the last two subarrays. Not sure why this is

## Solution
1. Parse the ciphertext by running it through `eval()` to get it in array form.
2. Read only the first and last elements of each subarray in the ciphertext, except the last two subarrays in which only the first element should be read.
