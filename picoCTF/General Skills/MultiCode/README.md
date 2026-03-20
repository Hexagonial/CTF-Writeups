# MultiCode
Challenge Description:
> We intercepted a suspiciously encoded message, but it’s clearly hiding a flag. No encryption, just multiple layers of obfuscation. Can you peel back the layers and reveal the truth?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>200</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> The flag has been wrapped in several layers of common encodings such as ROT13, URL encoding, Hex, and Base64. Can you figure out the order to peel them back?
</details>
<details>
<summary>Hint 2</summary>

> A tool like CyberChef can be interesting.
</details>

## Procedure
The flag has been run through multiple layers of encoding and we need to decode it. 
```
NjM3NjcwNjI1MDQ3NTMyNTM3NDI2MTcyNjY2NzcyNzE1ZjcyNjE3MDMwNzE3NjYxNzQ1ZjM0MzgzMTczMzAzNjM0NzAyNTM3NDQ=
```

The first encoding looks like base64. Decoding it gives us:
```
637670625047532537426172666772715f72617030717661745f3438317330363470253744
```

The second encoding looks like hexadecimal ASCII bytes. Decoding it gives us:
```
cvpbPGS%7Barfgrq_rap0qvat_481s064p%7D
```

We can see some strange sequences `%7B` and `%7D` in the third encoding, and these resemble URL encoded bytes. We can replace them with text (open brace and closing brace respectively)
```
cvpbPGS{arfgrq_rap0qvat_481s064p}
```

The final encoding looks like it could be a shift cipher. We can just brute-force caesar cipher to find out it's ROT13:
```
hammy{u win - hammy}
```

## Solution
1. See procedure
