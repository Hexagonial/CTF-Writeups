# unpackme
Challenge Description:
> Can you get the flag? Reverse engineer this binary.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What is UPX?
</details>

## Procedure
We are given a binary tha, when opened in gdb, doesn't appear to give us any function names or good places to start looking right off the bat.
```
gef➤  info func
All defined functions:
gef➤  
```
Running it in gdb doesn't reveal much else either, but we can still step through the program by `Ctrl+C`ing at the input.
```
     0x459260                  syscall 
 →   0x459262                  cmp    rax, 0xfffffffffffff000
     0x459268                  ja     0x4592c0
     0x45926a                  ret    
     0x45926b                  nop    DWORD PTR [rax+rax*1+0x0]
```
While I'm sure you'll come across the key instructions if you step through the binary, the easiest way to approach this problem is to <b>unpack</b> the binary. Given the `upx` in the filename and challenge hint, we can try using `upx-ucl` to unpack the binary.
```
$ upx-ucl -d unpackme-upx 
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2020
UPX 3.96        Markus Oberhumer, Laszlo Molnar & John Reiser   Jan 23rd 2020

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
   1002528 <-    379188   37.82%   linux/amd64   unpackme-upx
```
We can see a lot more in gdb now, and even disassemble the main function.
```
gef➤  info func
All defined functions:

Non-debugging symbols:
0x0000000000401000  _init
0x00000000004011b0  __assert_fail_base.cold
0x00000000004011bf  _nl_load_domain.cold
...
```
```
gef➤  disass main
Dump of assembler code for function main:
   0x0000000000401e43 <+0>:	endbr64 
   0x0000000000401e47 <+4>:	push   rbp
   ...
```
Within main we can see the call to `scanf` as well as what our input is compared against.
```
0x0000000000401ead <+106>:	lea    rax,[rbp-0x3c]
0x0000000000401eb1 <+110>:	mov    rsi,rax
0x0000000000401eb4 <+113>:	lea    rdi,[rip+0xb1165]        # 0x4b3020
0x0000000000401ebb <+120>:	mov    eax,0x0
0x0000000000401ec0 <+125>:	call   0x410d30 <__isoc99_scanf>
0x0000000000401ec5 <+130>:	mov    eax,DWORD PTR [rbp-0x3c]
0x0000000000401ec8 <+133>:	cmp    eax,0xb83cb
0x0000000000401ecd <+138>:	jne    0x401f12 <main+207>
```
The address `$rbp-0x3c` is loaded as the buffer for `scanf` at <+106> and <+110> so that's where our input is read. It is then compared with `0xb83cb` = 754635 at <+133>, so we can try using that for the "favorite number."
```
$ ./unpackme-upx 
What's my favorite number? 754635
hammy{u win - hammy}
```

## Solution
1. Enter 754635 as the favorite number.

## Key Takeaways
`upx-ucl` might be a good first step in trying to deobfuscate binaries so they are readable in gdb.