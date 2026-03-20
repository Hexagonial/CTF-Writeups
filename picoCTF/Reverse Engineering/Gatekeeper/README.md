# Gatekeeper
Challenge Description:
> What’s behind the numeric gate? You only get access if you enter the right kind of number.

CTF: <b>picoCTF 2026</b>
<br>Points: <b>100</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Tools like Ghidra, IDA Free, or Radare2 can analyze the binary’s logic.
</details>
<details>
<summary>Hint 2</summary>

> The program’s output isn’t straightforward; reversing the string and cleaning out extra text may help you recover the flag.
</details>

## Procedure
We can begin by analyzing `main` section by section and determining what it does.

The first section reads your input into a buffer at `$rbp-0x30` and stores its length in `$rbp-0x34`.
```
gef➤  disass main
Dump of assembler code for function main:
   0x000055555555557f <+0>:	endbr64 
   0x0000555555555583 <+4>:	push   rbp
   0x0000555555555584 <+5>:	mov    rbp,rsp
   0x0000555555555587 <+8>:	sub    rsp,0x40
   0x000055555555558b <+12>:	mov    rax,QWORD PTR fs:0x28
   0x0000555555555594 <+21>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000555555555598 <+25>:	xor    eax,eax
   0x000055555555559a <+27>:	lea    rdi,[rip+0xaa7]
   0x00005555555555a1 <+34>:	mov    eax,0x0
   0x00005555555555a6 <+39>:	call   0x5555555551d0 <printf@plt>  <-- printf("Enter a numeric code (must be > 999 ):")
   0x00005555555555ab <+44>:	mov    rax,QWORD PTR [rip+0x2a5e]
   0x00005555555555b2 <+51>:	mov    rdi,rax
   0x00005555555555b5 <+54>:	call   0x555555555220 <fflush@plt>
   0x00005555555555ba <+59>:	lea    rax,[rbp-0x30]
   0x00005555555555be <+63>:	mov    rsi,rax
   0x00005555555555c1 <+66>:	lea    rdi,[rip+0xaa8]
   0x00005555555555c8 <+73>:	mov    eax,0x0
   0x00005555555555cd <+78>:	call   0x555555555260 <__isoc99_scanf@plt>  <-- scanf("%31s", buf)
   0x00005555555555d2 <+83>:	mov    DWORD PTR [rbp-0x38],0xffffffff
   0x00005555555555d9 <+90>:	lea    rax,[rbp-0x30]
   0x00005555555555dd <+94>:	mov    rdi,rax
   0x00005555555555e0 <+97>:	call   0x5555555551b0 <strlen@plt>  <-- strlen(buf)
   0x00005555555555e5 <+102>:	mov    DWORD PTR [rbp-0x34],eax
```

Next, it determines if your input is a valid number (either decimal or hex). For now, let's assume `is_valid_decimal` and `is_valid_hex` do exactly as they're named and just determine if your input is a valid number - decimal, or hex if not a valid decimal. Based on if your input is a decimal or hex, the program calls `atoi` or `strtol` respectively to convert it from a string to a number. The number representation of your input is stored at `$rbp-0x38`.
```
0x00005555555555e8 <+105>:	lea    rax,[rbp-0x30]
0x00005555555555ec <+109>:	mov    rdi,rax
0x00005555555555ef <+112>:	call   0x5555555553d9 <is_valid_decimal>
0x00005555555555f4 <+117>:	test   eax,eax
0x00005555555555f6 <+119>:	je     0x555555555609 <main+138>    <-- If is_valid_decimal returns 0, it's not a valid decimal.

0x00005555555555f8 <+121>:	lea    rax,[rbp-0x30]
0x00005555555555fc <+125>:	mov    rdi,rax
0x00005555555555ff <+128>:	call   0x555555555250 <atoi@plt>    <-- If is_valid_decimal, convert the input using atoi
0x0000555555555604 <+133>:	mov    DWORD PTR [rbp-0x38],eax     <-- Store conversion into $rbp-0x38
0x0000555555555607 <+136>:	jmp    0x555555555647 <main+200>

0x0000555555555609 <+138>:	lea    rax,[rbp-0x30]
0x000055555555560d <+142>:	mov    rdi,rax
0x0000555555555610 <+145>:	call   0x555555555369 <is_valid_hex>    <-- If the input is not decimal, check if it's hex.
0x0000555555555615 <+150>:	test   eax,eax
0x0000555555555617 <+152>:	je     0x555555555634 <main+181>
0x0000555555555619 <+154>:	lea    rax,[rbp-0x30]
0x000055555555561d <+158>:	mov    edx,0x10
0x0000555555555622 <+163>:	mov    esi,0x0
0x0000555555555627 <+168>:	mov    rdi,rax
0x000055555555562a <+171>:	call   0x555555555200 <strtol@plt>  <-- Convert a valid hex string to a number with strtol(buf, 0, 16)
0x000055555555562f <+176>:	mov    DWORD PTR [rbp-0x38],eax
0x0000555555555632 <+179>:	jmp    0x555555555647 <main+200>

# If reaching here, input is neither valid decimal nor hex. Program exits.
0x0000555555555634 <+181>:	lea    rdi,[rip+0xa3a]        # 0x555555556075
0x000055555555563b <+188>:	call   0x555555555180 <puts@plt>
0x0000555555555640 <+193>:	mov    eax,0x1
0x0000555555555645 <+198>:	jmp    0x555555555698 <main+281>
```

After converting your input to a number, it is run through a series of comparisons. Basically, it checks:
1. Your input must be greater than 0x3e7 and smaller than 0x270f
2. Your input must be exactly 3 characters in size
```
0x0000555555555647 <+200>:	cmp    DWORD PTR [rbp-0x38],0x3e7  
0x000055555555564e <+207>:	jg     0x55555555565e <main+223>    <-- input > 0x3e7?
0x0000555555555650 <+209>:	lea    rdi,[rip+0xa2d]        # 0x555555556084
0x0000555555555657 <+216>:	call   0x555555555180 <puts@plt>    <-- If not, "too small"
0x000055555555565c <+221>:	jmp    0x555555555693 <main+276>

0x000055555555565e <+223>:	cmp    DWORD PTR [rbp-0x38],0x270f  <-- input < 0x270f?
0x0000555555555665 <+230>:	jle    0x555555555675 <main+246>
0x0000555555555667 <+232>:	lea    rdi,[rip+0xa21]        # 0x55555555608f
0x000055555555566e <+239>:	call   0x555555555180 <puts@plt>    <-- If not, "too big"
0x0000555555555673 <+244>:	jmp    0x555555555693 <main+276>

0x0000555555555675 <+246>:	cmp    DWORD PTR [rbp-0x34],0x3     <-- strlen(input) == 3?
0x0000555555555679 <+250>:	jne    0x555555555687 <main+264>    <-- If not, "access denied"
0x000055555555567b <+252>:	mov    eax,0x0
0x0000555555555680 <+257>:	call   0x555555555449 <reveal_flag>
0x0000555555555685 <+262>:	jmp    0x555555555693 <main+276>

0x0000555555555687 <+264>:	lea    rdi,[rip+0xa0b]        # 0x555555556099
0x000055555555568e <+271>:	call   0x555555555180 <puts@plt>
0x0000555555555693 <+276>:	mov    eax,0x0
...
```
Therefore you are required to enter hexadecimal for input because 0x3e7 = 999, and you only get 3 characters. Entering a number that fulfills these conditions (such as 69a) gives us a mutated form of the flag:
```
$ ./gatekeeper 
Enter a numeric code (must be > 999 ): 69a
Access granted: }ymmftc_oc_ipah -ftc_oc_ip niwftc_oc_ip u{yftc_oc_ipmmahftc_oc_ip
```
If you reverse the string and remove all random `pi_co_ctf`s, you get the flag. This is easier to deduce when running with a known debug flag locally.


## Solution
1. Enter a 3-character long hexadecimal (and non-decimal) number x such that `0x3e7 < x < 0x270f`, such as `69a`
2. Reverse the printed string and remove all `pi_co_ctf`s
