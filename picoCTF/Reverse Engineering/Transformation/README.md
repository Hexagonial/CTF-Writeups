# Transformation
Challenge Description:
> I wonder what this really is... `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> You may find some decoders online
</details>

## Procedure
We are given a file containing a unicode string `灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽` and a line of Python with little context.
```py
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
```

The key thing to note is that this line of Python is probably what was used to generate the flag, not what should be used to "decode" the given string. We need to do what the line of Python does, but in reverse.

The line of Python given takes two characters of the plaintext flag, concatenates their bytes, and returns the unicode character that represents the concatenation of the two bytes. Basically, it converts a flag with 1-byte characters into a flag with 2-byte characters.

So, all we need to do is take each 16-byte character of the encoded string and separate it into two 8-byte characters. You can separate a 16-byte character into two 8-byte chunks by shifting the character 8 bits right to obtain the upper 8 byte chunk, and bitwise ANDing it with `0xff` to get the lower 8-byte chunk.

```
$ python3 transformation.py 
hammy{u win - hammy}
```

## Solution
1. Parse the given string one character at a time. For each character:
    - Convert its upper 8 bytes to a string X.
    - Convert its lower 8 bytes to a string Y.
    - Concatenate X+Y onto the result.
