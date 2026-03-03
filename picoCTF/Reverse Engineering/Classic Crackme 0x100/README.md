# Classic Crackme 0x100
Challenge Description:
> A classic Crackme. Find the password, get the flag!

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Let the machine figure out the symbols!
</details>

## Procedure
The given binary takes (up to) 50 characters as a password input, transforms the input, and compares the result to the expected value. To analyze the binary in gdb we need to run it once before we can disassemble main. When main is disassembled, we can try to look for the "decision point" that determines if our input is correct.
```
0x000000000040136a <+500>:	call   0x401060 <memcmp@plt>
0x000000000040136f <+505>:	test   eax,eax
0x0000000000401371 <+507>:	jne    0x401389 <main+531>
0x0000000000401373 <+509>:	mov    esi,0x402029
0x0000000000401378 <+514>:	mov    edi,0x402040
0x000000000040137d <+519>:	mov    eax,0x0
0x0000000000401382 <+524>:	call   0x401050 <printf@plt>
0x0000000000401387 <+529>:	jmp    0x401393 <main+541>
0x0000000000401389 <+531>:	mov    edi,0x402060
0x000000000040138e <+536>:	call   0x401030 <puts@plt>
0x0000000000401393 <+541>:	mov    eax,0x0
0x0000000000401398 <+546>:	leave  
0x0000000000401399 <+547>:	ret    
```
At `*main+500`, we see a call to `memcmp` followed by a `test` and a branch between two print statements. Examining the strings passed into these print statements shows this is the decision point.
```
gef➤  x/s 0x402040
0x402040:	"SUCCESS! Here is your flag: %s\n"
gef➤  x/s 0x402060
0x402060:	"FAILED!"
```

Let's put a breakpoint at `*main+500` and see what's being passed into the memcmp. The input used is `hammy`.
```
→   0x40136a <main+01f4>      call   0x401060 <memcmp@plt>
   ↳    0x401060 <memcmp@plt+0000> jmp    QWORD PTR [rip+0x2fb2]        # 0x404018 <memcmp@got.plt>
        0x401066 <memcmp@plt+0006> push   0x3
        0x40106b <memcmp@plt+000b> jmp    0x401020
        0x401070 <setvbuf@plt+0000> jmp    QWORD PTR [rip+0x2faa]        # 0x404020 <setvbuf@got.plt>
        0x401076 <setvbuf@plt+0006> push   0x4
        0x40107b <setvbuf@plt+000b> jmp    0x401020
──────────────────────────────────────────────────────────────────────────────────────────────────────
memcmp@plt (
   $rdi = 0x00007ffe465cebb0 → "hdpsbTTWQTTWTWWZQTTWTWWZTWWZWZZ]QTTWTWWZTWWZWZZ]TW",
   $rsi = 0x00007ffe465cebf0 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze",
   $rdx = 0x0000000000000032,
   $rcx = 0x00007ffe465cebf0 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze"
)
```
It doesn't look like our raw input is being passed into the `memcmp`, and it was instead transformed in some way. Additionally, it seems like the input might need to match the length of the "expected" value in `$rsi`, so we need an input 50 characters long. Let's see what is passed in with `hammy` repeated 10 times as input:
```
memcmp@plt (
   $rdi = 0x00007ffd42968010 → "hdpsbngvpenjsvhtdsshnjvyeqjyvktppseqgvvknjvyhtmbsh",
   $rsi = 0x00007ffd42968050 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze",
   $rdx = 0x0000000000000032,
   $rcx = 0x00007ffd42968050 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze"
)
```
The transformed input is starting to look a bit more like the expected value in that they both consist only of lowercase characters.

What happens if we input `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` (fifty `a`s)?
```
memcmp@plt (
   $rdi = 0x00007fff16781ad0 → "addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj",
   $rsi = 0x00007fff16781b10 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze",
   $rdx = 0x0000000000000032,
   $rcx = 0x00007fff16781b10 → "qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze"
)
```
It's quite possible that all the transformation is doing is rotating the characters in our input through the alphabet. Let's compare the transformed output of fifty `a`s with that of fifty `b`s:
```
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj

bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
beehehhkehhkhkknehhkhkknhkknknnqehhkhkknhkknknnqhk
```
We can observe that the transformed output of fifty `b`s is one letter down the alphabet from that of fifty `a`s. Therefore, we can try taking the expected output `qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze` and applying the same transformation (rotations) in reverse. This can be done by taking the input `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` and respective output `addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj` and seeing how much each index was rotated, then doing the reverse rotation on the expected output.
```
$ python3 classic-crackme-0x100.py | ./crackme100
Enter the secret password: SUCCESS! Here is your flag: hammy{u win - hammy}
```
The password is the same on the remote machine.

## Solution
1. Enter `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` as the password, and copy the transformed version of your input as it's passed into `memcmp` at `*main+500`.
2. Determine how much each character of your input is rotated down the alphabet by comparing the original input to the argument given to `memcpy`.
3. Apply the rotations in reverse to the "expected value" passed into `memcpy`.
    - `qhcpgbpuwbaggepulhstxbwowawfgrkzjstccbnbshekpgllze`
