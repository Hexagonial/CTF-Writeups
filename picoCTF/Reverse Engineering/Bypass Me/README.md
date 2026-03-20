# Bypass Me
Challenge Description:
> Your task is to analyze and exploit a password-protected binary called bypassme.bin and binary performs input sanitization. However, instead of guessing the password, you are expected to reverse engineer or debug the program to bypass the authentication logic and retrieve the hidden flag. You'll need to think like an attacker using tool like LLDB to uncover how the binary works under the hood and leak the correct password.

CTF: <b>picoCTF 2026</b><br>Points: <b>100</b><br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Try disassembling the binary to understand its inner workings.
</details>
<details>
<summary>Hint 2</summary>

> Pay special attention to functions available
</details>
<details>
<summary>Hint 3</summary>

> The password might be hidden or decoded at runtime
</details>

## Procedure
This is a reasonably simple reverse engineering challenge, but the only reason it's hard is because it forces you to use `lldb` instead of gdb/gef/your favorite flavor of gdb enhancement. Half of your time is spent figuring out how to see all available functions and disassemble main, and the other half is spent trying to place a breakpoint at the end of a certain function you find.

When disassembling main during execution, we see an interesting-looking function address near the top:
```
(lldb) dis -n main
bypassme.bin`main:
    0x5c1b0347662e <+0>:   endbr64 
    0x5c1b03476632 <+4>:   pushq  %rbp
    0x5c1b03476633 <+5>:   movq   %rsp, %rbp
    0x5c1b03476636 <+8>:   subq   $0x220, %rsp              ; imm = 0x220 
    0x5c1b0347663d <+15>:  movq   %fs:0x28, %rax
    0x5c1b03476646 <+24>:  movq   %rax, -0x8(%rbp)
    0x5c1b0347664a <+28>:  xorl   %eax, %eax
    0x5c1b0347664c <+30>:  movl   $0x3, -0x21c(%rbp)
    0x5c1b03476656 <+40>:  leaq   -0x110(%rbp), %rax
    0x5c1b0347665d <+47>:  movq   %rax, %rdi
    0x5c1b03476660 <+50>:  callq  0x5c1b03476333            ; decode_password at bypassme.c:16:33
```

The return value of `decode_password` might hold the correct password. If we set a breakpoint near the end of `decode_password` (before the value of rax is overwritten) rax might contain the correct passwordl.
```
    0x5c1b034763ae <+123>: movq   -0x8(%rbp), %rax
    0x5c1b034763b2 <+127>: xorq   %fs:0x28, %rax
    0x5c1b034763bb <+136>: je     0x5c1b034763c2            ; <+143> at bypassme.c:22:1
    0x5c1b034763bd <+138>: callq  0x5c1b03476140
    0x5c1b034763c2 <+143>: leave  
    0x5c1b034763c3 <+144>: retq   

(lldb) breakpoint set -a 0x5c1b034763ae
```
After hitting the breakpoint we can use `frame variable` to check what the address held by `rax` points to.
```
(lldb) frame variable
(char *) out = 0x00007ffd99176000 "SuperSecure"
(unsigned char [11]) enc = "�����������
```
Entering `SuperSecure` as the password gives us the flag.

## Solution
1. Enter `SuperSecure` as the password
