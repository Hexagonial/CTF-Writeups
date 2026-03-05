# OTP Implementation
Challenge Description:
> Yay reversing!

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html
</details>
<details>
<summary>Hint 2</summary>

> I think GDB Python is very useful, you can solve this problem without it, but can you solve future problems (hint hint)?
</details>
<details>
<summary>Hint 3</summary>

> Also test your skills by solving this with ANGR!
</details>

<br>And a hint from me in case you need it.
<details>
<summary>Hint 4</summary>

> If you're not sure if your key is correct, you can always just give it to the program and it'll tell you. What exactly you need to do with the correct key might be unclear at first so using the program for a sanity check helps.
</details>

## Procedure
"OTP" from the challenge title is most likely referring to "one time pad." This program most likely checks to see if your input "key" is equivalent to the one-time pad used to generate `enc_flag.txt`. If OTP in fact refers to one-time pad, we can assume our key must be 100 bytes long since that's how long the encrypted flag is. Let's begin by looking at `main`. Everything before `main+88` is for checking if you supplied the key as an argument (checks if argc > 1), so we can ignore everything before `main+88`.
```
0x0000613e9d400866 <+88>:	mov    rax,QWORD PTR [rbp-0x100]
0x0000613e9d40086d <+95>:	add    rax,0x8
0x0000613e9d400871 <+99>:	mov    rcx,QWORD PTR [rax]
0x0000613e9d400874 <+102>:	lea    rax,[rbp-0xe0]
0x0000613e9d40087b <+109>:	mov    edx,0x64
0x0000613e9d400880 <+114>:	mov    rsi,rcx
0x0000613e9d400883 <+117>:	mov    rdi,rax
0x0000613e9d400886 <+120>:	call   0x613e9d400620 <strncpy@plt> <-- strncpy($rbp-0xe0, argv[1], 100)
0x0000613e9d40088b <+125>:	mov    BYTE PTR [rbp-0x7c],0x0
0x0000613e9d40088f <+129>:	mov    DWORD PTR [rbp-0xe8],0x0
0x0000613e9d400899 <+139>:	jmp    0x613e9d40093c <main+302>
```
Ok, maybe we can't entirely ignore everything before `main+88`. argv, which is stored in `$rsi` in the call to `main`, is stored at `$rbp-0x100`. The first notable thing that seems to happen in `main` is a call to `strncpy($rbp-0xe0, argv[1], 100)`, copying at most 100 bytes from `argv[1]` (our argument-supplied key) to a buffer at `$rbp-0xe0`. Immediately after the call to `strncpy` the buffer is surrounded with null bytes at `$rbp-0x7c` (which is 100 bytes from `$rbp-0xe0`) and `$rbp-0xe8` (8 bytes below the buffer). We then jump to `main+302`:
```
0x0000613e9d40093c <+302>:	mov    eax,DWORD PTR [rbp-0xe8]         <-- eax = i
0x0000613e9d400942 <+308>:	cdqe   
0x0000613e9d400944 <+310>:	movzx  eax,BYTE PTR [rbp+rax*1-0xe0]    <-- eax = input_buffer[i]
0x0000613e9d40094c <+318>:	movsx  eax,al
0x0000613e9d40094f <+321>:	mov    edi,eax
0x0000613e9d400951 <+323>:	call   0x613e9d40078a <valid_char>      <-- valid_char(input_buffer[i])
0x0000613e9d400956 <+328>:	test   eax,eax
0x0000613e9d400958 <+330>:	jne    0x613e9d40089e <main+144>        <-- Loop if valid_char returns nonzero
0x0000613e9d40095e <+336>:	mov    DWORD PTR [rbp-0xe4],0x0
0x0000613e9d400968 <+346>:	jmp    0x613e9d40098f <main+385>
```
Judging from the instruction at `+310`, the value stored at `$rbp-0xe8` looks like an iterator/index over our buffer. The instructions from `+302` to `+323` set up a call to `valid_char(input_buffer[i])`, whose return value is checked. If the return value is nonzero, we jump back to the start of the loop at `main+144`. Otherwise, we break out of the loop. Let's see what `valid_char` does. 

### valid_char
`valid_char` is called with `input_buffer[i]` as the only argument in `$rdi`.
```
0x0000613e9d40078a <+0>:	push   rbp
0x0000613e9d40078b <+1>:	mov    rbp,rsp
0x0000613e9d40078e <+4>:	mov    eax,edi
0x0000613e9d400790 <+6>:	mov    BYTE PTR [rbp-0x4],al            <-- rbp-0x4 = input_buffer[i]
0x0000613e9d400793 <+9>:	cmp    BYTE PTR [rbp-0x4],0x2f
0x0000613e9d400797 <+13>:	jle    0x613e9d4007a6 <valid_char+28>   <-- Jump if input_buffer[i] <= 0x2f (/)
0x0000613e9d400799 <+15>:	cmp    BYTE PTR [rbp-0x4],0x39
0x0000613e9d40079d <+19>:	jg     0x613e9d4007a6 <valid_char+28>   <-- Jump if input_buffer[i] > 0x39 (9)

0x0000613e9d40079f <+21>:	mov    eax,0x1
0x0000613e9d4007a4 <+26>:	jmp    0x613e9d4007be <valid_char+52>   <-- If 0x30 <= input_buffer[i]  <= 0x39 (i.e., input_buffer[i] is a digit) return 1

# If reaching here, input_buffer[i] <= 0x2f OR input_buffer[i] > 0x39
0x0000613e9d4007a6 <+28>:	cmp    BYTE PTR [rbp-0x4],0x60
0x0000613e9d4007aa <+32>:	jle    0x613e9d4007b9 <valid_char+47>   <-- If 0x39 < input_buffer[i] <= 0x60 (`), return 0
0x0000613e9d4007ac <+34>:	cmp    BYTE PTR [rbp-0x4],0x66
0x0000613e9d4007b0 <+38>:	jg     0x613e9d4007b9 <valid_char+47>   <-- If input_buffer[i] > 0x66 (f), return 0
0x0000613e9d4007b2 <+40>:	mov    eax,0x1
0x0000613e9d4007b7 <+45>:	jmp    0x613e9d4007be <valid_char+52>   <-- If 0x61 <= input_buffer[i] <= 0x66, return 1
0x0000613e9d4007b9 <+47>:	mov    eax,0x0
0x0000613e9d4007be <+52>:	pop    rbp
0x0000613e9d4007bf <+53>:	ret 
```
There are two conditions in which `valid_char` returns 1:
1. 0x30 <= `input_buffer[i]`  <= 0x39
    - I.e., `input_buffer[i]` is a digit
2. 0x61 <= `input_buffer[i]` <= 0x66
    - I.e., `input_buffer[i]` is a letter between a-f

Therefore we can deduce that `valid_char` checks if `input_buffer[i]` is a valid (lowercase) hexadecimal digit.

Now that we know what `valid_char` does, let's examine the inner workings of the loop at `main+144`.

### main+144
We jump to `main+144` if the call to `valid_char(input_buffer[i])` returns 1 (i.e., `input_buffer[i]` is a valid hexadecimal digit).
```
0x0000613e9d40089e <+144>:	cmp    DWORD PTR [rbp-0xe8],0x0
0x0000613e9d4008a5 <+151>:	jne    0x613e9d4008e4 <main+214>        <-- Jump if i != 0
0x0000613e9d4008a7 <+153>:	mov    eax,DWORD PTR [rbp-0xe8]         
0x0000613e9d4008ad <+159>:	cdqe   
0x0000613e9d4008af <+161>:	movzx  eax,BYTE PTR [rbp+rax*1-0xe0]    <-- eax = input_buffer[i]
0x0000613e9d4008b7 <+169>:	movsx  eax,al
0x0000613e9d4008ba <+172>:	mov    edi,eax
0x0000613e9d4008bc <+174>:	call   0x613e9d4007c0 <jumble>          <-- jumble(input_buffer[i])
```
When `i == 0`, the first part of the loop sets up a call to `jumble(input_buffer[i])`. Let's check out what `jumble` does to our input, I'm sure it will be fun !

### jumble
`jumble` is called with `input_buffer[i]` as the only argument in `$rdi`.
```
0x0000613e9d4007c0 <+0>:	push   rbp
0x0000613e9d4007c1 <+1>:	mov    rbp,rsp
0x0000613e9d4007c4 <+4>:	mov    eax,edi
0x0000613e9d4007c6 <+6>:	mov    BYTE PTR [rbp-0x4],al
0x0000613e9d4007c9 <+9>:	cmp    BYTE PTR [rbp-0x4],0x60
0x0000613e9d4007cd <+13>:	jle    0x613e9d4007d9 <jumble+25>   <-- Jump if input_buffer[i] is a digit
0x0000613e9d4007cf <+15>:	movzx  eax,BYTE PTR [rbp-0x4]
0x0000613e9d4007d3 <+19>:	add    eax,0x9                      <-- If input_buffer[i] is a-f, add 9 to it
0x0000613e9d4007d6 <+22>:	mov    BYTE PTR [rbp-0x4],al
0x0000613e9d4007d9 <+25>:	movzx  eax,BYTE PTR [rbp-0x4]
0x0000613e9d4007dd <+29>:	mov    edx,eax
0x0000613e9d4007df <+31>:	sar    dl,0x7
0x0000613e9d4007e2 <+34>:	shr    dl,0x4                       <-- edx = 0
0x0000613e9d4007e5 <+37>:	add    eax,edx                  
0x0000613e9d4007e7 <+39>:	and    eax,0xf                      
0x0000613e9d4007ea <+42>:	sub    eax,edx                      <-- eax = input_buffer[i] & 0xf
0x0000613e9d4007ec <+44>:	mov    BYTE PTR [rbp-0x4],al                  i.e., ord(input_buffer[i])
0x0000613e9d4007ef <+47>:	movsx  eax,BYTE PTR [rbp-0x4]
0x0000613e9d4007f3 <+51>:	add    eax,eax                      
0x0000613e9d4007f5 <+53>:	mov    BYTE PTR [rbp-0x4],al        <-- rbp-0x4 = (eax + eax)
0x0000613e9d4007f8 <+56>:	cmp    BYTE PTR [rbp-0x4],0xf
0x0000613e9d4007fc <+60>:	jle    0x613e9d400808 <jumble+72>   <-- Return eax + eax if it's <= 0xf
0x0000613e9d4007fe <+62>:	movzx  eax,BYTE PTR [rbp-0x4]   
0x0000613e9d400802 <+66>:	add    eax,0x1
0x0000613e9d400805 <+69>:	mov    BYTE PTR [rbp-0x4],al        <-- Else, return ((eax + eax) & 0xff)+1
0x0000613e9d400808 <+72>:	movzx  eax,BYTE PTR [rbp-0x4]
0x0000613e9d40080c <+76>:	pop    rbp
0x0000613e9d40080d <+77>:	ret   
```
Therefore, jumble returns a value according to these rules:
- If `2 * (ord(input_buffer[i])) <= 0xf`, return `2 * (ord(input_buffer[i]))`
    - Values 0-7 will return `2 * (ord(input_buffer[i]))`
- Else, return `2 * (ord(input_buffer[i])) + 1`
    - Values 8-f will return `2 * (ord(input_buffer[i])) + 1`

### main+144, continued
```
0x0000613e9d4008c1 <+179>:	mov    edx,eax                          <-- edx = jumble(input_buffer[i])
0x0000613e9d4008c3 <+181>:	mov    eax,edx
0x0000613e9d4008c5 <+183>:	sar    al,0x7
0x0000613e9d4008c8 <+186>:	shr    al,0x4                           <-- eax = 0
0x0000613e9d4008cb <+189>:	add    edx,eax                          <-- edx = jumble(input_buffer[i])
0x0000613e9d4008cd <+191>:	and    edx,0xf                          <-- edx = jumble(input_buffer[i]) & 0xf
0x0000613e9d4008d0 <+194>:	sub    edx,eax
0x0000613e9d4008d2 <+196>:	mov    eax,edx
0x0000613e9d4008d4 <+198>:	mov    edx,eax
0x0000613e9d4008d6 <+200>:	mov    eax,DWORD PTR [rbp-0xe8]         <-- eax = i
0x0000613e9d4008dc <+206>:	cdqe   
0x0000613e9d4008de <+208>:	mov    BYTE PTR [rbp+rax*1-0x70],dl     <-- mystery[i] = jumble(input_buffer[i]) & 0xf
0x0000613e9d4008e2 <+212>:	jmp    0x613e9d400935 <main+295>        <-- i++, reloop
...
0x0000613e9d400935 <+295>:	add    DWORD PTR [rbp-0xe8],0x1
0x0000613e9d40093c <+302>:	mov    eax,DWORD PTR [rbp-0xe8]
0x0000613e9d400942 <+308>:	cdqe   
0x0000613e9d400944 <+310>:	movzx  eax,BYTE PTR [rbp+rax*1-0xe0]
0x0000613e9d40094c <+318>:	movsx  eax,al
0x0000613e9d40094f <+321>:	mov    edi,eax
0x0000613e9d400951 <+323>:	call   0x613e9d40078a <valid_char>
```
The result of the call to `jumble(input_buffer[i])` is ANDed with `0xf` and stored in a buffer at `rbp-0x70`. We don't know what this buffer is yet so I'll just call it `mystery`.

### main+214
If we are in this part of the loop, `i >= 1` and `mystery[0] = jumble(input_buffer[0]) & 0xf`.
```
0x0000613e9d4008e4 <+214>:	mov    eax,DWORD PTR [rbp-0xe8]
0x0000613e9d4008ea <+220>:	cdqe   
0x0000613e9d4008ec <+222>:	movzx  eax,BYTE PTR [rbp+rax*1-0xe0]    <-- eax = input_buffer[i]
0x0000613e9d4008f4 <+230>:	movsx  eax,al
0x0000613e9d4008f7 <+233>:	mov    edi,eax
0x0000613e9d4008f9 <+235>:	call   0x613e9d4007c0 <jumble>
0x0000613e9d4008fe <+240>:	movsx  edx,al                           <-- edx = jumble(input_buffer[i])
0x0000613e9d400901 <+243>:	mov    eax,DWORD PTR [rbp-0xe8]
0x0000613e9d400907 <+249>:	sub    eax,0x1                          <-- eax = i-1
0x0000613e9d40090a <+252>:	cdqe   
0x0000613e9d40090c <+254>:	movzx  eax,BYTE PTR [rbp+rax*1-0x70]    <-- eax = mystery[i-1]
0x0000613e9d400911 <+259>:	movsx  eax,al
0x0000613e9d400914 <+262>:	add    edx,eax                          <-- edx = jumble(input_buffer[i])+mystery[i-1]
0x0000613e9d400916 <+264>:	mov    eax,edx                          
0x0000613e9d400918 <+266>:	sar    eax,0x1f
0x0000613e9d40091b <+269>:	shr    eax,0x1c                         <-- eax = 0
0x0000613e9d40091e <+272>:	add    edx,eax                          
0x0000613e9d400920 <+274>:	and    edx,0xf                          <-- edx = jumble(input_buffer[i])+mystery[i-1] & 0xf
0x0000613e9d400923 <+277>:	sub    edx,eax
0x0000613e9d400925 <+279>:	mov    eax,edx
0x0000613e9d400927 <+281>:	mov    edx,eax
0x0000613e9d400929 <+283>:	mov    eax,DWORD PTR [rbp-0xe8]         <-- eax = i
0x0000613e9d40092f <+289>:	cdqe   
0x0000613e9d400931 <+291>:	mov    BYTE PTR [rbp+rax*1-0x70],dl     <-- mystery[i] = jumble(input_buffer[i])+mystery[i-1] & 0xf
# i++ and reloop
```
When the loop terminates, `mystery` will be filled with the following contents:
1. `mystery[0] = jumble(input_buffer[0]) & 0xf`
2. `mystery[i] = jumble(input_buffer[i])+mystery[i-1] & 0xf` for i > 0

### main+336
At this point, the loop has terminated since `input_buffer[i]` is no longer a valid hexadecimal digit (whether it's because the input key contains an invalid hex digit or because we reached the end of it). It looks like we start another loop here.
```
0x00005e0e3120095e <+336>:	mov    DWORD PTR [rbp-0xe4],0x0         <-- j = 0
0x00005e0e31200968 <+346>:	jmp    0x5e0e3120098f <main+385>
0x00005e0e3120096a <+348>:	mov    eax,DWORD PTR [rbp-0xe4]     
0x00005e0e31200970 <+354>:	cdqe   
0x00005e0e31200972 <+356>:	movzx  eax,BYTE PTR [rbp+rax*1-0x70]    <-- eax = mystery[j]
0x00005e0e31200977 <+361>:	add    eax,0x61                         <-- eax = mystery[j] + 0x61
0x00005e0e3120097a <+364>:	mov    edx,eax                          <-- edx = mystery[j] + 0x61
0x00005e0e3120097c <+366>:	mov    eax,DWORD PTR [rbp-0xe4]         <-- eax = j
0x00005e0e31200982 <+372>:	cdqe   
0x00005e0e31200984 <+374>:	mov    BYTE PTR [rbp+rax*1-0x70],dl     <-- mystery[j] += 0x61 
0x00005e0e31200988 <+378>:	add    DWORD PTR [rbp-0xe4],0x1         <-- j++
0x00005e0e3120098f <+385>:	mov    eax,DWORD PTR [rbp-0xe4]
0x00005e0e31200995 <+391>:	cmp    eax,DWORD PTR [rbp-0xe8]
0x00005e0e3120099b <+397>:	jl     0x5e0e3120096a <main+348>        <-- while j < i, loop
```
All the loop does is add `0x61` to all elements of `mystery`, probably to turn hexadecimal digits into readable lowercase letters.

### The Rest of main
The rest of the program seems to perform a check on the contents of `mystery` against a hardcoded `expected` value of mystery:
```
0x00005e0e3120099d <+399>:	cmp    DWORD PTR [rbp-0xe8],0x64
0x00005e0e312009a4 <+406>:	jne    0x5e0e312009c6 <main+440>                <-- If i != 100, invalid key
0x00005e0e312009a6 <+408>:	mov    eax,DWORD PTR [rbp-0xe8]
0x00005e0e312009ac <+414>:	movsxd rdx,eax
0x00005e0e312009af <+417>:	lea    rax,[rbp-0x70]
0x00005e0e312009b3 <+421>:	lea    rsi,[rip+0xe6]        # 0x5e0e31200aa0
0x00005e0e312009ba <+428>:	mov    rdi,rax
0x00005e0e312009bd <+431>:	call   0x5e0e31200630 <strncmp@plt>             <-- Compare mystery with expected
0x00005e0e312009c2 <+436>:	test   eax,eax
0x00005e0e312009c4 <+438>:	je     0x5e0e312009d9 <main+459>                <-- If mystery = expected, correct key
0x00005e0e312009c6 <+440>:	lea    rdi,[rip+0x138]        # 0x5e0e31200b05
0x00005e0e312009cd <+447>:	call   0x5e0e31200640 <puts@plt>
0x00005e0e312009d2 <+452>:	mov    eax,0x1
0x00005e0e312009d7 <+457>:	jmp    0x5e0e312009ea <main+476>
0x00005e0e312009d9 <+459>:	lea    rdi,[rip+0x138]        # 0x5e0e31200b18
0x00005e0e312009e0 <+466>:	call   0x5e0e31200640 <puts@plt>
...
gef➤  x/s 0x5e0e31200aa0
0x5e0e31200aa0:	"pnbopoejdmapflhkefabijeajpcijdniefahigichdmhekgohnhdkfdjbgapnhndlcbeglloaogkokbiffbhomgpminjpgieieme"
gef➤  x/s 0x5e0e31200b05
0x5e0e31200b05:	"Invalid key!"
gef➤  x/s 0x5e0e31200b18
0x5e0e31200b18:	"You got the key, congrats! Now xor it with the flag!"
```

We know `expected = pnbopoejdmapflhkefabijeajpcijdniefahigichdmhekgohnhdkfdjbgapnhndlcbeglloaogkokbiffbhomgpminjpgieieme`, we know how `mystery` is generated, now all that's left is to reverse `expected` to get the key. I.e., `expected` holds the state of `mystery` at the end of `main` when the input buffer holds the key.
```
$ python3 otp-implementation.py 
Key: hammy's key
Flag: hammy{u win - hammy}
```

## Solution
1. Read the procedure and/or look at the script. Too many words to summarize in a short solution section

## Key Takeaways
Another relatively easy (but still tedious) reversing problem, and a reasonable step up from the easier problems like reverse_cipher and Let's get dynamic. There were some strange shift instructions that I don't know the purpose of (the `sar` and `shr` instructions), the amount they shifted guaranteed the result would always be 0.

perplexed, despite being rated Medium, would be a good next challenge to solve in this progression.