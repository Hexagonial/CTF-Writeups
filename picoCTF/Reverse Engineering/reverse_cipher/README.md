# reverse_cipher
Challenge Description:
> We have recovered a binary and a text file. Can you reverse the flag.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> objdump and Gihdra are some tools that could assist with this
</details>

## Procedure
As always, we can begin by running the binary just to see if it gives any hints for its behavior. After creating a flag file with `hammy{u win - hammy}` in the directory and running it, the program exits without a word and creates an empty `rev_this` file. We can assume the program is supposed to encrypt the flag somehow and write the ciphertext to `rev_this` but something went wrong. Let's disassemble `main` and see what it's doing.
```
gef➤  disass main
Dump of assembler code for function main:
   ...
   0x0000638b0fa181e1 <+92>:	mov    rdx,QWORD PTR [rbp-0x18]
   0x0000638b0fa181e5 <+96>:	lea    rax,[rbp-0x50]
   0x0000638b0fa181e9 <+100>:	mov    rcx,rdx
   0x0000638b0fa181ec <+103>:	mov    edx,0x1
   0x0000638b0fa181f1 <+108>:	mov    esi,0x18
   0x0000638b0fa181f6 <+113>:	mov    rdi,rax
   0x0000638b0fa181f9 <+116>:	call   0x638b0fa18040 <fread@plt>
   0x0000638b0fa181fe <+121>:	mov    DWORD PTR [rbp-0x24],eax
   0x0000638b0fa18201 <+124>:	cmp    DWORD PTR [rbp-0x24],0x0
   0x0000638b0fa18205 <+128>:	jg     0x638b0fa18211 <main+140>
   0x0000638b0fa18207 <+130>:	mov    edi,0x0
   0x0000638b0fa1820c <+135>:	call   0x638b0fa18080 <exit@plt>
```
Everything up until `main+92` is opening the `flag.txt` file for reading and `rev_this` file for appending. The file descriptors are stored at these stack addresses:
- flag.txt: `$rbp-0x18`
- rev_this: `$rbp-0x20`

`main+112` seems to call `fread($rbp-0x50, 0x18, 0x1, $rbp-0x18)`; i.e., `fread(buffer, 24, 1, flag.txt)`. This call to `fread` is attempting to read 24*1 bytes from `flag.txt`. Our current flag has a length less than 24, which is why the program exits without writing anything to `rev_this` as it skips the branch at `main+128` and calls `exit`.
- We can extend our flag to `hammyyy{u win - hammyyy}`, exactly 24 bytes.

The meat of the program seems to be organized into some loops, as we can observe the characteristic `move constant into stack address -> jump to further code address that compares this address to another constant`. Let's look at what appears to be the first loop:
```
0x0000638b0fa18211 <+140>:	mov    DWORD PTR [rbp-0x8],0x0
0x0000638b0fa18218 <+147>:	jmp    0x638b0fa1823d <main+184>
0x0000638b0fa1821a <+149>:	mov    eax,DWORD PTR [rbp-0x8]
0x0000638b0fa1821d <+152>:	cdqe   
0x0000638b0fa1821f <+154>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
0x0000638b0fa18224 <+159>:	mov    BYTE PTR [rbp-0x1],al
0x0000638b0fa18227 <+162>:	movsx  eax,BYTE PTR [rbp-0x1]
0x0000638b0fa1822b <+166>:	mov    rdx,QWORD PTR [rbp-0x20]
0x0000638b0fa1822f <+170>:	mov    rsi,rdx
0x0000638b0fa18232 <+173>:	mov    edi,eax
0x0000638b0fa18234 <+175>:	call   0x638b0fa18060 <fputc@plt>
0x0000638b0fa18239 <+180>:	add    DWORD PTR [rbp-0x8],0x1
0x0000638b0fa1823d <+184>:	cmp    DWORD PTR [rbp-0x8],0x7
0x0000638b0fa18241 <+188>:	jle    0x638b0fa1821a <main+149>
```
We can translate this disassembly to:
```py
result_to_write = ""
for i in range(8):
    char = plaintext_flag[i]
    result_to_write += char
```
So the first loop copies the first 8 characters of the flag without modifying them. This lines up with keeping the opening half of the `picoCTF{` wrapper untouched.

The next loop is:
```
0x0000638b0fa18243 <+190>:	mov    DWORD PTR [rbp-0xc],0x8
0x0000638b0fa1824a <+197>:	jmp    0x638b0fa1828f <main+266>
0x0000638b0fa1824c <+199>:	mov    eax,DWORD PTR [rbp-0xc]
0x0000638b0fa1824f <+202>:	cdqe   
0x0000638b0fa18251 <+204>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
0x0000638b0fa18256 <+209>:	mov    BYTE PTR [rbp-0x1],al
0x0000638b0fa18259 <+212>:	mov    eax,DWORD PTR [rbp-0xc]
0x0000638b0fa1825c <+215>:	and    eax,0x1
0x0000638b0fa1825f <+218>:	test   eax,eax
0x0000638b0fa18261 <+220>:	jne    0x638b0fa1826f <main+234>

0x0000638b0fa18263 <+222>:	movzx  eax,BYTE PTR [rbp-0x1]
0x0000638b0fa18267 <+226>:	add    eax,0x5
0x0000638b0fa1826a <+229>:	mov    BYTE PTR [rbp-0x1],al
0x0000638b0fa1826d <+232>:	jmp    0x638b0fa18279 <main+244>

0x0000638b0fa1826f <+234>:	movzx  eax,BYTE PTR [rbp-0x1]
0x0000638b0fa18273 <+238>:	sub    eax,0x2
0x0000638b0fa18276 <+241>:	mov    BYTE PTR [rbp-0x1],al
0x0000638b0fa18279 <+244>:	movsx  eax,BYTE PTR [rbp-0x1]
0x0000638b0fa1827d <+248>:	mov    rdx,QWORD PTR [rbp-0x20]
0x0000638b0fa18281 <+252>:	mov    rsi,rdx
0x0000638b0fa18284 <+255>:	mov    edi,eax
0x0000638b0fa18286 <+257>:	call   0x638b0fa18060 <fputc@plt>
0x0000638b0fa1828b <+262>:	add    DWORD PTR [rbp-0xc],0x1
0x0000638b0fa1828f <+266>:	cmp    DWORD PTR [rbp-0xc],0x16
0x0000638b0fa18293 <+270>:	jle    0x638b0fa1824c <main+199>
```
This translates to:
```py
for i in range(8, 23):
    char = plaintext_flag[i]
    if i & 1 != 0:
        char = chr(ord(char) - 2)
    else:
        char = chr(ord(char) + 5)
    result_to_write += char
```
The last bit of `main` before closing the file descriptors is:
```
0x0000638b0fa18295 <+272>:	movzx  eax,BYTE PTR [rbp-0x39]
0x0000638b0fa18299 <+276>:	mov    BYTE PTR [rbp-0x1],al
0x0000638b0fa1829c <+279>:	movsx  eax,BYTE PTR [rbp-0x1]
0x0000638b0fa182a0 <+283>:	mov    rdx,QWORD PTR [rbp-0x20]
0x0000638b0fa182a4 <+287>:	mov    rsi,rdx
0x0000638b0fa182a7 <+290>:	mov    edi,eax
0x0000638b0fa182a9 <+292>:	call   0x638b0fa18060 <fputc@plt>
```
Given the plaintext flag sits at `$rbp-0x50`, This translates to:
```py
result_to_write += plaintext_flag[23]
```
This just keeps the closing brace of the flag intact. The only meaningful transformations occur in the second loop, and we've more or less reverse engineered it so we can implement its reverse in a separate script.
```
$ python3 reverse_cipher.py 
hammyyy{u win - hammyyy}
```

## Solution
1. Keep the first 8 characters and the last (flag[23]) character of the flag intact. For the middle 15 characters, use this logic to decrypt it:
```py
for i in range(8, 23):
    char = ciphertext_flag[i]
    if i & 1 != 0:
        char = chr(char + 2)
    else:
        char = chr(char - 5)
    result += char
```

## Key Takeaways
Despite being rated "hard," I think this is one of the best introductions to reverse engineering possible. The program isn't complex and doesn't nest loops (which clutters the disassembly really quickly), letting you analyze it one  chunk at a time. All that's required is an understanding of x86-64 calling convention (which registers store which arguments and what register stores the return value).