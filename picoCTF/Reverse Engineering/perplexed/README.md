# perplexed
Challenge Description:
> [No description]

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
No hints are provided by the challenge author.

## Procedure
Due to not having a decompiler at the ready I kind of approached this problem in a brute-forcy kind of way and attempted to make sense of the disassembled code myself. You can find all my notes down at the [note dump](#note-dump) section, but it's just a bunch of gibberish.

Opening the program in gdb reveals two functions of interest: `main` and `check`. All `main` does is read in your input and store it in a buffer at `$rbp-0x110` that is zeroed out beforehand, and calls `check` with the input. `check` is probably where all the meat is, so let's disassemble it.
```
main:
0x00000000004013fc <+343>:	lea    rax,[rbp-0x110]
0x0000000000401403 <+350>:	mov    esi,0x100
0x0000000000401408 <+355>:	mov    rdi,rax
0x000000000040140b <+358>:	call   0x401060 <fgets@plt>
0x0000000000401410 <+363>:	lea    rax,[rbp-0x110]
0x0000000000401417 <+370>:	mov    rdi,rax
0x000000000040141a <+373>:	call   0x401156 <check>
```
We can see `check` is called with our input buffer as the first argument. `check` will first check to see if our input is of length 27, failing if not.
```
check:
0x000000000040115f <+9>:	mov    QWORD PTR [rbp-0x58],rdi
0x0000000000401163 <+13>:	mov    rax,QWORD PTR [rbp-0x58]
0x0000000000401167 <+17>:	mov    rdi,rax
0x000000000040116a <+20>:	call   0x401040 <strlen@plt>
0x000000000040116f <+25>:	cmp    rax,0x1b
0x0000000000401173 <+29>:	je     0x40117f <check+41>
0x0000000000401175 <+31>:	mov    eax,0x1
0x000000000040117a <+36>:	jmp    0x40129f <check+329>
0x000000000040117f <+41>:	movabs rax,0x617b2375f81ea7e1
```
After the length check, `check` loads in three constants.
```
0x000000000040117f <+41>:	movabs rax,0x617b2375f81ea7e1
0x0000000000401189 <+51>:	movabs rdx,0xd269df5b5afc9db9
0x0000000000401193 <+61>:	mov    QWORD PTR [rbp-0x50],rax
0x0000000000401197 <+65>:	mov    QWORD PTR [rbp-0x48],rdx
0x000000000040119b <+69>:	movabs rax,0xf467edf4ed1bfed2
0x00000000004011a5 <+79>:	mov    QWORD PTR [rbp-0x41],rax
```
Note that the third constant is loaded at a non-aligned memory address (probably some compiler optimization). The least significant bit `0xd2` will overlap with the second constant's most significant bit `0xd2` at address `$rbp-0x48`, so you can interpret the loading of the third constant like this instead:
```
0x000000000040119b <+69>:	movabs rax,0x00f467edf4ed1bfe
0x00000000004011a5 <+79>:	mov    QWORD PTR [rbp-0x40],rax
```
After analyzing `check`, we can conclude its structure is built from 2 loops in this structure (or at least close to this structure... not sure how accurate my analysis was):
```py
i = 0
j = 0
k = 1
input_iter = 0
while i <= 22:
    while j <= 7:
        ...
        k += 1
        if k == 8:
            k = 1
            input_iter += 1
        j += 1
    i += 1
```
Variable `i` seems to be the iterator over the constants loaded in earlier. The constants earlier total up to 23 bytes. The purposes of `j` and `k` are a lot less clear, however. `j` spans [0, 7] and `k` spans [1, 7] (being auto-reset to 1 upon reaching 8).

The primary check in `check` happens at `check+230` to `check+234` in which `eax` is XORed with `ecx` and we fail if `eax != 0`. Given that `$rbp-0x28` and `$rbp-0x20c` hold `j` and `k` respectively, we can determine what values will be in `eax` and `ecx` by looking at the disassembly from `check+187`.

```
# ecx = (constants[i] & (1 << (7-j))) > 0
0x0000000000401211 <+187>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50] # constants[i]
0x0000000000401216 <+192>:	movsx  eax,al
0x0000000000401219 <+195>:	and    eax,DWORD PTR [rbp-0x28] # 1 << (7-j)
0x000000000040121c <+198>:	test   eax,eax
0x000000000040121e <+200>:	setg   cl

# eax = (input[index] & (1 << (7-k))) > 0
0x0000000000401221 <+203>:	mov    eax,DWORD PTR [rbp-0x14] # The index of the character in our input that we are examining
0x0000000000401224 <+206>:	movsxd rdx,eax
0x0000000000401227 <+209>:	mov    rax,QWORD PTR [rbp-0x58] # Our password input
0x000000000040122b <+213>:	add    rax,rdx                  # rax = input[index]
0x000000000040122e <+216>:	movzx  eax,BYTE PTR [rax]
0x0000000000401231 <+219>:	movsx  eax,al
0x0000000000401234 <+222>:	and    eax,DWORD PTR [rbp-0x2c] # 1 << (7-k)
0x0000000000401237 <+225>:	test   eax,eax
0x0000000000401239 <+227>:	setg   al

# If (eax ^ ecx) != 0, failed
0x000000000040123c <+230>:	xor    eax,ecx
0x000000000040123e <+232>:	test   al,al
0x0000000000401240 <+234>:	je     0x401249 <check+243>
0x0000000000401242 <+236>:	mov    eax,0x1
0x0000000000401247 <+241>:	jmp    0x40129f <check+329>
```
`(constants[i] & (1 << (7-j))) > 0` and `(input[index] & (1 << (7-k))) > 0` are basically checking each bit of the characters `constants[i]` and `input[index]`. So, we are comparing the bits between the constants and the input. The indices of the bits being compared, however, don't seem to match up directly because `j` spans [0, 7] and `k` spans [1, 7]. This means `j` cycles every 8 bits examined, and `k` cycles every 7 bits examined.

My theory of what is happening is the bits of the loaded constants are being compared with the bits of the input password, except skipping the comparison of the most significant bit in each byte of the password. We can test this out using what is probably the first eight characters of the password (`picoCTF{`) and comparing it to the first eight bytes in the constants.
- First eight constant bytes:   `1110000110100111000111101111100001110101001000110111101101100001`
- `picoCTF{`:         `0111000001101001011000110110111101000011010101000100011001111011`

If we line up the binary strings side by side, we get:<br>
`1110000110100111000111101111100001110101001000110111101101100001`<br>
`0111000001101001011000110110111101000011010101000100011001111011`

If we "skip" the most significant bit of each octet in the input string, we get:<br>
`|1110000|1101001|1100011|1101111|1000011|1010100|1000110|1111011|01100001`<br>
`0111000001101001011000110110111101000011010101000100011001111011`

And this seems to line the bits up! Therefore, we can probably extract the flag by:
1. Converting all the constant bytes to binary strings and concatenating all of them
2. Insert a `0` after every 7th bit, starting at the 0th bit (i.e., replace the `|` characters with `0`s in the lineup above)
3. Divide the binary string into octets and convert each octet into an ASCII character

```
$ python3 perplexed.py 
hammy{u win - hammy}
```

## Solution
1. Grab the three constants loaded in `check` and organize their bytes into an array you can iterate over.
```
gef➤  x/23b $rbp-0x50
0x7ffda2a17600:	0xe1	0xa7	0x1e	0xf8	0x75	0x23	0x7b	0x61
0x7ffda2a17608:	0xb9	0x9d	0xfc	0x5a	0x5b	0xdf	0x69	0xd2
0x7ffda2a17610:	0xfe	0x1b	0xed	0xf4	0xed	0x67	0xf4
```
```
[
0xe1, 0xa7, 0x1e, 0xf8, 
0x75, 0x23, 0x7b, 0x61, 
0xb9, 0x9d, 0xfc, 0x5a, 
0x5b, 0xdf, 0x69, 0xd2, 
0xfe, 0x1b, 0xed, 0xf4, 
0xed, 0x67, 0xf4
]
```
2. Convert each byte into binary (8 bits, padded with zeroes if necessary) and concatenate everything into one binary string.
3. Insert a 0 after every 7th bit in the binary string.
    - Then, add a 0 at the start of the binary string.
4. Separate the binary string into octets and convert each octet to an ASCII character for the flag.

## Note Dump
1. Length 27 (including newline)
2. +116 to +318: main loop ([$rbp-0x1c] <= 0x16)
3. +128 to +302: sub loop 1 ([$rbp-0x20] <= 0x7)

Stack

rbp-0x14    0x0     <-- input index counter?
rbp-0x18    0x1     <-- k
rbp-0x1c    0x0     <-- Main loop increment, i <= 0x16
rbp-0x20    0x0     <-- Subloop increment, j <= 0x7
rbp-0x24    0x0
rbp-0x40    0x00f467edf4ed1bfe
rbp-0x48    0xd269df5b5afc9db9
rbp-0x50    0x617b2375f81ea7e1
rbp-0x58    input

```
========== MAIN LOOP ==========
<+116>:	mov    DWORD PTR [rbp-0x20],0x0
<+123>:	jmp    0x401280 <check+298>
---------- SUB LOOP ----------
<+128>:	cmp    DWORD PTR [rbp-0x18],0x0
<+132>:	jne    0x4011e0 <check+138>
<+134>:	add    DWORD PTR [rbp-0x18],0x1
<+138>:	mov    eax,0x7
<+143>:	sub    eax,DWORD PTR [rbp-0x20]     # eax = 7-j
<+146>:	mov    edx,0x1                      # edx = 0x1
<+151>:	mov    ecx,eax                      # ecx = 7-j
<+153>:	shl    edx,cl                       # edx = 1 << (7-j) = 0x80 downto 1
<+155>:	mov    eax,edx                      # eax = 1 << (7-j)
<+157>:	mov    DWORD PTR [rbp-0x28],eax     # rbp-0x28 = 1 << (7-j)

<+160>:	mov    eax,0x7                      # eax = 0x7
<+165>:	sub    eax,DWORD PTR [rbp-0x18]     # eax = 7 - rbp-0x18
<+168>:	mov    edx,0x1                      # edx = 0x1
<+173>:	mov    ecx,eax                      # ecx = 7 - rbp-0x18
<+175>:	shl    edx,cl                       # edx = 1 << (7 - rbp-0x18)
                                            # = 0x40 downto 1?
<+177>:	mov    eax,edx                      # eax = 1 << (7 - rbp-0x18)
<+179>:	mov    DWORD PTR [rbp-0x2c],eax     # rbp-0x2c = 1 << (7 - rbp-0x18)

<+182>:	mov    eax,DWORD PTR [rbp-0x1c]     # eax = i
<+185>:	cdqe                                # sign extend eax -> rax
<+187>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]    # eax = rbp+i-0x50
<+192>:	movsx  eax,al                       # eax = 0xffffff[rbp+i-0x50]
<+195>:	and    eax,DWORD PTR [rbp-0x28]     # eax = eax & (1 << (7-j))
<+198>:	test   eax,eax
<+200>:	setg   cl                           # rcx = eax > 0

<+203>:	mov    eax,DWORD PTR [rbp-0x14]     # eax = currIndex
<+206>:	movsxd rdx,eax                      # rdx = sign extend rbp-0x14
<+209>:	mov    rax,QWORD PTR [rbp-0x58]     # rax = input
<+213>:	add    rax,rdx                      # rax = input[currIndex]

<+216>:	movzx  eax,BYTE PTR [rax]           
<+219>:	movsx  eax,al                       # eax = current character value

<+222>:	and    eax,DWORD PTR [rbp-0x2c]     # eax = eax & (1 << (7 - rbp-0x18))
<+225>:	test   eax,eax
<+227>:	setg   al                           # eax = eax > 0

# 0xffffff[rbp+i-0x50] & (1 << (7-j)) ^ input[currIndex] & (1 << (7 - rbp-0x18))
# must = 0, otherwise failed check
<+230>:	xor    eax,ecx
<+232>:	test   al,al
<+234>:	je     0x401249 <check+243>
<+236>:	mov    eax,0x1
<+241>:	jmp    0x40129f <check+329>

If rbp-0x18 += 1 == 0x8:
    rbp-0x18 = 0
    currIndex += 1
<+243>:	add    DWORD PTR [rbp-0x18],0x1
<+247>:	cmp    DWORD PTR [rbp-0x18],0x8
<+251>:	jne    0x40125e <check+264>
<+253>:	mov    DWORD PTR [rbp-0x18],0x0
<+260>:	add    DWORD PTR [rbp-0x14],0x1

if we have iterated over all chars in input:
    check = True
<+264>:	mov    eax,DWORD PTR [rbp-0x14] # eax = currIndex
<+267>:	movsxd rbx,eax                  # rbx = currIndex
<+270>:	mov    rax,QWORD PTR [rbp-0x58] 
<+274>:	mov    rdi,rax
<+277>:	call   0x401040 <strlen@plt>
<+282>:	cmp    rbx,rax
<+285>:	jne    0x40127c <check+294>
<+287>:	mov    eax,0x0
<+292>:	jmp    0x40129f <check+329>

<+294>:	add    DWORD PTR [rbp-0x20],0x1 # j += 1

<+298>:	cmp    DWORD PTR [rbp-0x20],0x7 
<+302>:	jle    0x4011d6 <check+128>     # if j <= 7 restart subloop
--------------------

if i <= 0x16 restart main loop
0x000000000040128a <+308>:	add    DWORD PTR [rbp-0x1c],0x1
0x000000000040128e <+312>:	mov    eax,DWORD PTR [rbp-0x1c]
0x0000000000401291 <+315>:	cmp    eax,0x16
0x0000000000401294 <+318>:	jbe    0x4011ca <check+116>
====================

0x000000000040129a <+324>:	mov    eax,0x0
0x000000000040129f <+329>:	mov    rbx,QWORD PTR [rbp-0x8]
0x00000000004012a3 <+333>:	leave  
0x00000000004012a4 <+334>:	ret  
```
```
i = $rbp-0x1c
j = $rbp-0x20
k = $rbp-0x18
inputIndex=  $rbp-0x14

expected = {
0xe1	0xa7	0x1e	0xf8	0x75	0x23	0x7b	0x61
0xb9	0x9d	0xfc	0x5a	0x5b	0xdf	0x69	0xd2
0xfe	0x1b	0xed	0xf4	0xed	0x67	0xf4
}

input = picoCTF{aaaaaaaaaaaaaaaaaa}
0xe7 =   11100001
p = 	01110000

expected    =  X1110000|1101001|1100011|1101111|1000011|1010100|1000110|1111011|01100001
input       =  01110000011010010110001101101111010000110101010001000110

if (strlen(input) != 27) return False;

int k = 1;
for (int i = 0; i <= 22; i++) {
	for (int j = 0; j <= 7; j++) {
		var2 = 1 << (7-k);
		
		expectedBool = (expected[i] & (1 << (7-j))) > 0;
		inputBool = (input[inputIndex] & (1 << (7-k))) > 0;
		
		if (expectedBool ^ inputBool) return False;
		
		k++;
		if (k == 8) {
			k = 1;
			inputIndex++;
		}
		
		if (strlen(input) == inputIndex) return True;
	}
}
```