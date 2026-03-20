# Autorev 1
Challenge Description:
> You think you can reverse engineer? Let's test out your speed

CTF: <b>picoCTF 2026</b>
<br>Points: <b>200</b>
<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#easy-solution)</b>

## Hints
No hints are provided by the challenge author.

## Procedure

> <b>Okay, in the process of making this write up I have discovered my original solution was overkill and is hopefully the intended solution for an upcoming Autorev 2.</b> Turns out the remote machine (possibly mistakenly) just prints the secret for you to see, making this an introductory pwntools challenge instead of a medium reversing challenge. Here's the writeup anyway.

This challenge requires you to read in 20 binaries (one at a time) and discover the secret value within 1 second. Obviously this is impossible to do by hand, so we need to automate the process somehow.

When connecting to the service, we get the following message:
```
Welcome! I think I'm pretty good at reverse enginnering. There's NO WAY anyone's better than me. Wanna try? I have 20 binaries I'm going to send you and you have 1 second EACH to get the secret in each one. Good luck >:)
[the secret in plaintext for some reason]
Here's the next binary in bytes:
7f454c4602010100000000000000000002003e0001...
...
...000000000000000000000000000000
What's the secret?: 
```
The service gives us the binary in bytes (which we'll have to read in and reconstruct the binary if we want it) and asks us for the secret. You can either just read the secret that it gives you in plaintext for some reason, or take the harder route of reconstructing the binary and extracting the secret from it ! !

To reconstruct the binary, we read in all the given bytes and parse them 2 characters at a time to convert them to actual bytes. Then, the result is written to a file (which should have execute permissions; if not, you need to manually set it).
```py
# Generate the binary by translating the raw bytes into actual bytes and writing to a file.
def generate_binary(raw):
    bin = open("bin", "wb")
    to_write = b""
    for i in range (0, len(raw), 2):
        byte = int(raw[i:i+2], 16).to_bytes(1, "little")
        to_write += byte
    bin.write(to_write)
    bin.close()
```

Once we have a sample binary, we need to reverse it manually so we know the process we need to automate. Opening up the binary in gdb and disassembling main gives us:
```
gef➤  disass main
Dump of assembler code for function main:
   0x0000000000401136 <+0>:	push   rbp
   0x0000000000401137 <+1>:	mov    rbp,rsp
   0x000000000040113a <+4>:	sub    rsp,0x10
   0x000000000040113e <+8>:	mov    DWORD PTR [rbp-0x4],0x965eafd3   <-- secret = 0x965eafd3
   0x0000000000401145 <+15>:	mov    DWORD PTR [rbp-0x8],0x0
   0x000000000040114c <+22>:	mov    edi,0x402010
   0x0000000000401151 <+27>:	call   0x401030 <puts@plt>
   0x0000000000401156 <+32>:	lea    rax,[rbp-0x8]
   0x000000000040115a <+36>:	mov    rsi,rax
   0x000000000040115d <+39>:	mov    edi,0x402023
   0x0000000000401162 <+44>:	mov    eax,0x0
   0x0000000000401167 <+49>:	call   0x401040 <__isoc99_scanf@plt>    <-- scanf("%u", buf)
   0x000000000040116c <+54>:	mov    eax,DWORD PTR [rbp-0x8]
   0x000000000040116f <+57>:	cmp    DWORD PTR [rbp-0x4],eax          <-- Compare buf to the secret
```
The secret is moved into the stack in an instruction at `main+8`. Because the secret is simply a constant, it's most likely baked into the raw instruction bytes. 
```
gef➤  x/7b *main+8
0x40113e <main+8>:	0xc7	0x45	0xfc	0xd3	0xaf	0x5e	0x96
gef➤  x/wx *main+11
0x401141 <main+11>:	0x965eafd3
```
Therefore, we can find the secret by examining 4 bytes at `main+11`.

The plan of attack for each binary is as follows:
1. Read in the binary bytes and reconstruct the binary.
2. Spawn a gdb process and run `x/wx *main+11`, and parse the output to extract the secret.
3. Send the secret.
```
$ python3 autorev-1.py 
Reversing binary #1...
Reversing binary #2...
Reversing binary #3...
Reversing binary #4...
Reversing binary #5...
Reversing binary #6...
Reversing binary #7...
Reversing binary #8...
Reversing binary #9...
Reversing binary #10...
Reversing binary #11...
Reversing binary #12...
Reversing binary #13...
Reversing binary #14...
Reversing binary #15...
Reversing binary #16...
Reversing binary #17...
Reversing binary #18...
Reversing binary #19...
Reversing binary #20...

Woah, how'd you do that??
Here's your flag: hammy{u win - hammy}
```

## Easy Solution
1. The service prints the secret in plaintext before giving you the generated binary. Simply read in the given secret and repeat it for all 20 binaries.
