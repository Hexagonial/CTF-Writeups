# Bbbbloat
Challenge Description:
> Can you get the flag? Reverse engineer this binary.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
No hints are provided by the challenge author.

## Procedure
Again we have a binary that doesn't reveal anything (not even function names) when opened in gdb. We can begin by running it and `Ctrl+C`ing it at the first input to begin single stepping through the instructions. This one is a bit annoying because you'll find yourself stuck in some libc functions for a while before landing back in the code address space.

When you return to the code address space and step through the useless computation, you'll run into this `cmp` instruction that looks like it's comparing our input to something. When I ran the program my input was `32` = 0x20.
```
$rax   : 0x20              
...
   0x5d443b0974c8                  mov    eax, DWORD PTR [rbp-0x40]
 → 0x5d443b0974cb                  cmp    eax, 0x86187
```
So it looks like `0x86187` = 549255 might be the answer! Can't say for sure until we try:
```
$ ./bbbbloat 
What's my favorite number? 549255
hammy{u win - hammy}
```

## Solution
1. Enter 549255 as the favorite number.

## Key Takeaways
Ok well after solving `unpackme` I guess `upx-ucl` isn't gonna be a swiss army knife :(
