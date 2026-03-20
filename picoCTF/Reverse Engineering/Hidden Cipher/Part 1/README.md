# Hidden Cipher 1
Challenge Description:
> The flag is right in front of you; just slightly encrypted. All you have to do is figure out the cipher and the key. 

CTF: <b>picoCTF 2026</b><br>Points: <b>100</b><br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> The binary can be unpacked using a tool that's often pre-installed on Linux
</details>
<details>
<summary>Hint 2</summary>

> The program hides a secret. Look at how it's defined and used.
</details>
<details>
<summary>Hint 3</summary>

> Think XOR. What happens when you XOR something twice with the same key?
</details>

## Procedure
The first thing we notice when opening the program in gdb is that nothing is listed when running `info func`. This is a sign that the binary is possibly packed in some way, and when running `checksec` we can see it's packed with UPX.
```
$ checksec hiddencipher
[!] Did not find any GOT entries
    Arch:       amd64-64-little
    RELRO:      No RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Packer:     Packed with UPX
```
So the first thing we can do is unpack it with `upx -d` and try again.
```
$ upx -d hiddencipher 
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2026
UPX 5.1.1       Markus Oberhumer, Laszlo Molnar & John Reiser    Mar 5th 2026

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
     16568 <-      7196   43.43%   linux/amd64   hiddencipher

Unpacked 1 file.
```
```
gef➤  info func
All defined functions:

Non-debugging symbols:
0x0000000000001000  _init
0x00000000000011c0  _start
0x00000000000011f0  deregister_tm_clones
0x0000000000001220  register_tm_clones
0x0000000000001260  __do_global_dtors_aux
0x00000000000012a0  frame_dummy
0x00000000000012a9  get_secret
0x00000000000012eb  main
0x000000000000148c  _fini
```

Now we can start by analyzing main section-by-section. The binary still has unnamed code addresses which obfuscate some parts, but we can easy infer what the functions are based on their static arguments. For the ones we can't infer, we can set a breakpoint in gdb at their callsites and see where it takes us:
```
gef➤  x/3i 0x555555555170
   0x555555555170:	endbr64 
   0x555555555174:	jmp    QWORD PTR [rip+0x2e36]        # 0x555555557fb0 <ftell@got.plt>
   0x55555555517a:	nop    WORD PTR [rax+rax*1+0x0]
gef➤  x/3i 0x555555555190
   0x555555555190:	endbr64 
   0x555555555194:	jmp    QWORD PTR [rip+0x2e26]        # 0x555555557fc0 <fseek@got.plt>
   0x55555555519a:	nop    WORD PTR [rax+rax*1+0x0]
gef➤  x/3i 0x5555555551a0
   0x5555555551a0:	endbr64 
   0x5555555551a4:	jmp    QWORD PTR [rip+0x2e1e]        # 0x555555557fc8 <fopen@got.plt>
   0x5555555551aa:	nop    WORD PTR [rax+rax*1+0x0]
```
```
gef➤  disas main
Dump of assembler code for function main:
   0x00005555555552eb <+0>:	endbr64 
   0x00005555555552ef <+4>:	push   rbp
   0x00005555555552f0 <+5>:	mov    rbp,rsp
   0x00005555555552f3 <+8>:	sub    rsp,0x30
   0x00005555555552f7 <+12>:	lea    rdx,[rip+0xd06]        # 0x555555556004 ("rb")
   0x00005555555552fe <+19>:	lea    rax,[rip+0xd02]        # 0x555555556007 ("flag.txt")
   0x0000555555555305 <+26>:	mov    rsi,rdx
   0x0000555555555308 <+29>:	mov    rdi,rax
   0x000055555555530b <+32>:	call   0x5555555551a0       <-- fopen("flag.txt", "rb")
   0x0000555555555310 <+37>:	mov    QWORD PTR [rbp-0x20],rax
   0x0000555555555314 <+41>:	cmp    QWORD PTR [rbp-0x20],0x0
   0x0000555555555319 <+46>:	jne    0x555555555334 <main+73>

   0x000055555555531b <+48>:	lea    rax,[rip+0xcee]        #  ("[!] Failed to open flag.txt")
   0x0000555555555322 <+55>:	mov    rdi,rax
   0x0000555555555325 <+58>:	call   0x5555555551b0       <-- Most likely a call to puts or printf
   0x000055555555532a <+63>:	mov    eax,0x1
   0x000055555555532f <+68>:	jmp    0x55555555548a <main+415>

   0x0000555555555334 <+73>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000555555555338 <+77>:	mov    edx,0x2
   0x000055555555533d <+82>:	mov    esi,0x0
   0x0000555555555342 <+87>:	mov    rdi,rax
   0x0000555555555345 <+90>:	call   0x555555555190       <-- fseek(flag.txt, 0, 0x2), probably move to the end of the file

   0x000055555555534a <+95>:	mov    rax,QWORD PTR [rbp-0x20]
   0x000055555555534e <+99>:	mov    rdi,rax
   0x0000555555555351 <+102>:	call   0x555555555170       <-- ftell(flag.txt), gives the length of the file after the previous fseek
   0x0000555555555356 <+107>:	mov    QWORD PTR [rbp-0x18],rax

   0x000055555555535a <+111>:	mov    rax,QWORD PTR [rbp-0x20]
   0x000055555555535e <+115>:	mov    rdi,rax
   0x0000555555555361 <+118>:	call   0x555555555160       <-- Call to rewind() to reset flag.txt's file pointer to 0

   0x0000555555555366 <+123>:	mov    rax,QWORD PTR [rbp-0x18]
   0x000055555555536a <+127>:	add    rax,0x1
   0x000055555555536e <+131>:	mov    rdi,rax
   0x0000555555555371 <+134>:	call   0x555555555180           <-- Most likely a call to malloc or some other memory allocation function
   0x0000555555555376 <+139>:	mov    QWORD PTR [rbp-0x10],rax
   0x000055555555537a <+143>:	cmp    QWORD PTR [rbp-0x10],0x0
   0x000055555555537f <+148>:	jne    0x5555555553a6 <main+187>

   # Only reach here if we get an error allocating memory.
   0x0000555555555381 <+150>:	lea    rax,[rip+0xca4]        # 0x55555555602c (""[!] Memory allocation error."")
   0x0000555555555388 <+157>:	mov    rdi,rax
   0x000055555555538b <+160>:	call   0x555555555120       <-- Most likely a call to puts or printf

   # Close the file flag.txt
   0x0000555555555390 <+165>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000555555555394 <+169>:	mov    rdi,rax
   0x0000555555555397 <+172>:	call   0x555555555140       <-- fclose
   0x000055555555539c <+177>:	mov    eax,0x1
   0x00005555555553a1 <+182>:	jmp    0x55555555548a <main+415>

   0x00005555555553a6 <+187>:	mov    rdx,QWORD PTR [rbp-0x18]
   0x00005555555553aa <+191>:	mov    rcx,QWORD PTR [rbp-0x20]
   0x00005555555553ae <+195>:	mov    rax,QWORD PTR [rbp-0x10]
   0x00005555555553b2 <+199>:	mov    esi,0x1
   0x00005555555553b7 <+204>:	mov    rdi,rax
   0x00005555555553ba <+207>:	call   0x555555555130   <-- fread(allocated buffer, length of flag.txt, length of flag.txt)

   0x00005555555553bf <+212>:	mov    rax,QWORD PTR [rbp-0x20]
   0x00005555555553c3 <+216>:	mov    rdi,rax
   0x00005555555553c6 <+219>:	call   0x555555555140   <-- fclose(flag.txt)

   0x00005555555553cb <+224>:	mov    rdx,QWORD PTR [rbp-0x18]
   0x00005555555553cf <+228>:	mov    rax,QWORD PTR [rbp-0x10]
   0x00005555555553d3 <+232>:	add    rax,rdx
   0x00005555555553d6 <+235>:	mov    BYTE PTR [rax],0x0   <-- null-terminate the allocated buffer containing the contents of flag.txt
   0x00005555555553d9 <+238>:	call   0x5555555552a9 <get_secret>
   0x00005555555553de <+243>:	mov    QWORD PTR [rbp-0x8],rax  <-- "S3Cr3t"
```
The first section of `main` simply reads in flag.txt and copies its contents to a dynamically allocated buffer. It finishes by calling `get_secret` which always returns a string `S3Cr3t`.

The rest of main is where the "encryption" happens:
```
0x00005555555553e2 <+247>:	lea    rax,[rip+0xc60]        # 0x555555556049 ("Here your encrypted flag:")
0x00005555555553e9 <+254>:	mov    rdi,rax
0x00005555555553ec <+257>:	call   0x555555555120           <-- puts

# Loop initialization: i = 0
0x00005555555553f1 <+262>:	mov    DWORD PTR [rbp-0x24],0x0
0x00005555555553f8 <+269>:	jmp    0x555555555464 <main+377>

# The loop
    0x00005555555553fa <+271>:	mov    eax,DWORD PTR [rbp-0x24] 
    0x00005555555553fd <+274>:	movsxd rdx,eax                      rdx = i
    0x0000555555555400 <+277>:	mov    rax,QWORD PTR [rbp-0x10]
    0x0000555555555404 <+281>:	add    rax,rdx                      rax = &buffer+i
    0x0000555555555407 <+284>:	movzx  esi,BYTE PTR [rax]           esi = buffer[i]
    0x000055555555540a <+287>:	mov    ecx,DWORD PTR [rbp-0x24]     ecx = i
    0x000055555555540d <+290>:	movsxd rax,ecx                      
    0x0000555555555410 <+293>:	imul   rax,rax,0x2aaaaaab           
    0x0000555555555417 <+300>:	shr    rax,0x20
    0x000055555555541b <+304>:	mov    rdx,rax                  rdx = rax = i * 0x2aaaaaab >> 32 
    0x000055555555541e <+307>:	mov    eax,ecx                  
    0x0000555555555420 <+309>:	sar    eax,0x1f                 eax = i >> 31
    0x0000555555555423 <+312>:	sub    edx,eax                  rdx = rax = i * 0x2aaaaaab >> 32 - (i >> 31)
    0x0000555555555425 <+314>:	mov    eax,edx                  eax = edx
    0x0000555555555427 <+316>:	add    eax,eax                  eax = 2 * edx
    0x0000555555555429 <+318>:	add    eax,edx                  eax = 3 * edx
    0x000055555555542b <+320>:	add    eax,eax                  eax = 6 * edx
    0x000055555555542d <+322>:	sub    ecx,eax                  
    0x000055555555542f <+324>:	mov    edx,ecx
    0x0000555555555431 <+326>:	movsxd rdx,edx                  rdx = ecx = i - 6 * edx (= i % 6)
    0x0000555555555434 <+329>:	mov    rax,QWORD PTR [rbp-0x8]
    0x0000555555555438 <+333>:	add    rax,rdx                  rax = "S3Cr3t"[i%6]
    0x000055555555543b <+336>:	movzx  eax,BYTE PTR [rax]
    0x000055555555543e <+339>:	xor    eax,esi                  eax = "S3Cr3t"[i%6] ^ buffer[i] 
    0x0000555555555440 <+341>:	mov    BYTE PTR [rbp-0x25],al
    0x0000555555555443 <+344>:	movzx  eax,BYTE PTR [rbp-0x25]
    0x0000555555555447 <+348>:	movzx  eax,al
    0x000055555555544a <+351>:	lea    rdx,[rip+0xc12]        # 0x555555556063 ("%02x")
    0x0000555555555451 <+358>:	mov    esi,eax                  esi = ("S3Cr3t" + rdx) ^ buffer[i]
    0x0000555555555453 <+360>:	mov    rdi,rdx
    0x0000555555555456 <+363>:	mov    eax,0x0
    0x000055555555545b <+368>:	call   0x555555555150         <-- printf("%02x, ("S3Cr3t" + rdx) ^ buffer[i])

    # i += 1
    0x0000555555555460 <+373>:	add    DWORD PTR [rbp-0x24],0x1

# Loop boolean: If i < len(flag.txt), loop
0x0000555555555464 <+377>:	mov    eax,DWORD PTR [rbp-0x24]
0x0000555555555467 <+380>:	cdqe   
0x0000555555555469 <+382>:	cmp    QWORD PTR [rbp-0x18],rax
0x000055555555546d <+386>:	jg     0x5555555553fa <main+271>

... cleanup ...
```
The key to how the cipher works is determining what the value of `rdx` holds in relation to `i`. By setting a breakpoint at `*main+329` and observing the value of `rdx` as we execute, it seems to hold `i%6`. Therefore, `encrypted_flag[i] = flag[i] ^ secret[i%6]`.
```
$ python3 hiddencipher1.py 
hammy{u win - hammy}
```

## Solution
1. flag[i] = encrypted_flag[i] % secret[i%6]
    - secret = `S3Cr3t`

## Key Takeaways
From this challenge (and its second part), I've now discovered that modulus operations like the be compiled into weird multiplication/shift operations. Right now I'm still unsure of how the math works but one day I'll figure it out
