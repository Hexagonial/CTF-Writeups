# bytemancy 0-3

This is a writeup for all parts of bytemancy, since most parts are easy.

Challenge Description:
> Can you conjure the right bytes?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>50/100/200/400</b>
<br>Difficulty: <b>Easy-Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author for bytemancy 3.
<details>
<summary>Hint 1</summary>

> objdump -t spellbook reveals the symbol table.
</details>
<details>
<summary>Hint 2</summary>

> Send the addresses as 4 raw bytes in little-endian order.
</details>
<details>
<summary>Hint 3</summary>

> pwnlib.util.packing.p32() simplifies crafting the payloads.
</details>

## bytemancy 0-2
bytemancy 0 asks us to send ASCII decimal 101, 101, 101 side-by-side with no delimiters. If you reference an ASCII table, the decimal value 101 translates to the letter `e`. So, send `eee`.
```
==> eee
hammy{u win - hammy}
```
bytemancy 1 asks for the same thing, but 1751 characters long instead of just 3. You can whip out pwntools for this, or you can simply run the following to get a copy-pastable input:
```
$ python3
Python 3.10.12 (main, Mar  3 2026, 11:56:32) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("e"*1751)
eeeeeeeeeeeeeeeeeeeee...
```
bytemancy 2 asks for three `\xff` bytes instead of `e`s. Now we can't just use the keyboard, so the easiest way for me is to whip out pwntools. `echo -ne "\xff\xff\xff"` gives three `\xff` bytes but I don't know how to feed that into the netcat connection, so if you do there you go.
```py
from pwn import *

# Disable logs
context.log_level = 69

target = remote("lonely-island.picoctf.net", 62607)

# Wait until we get the prompt
target.recvuntil(b"==>")

# Send the bytes
target.sendline(b"\xff\xff\xff")

# Get the flag
print(target.recvall().decode())
```

## bytemancy 3
This part is a bit more involved as it asks you for three 4-byte little-endian addresses of certain symbols in the given `spellbook` binary.

As hint 1 suggests, you can use `objdump -t spellbook` to find the addresses of all the symbols on the left.
```
08049176 g     F .text	00000024              ember_sigil
...
0804919a g     F .text	00000027              glyph_conflux
...
080491e3 g     F .text	00000031              binding_word
...
08049214 g     F .text	00000073              main
...
080491c1 g     F .text	00000022              astral_spark
```

Using pwntools to parse the prompts and pack the addresses into little-endian order, we can get the flag.
```
$ python3 bytemancy-3.py
hammy{u win - hammy}
```

## Solution
1. Read the procedures (or script for part 3)
