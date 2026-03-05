# Let's get dynamic
Challenge Description:
> Can you tell what this file is reading?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Running this in a debugger would be helpful
</details>

## Procedure
After reading so much assembly in Intel syntax, seeing AT&T syntax gave me a headache. First order of business is to convert every large decimal constant to hexadecimal before beginning our analysis.

We can begin by analyzing the disassembly and building an image of the stack layout. A quick analysis yields the following:
```
[canary]            rbp-24
0x0000000000000000  rbp-32
0x82BB489CBF50E1A1  rbp-40
0xE01922F6C7DD80D4  rbp-48
0x3BF408DB71DDEC66  rbp-56
0xEE3C31DD459B33E8  rbp-64
0x1DEB17D1F5553C3D  rbp-72
0x6787AE145035E46E  rbp-80
..................  rbp-88
0x0000000000000000  rbp-96
0xC3E34692E550E8AA  rbp-104
0x8B4061A7C49FC7B8  rbp-112
0x45CA76A14C8B955C  rbp-120
0xB54A06A329AE5FDF  rbp-128
0x5E9538A3D9225F42  rbp-136
0x08D4EC402F479F0D  rbp-144
[8 bytes of input]  rbp-152
[8 bytes of input]  rbp-160
[8 bytes of input]  rbp-168
[8 bytes of input]  rbp-176
[8 bytes of input]  rbp-184
[8 bytes of input]  rbp-192 <-- base address of input
[8 bytes of flag]   rbp-200
[8 bytes of flag]   rbp-208
[8 bytes of flag]   rbp-216
[8 bytes of flag]   rbp-224
[8 bytes of flag]   rbp-232
[8 bytes of flag]   rbp-240 <-- base address of the flag to be built by .L3
0x0000000000000000  rbp-244 <-- Loop iterator, loop [0, 48) (terminate at 48)
```
The first section of the disassembly is more or less entirely setup for the meat of the program, ending by reading in user input to `$rbp-192`, initializing the loop iterator at `$rbp-244` to 0, and jumping to section `.L2`. We can check out `.L2` next:
```
.L2:
	movl	-244(%rbp), %eax
	movslq	%eax, %rbx
	leaq	-144(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT          <-- strlen(constants)
	cmpq	%rax, %rbx
	jb	.L3

	leaq	-240(%rbp), %rcx
	leaq	-192(%rbp), %rax
	movl	$48, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	memcmp@PLT          <-- memcmp(input, flag)
	testl	%eax, %eax
	je	.L4

	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	movl	$0, %eax
	jmp	.L6
```
The first part of `.L2` seems to be the loop condition - while the loop iterator (`rbp-244`) is less than strlen(`rbp-144`), jump to `.L3`. `rbp-144` contains the first half of the loaded constants, which are 48 bytes total. So we loop while `i < 48`. Let's skip to looking at `.L3` since it'll make the rest of `.L2` make more sense.
```
.L3:
	movl	-244(%rbp), %eax
	cltq
	movzbl	-144(%rbp,%rax), %edx   <-- edx = constants_part_1[i]
	movl	-244(%rbp), %eax
	cltq
	movzbl	-80(%rbp,%rax), %eax    <-- eax = constants_part_2[i]

	xorl	%eax, %edx          <-- edx = constants_part_2[i] ^ constants_part_1[i]
	movl	-244(%rbp), %eax    <-- eax = i
	xorl	%edx, %eax          <-- eax = constants_part_2[i] ^ constants_part_1[i] ^ i
	xorl	$19, %eax           <-- eax = eax ^ 19
	movl	%eax, %edx          <-- edx = eax
	movl	-244(%rbp), %eax    <-- eax = i
	cltq
	movb	%dl, -240(%rbp,%rax)    <-- flag[i] = edx
	addl	$1, -244(%rbp)          <-- i++
```
This is where the constants are modified into the flag as described by the annotations. For each value of the iterator `i`:
```
flag[i] = constants_part_2[i] ^ constants_part_1[i] ^ i ^ 19
```
`.L3` is basically just the loop logic for building the flag at `rbp-240` which is then passed into a call to `memcpy` in `.L2` that compares your input with the flag that was built. The rest of the program just tells you if you were correct or not.
- Side note: Yeah as the challenge name suggests, running the code would just show us the flag at `rbp-240` at some point which is much easier than static reversing
```
$ python3 let\'s-get-dynamic.py 
hammy{u win - hammy}
```
## Solution
1. Load up all the constants into two lists. You can do it by copying the code below, or manually separating them into individual bytes which makes the next step easier.
```py
constants_part_1 = [
    0x08D4EC402F479F0D,
    0x5E9538A3D9225F42,
    0xB54A06A329AE5FDF,
    0x45CA76A14C8B955C,
    0x8B4061A7C49FC7B8,
    0xC3E34692E550E8AA
]

constants_part_2 = [
    0x6787AE145035E46E,
    0x1DEB17D1F5553C3D,
    0xEE3C31DD459B33E8,
    0x3BF408DB71DDEC66,
    0xE01922F6C7DD80D4,
    0x82BB489CBF50E1A1
]
```
2. Iterate over all 48 byte indices of the constant lists and perform the following on each index:
```
flag[i] = constants_part_2[i] ^ constants_part_1[i] ^ i ^ 19
```

## Key Takeaways
Another pretty good introduction to reverse engineering mistakenly placed in the hard category
