# Forky
Challenge Description:
> In this program, identify the last integer value that is passed as parameter to the function doNothing().

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What happens when you fork?
</details>

<br>Hint 2:
> The flag is picoCTF{IntegerYouFound}. For example, if you found that the last integer passed was 1234, the flag would be picoCTF{1234}

## Procedure
A call to `fork()` in C spawns a child process that runs in parallel to its parent, continuing execution to the instruction just after the call to `fork()`. 

The given binary calls `fork()` four times in a row, thus ending the calls with a total of 16 processes. Here's the disassembly with simplified annotations (which are technically incorrect, but for the purposes of this challenge are enough):
```
# eax = 0x3b9aca00
0x59da0255 <+75>:	mov    eax,DWORD PTR [ebp-0xc]
0x59da0258 <+78>:	mov    DWORD PTR [eax],0x3b9aca00

# 16 total processes after
0x59da025e <+84>:	call   0x59da00a0 <fork@plt>
0x59da0263 <+89>:	call   0x59da00a0 <fork@plt>
0x59da0268 <+94>:	call   0x59da00a0 <fork@plt>
0x59da026d <+99>:	call   0x59da00a0 <fork@plt>

# eax += 0x499602d2
0x59da0272 <+104>:	mov    eax,DWORD PTR [ebp-0xc]
0x59da0275 <+107>:	mov    eax,DWORD PTR [eax]
0x59da0277 <+109>:	lea    edx,[eax+0x499602d2]
0x59da027d <+115>:	mov    eax,DWORD PTR [ebp-0xc]
0x59da0280 <+118>:	mov    DWORD PTR [eax],edx
0x59da0282 <+120>:	mov    eax,DWORD PTR [ebp-0xc]
0x59da0285 <+123>:	mov    eax,DWORD PTR [eax]

# Call doNothing(eax)
0x59da0287 <+125>:	sub    esp,0xc
0x59da028a <+128>:	push   eax
0x59da028b <+129>:	call   0x59da01ed <doNothing>
```

Because there are 16 total processes after the forks, `eax += 0x499602d2` runs 16 times bringing the total to `0x3b9aca00 + 0x499602d20 = 0x4d4faf720`. Integers can only fit 4 bytes so the leading 0x4 is truncated to `0xd4faf720`. Represented in a signed integer, `0xd4faf720` = -721750240, which is the flag.

## Solution
`0x3b9aca00 + 0x499602d20 = 0x4d4faf720` = `-721750240` as a signed 32-bit integer
