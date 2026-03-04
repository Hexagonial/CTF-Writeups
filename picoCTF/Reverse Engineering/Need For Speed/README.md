# Need For Speed
Challenge Description:
> The name of the game is speed. Are you quick enough to solve this problem and keep it above 50 mph?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What is the final key?
</details>

## Procedure
When the binary is run, a timer seems to be set. An expensive computation runs and gets cutoff halfway by the timer, ending the program.
```
$ ./need-for-speed 
Keep this thing over 50 mph!
============================

Creating key...
Not fast enough. BOOM!
```
Let's open the program up in gdb and see what's going on in `main`.
```
gef➤  disass main
Dump of assembler code for function main:
   0x000000000000139c <+0>:	endbr64 
   0x00000000000013a0 <+4>:	push   rbp
   0x00000000000013a1 <+5>:	mov    rbp,rsp
   0x00000000000013a4 <+8>:	sub    rsp,0x10
   0x00000000000013a8 <+12>:	mov    DWORD PTR [rbp-0x4],edi
   0x00000000000013ab <+15>:	mov    QWORD PTR [rbp-0x10],rsi
   0x00000000000013af <+19>:	mov    eax,0x0
   0x00000000000013b4 <+24>:	call   0x1356 <header>
   0x00000000000013b9 <+29>:	mov    eax,0x0
   0x00000000000013be <+34>:	call   0x12a1 <set_timer>
   0x00000000000013c3 <+39>:	mov    eax,0x0
   0x00000000000013c8 <+44>:	call   0x12f3 <get_key>
   0x00000000000013cd <+49>:	mov    eax,0x0
   0x00000000000013d2 <+54>:	call   0x1326 <print_flag>
   0x00000000000013d7 <+59>:	mov    eax,0x0
   0x00000000000013dc <+64>:	leave  
   0x00000000000013dd <+65>:	ret    
End of assembler dump.
```
`set_timer` might be setting up the timer that ends the program. Let's put a breakpoint at `*main+29` and skip over the call to `set_timer`.
```
gef➤  b *main+29
Breakpoint 1 at 0x13b9
gef➤  r
Keep this thing over 50 mph!
============================
[#0] Id 1, Name: "need-for-speed", stopped 0x62939dfc13b9 in main (), reason: BREAKPOINT
...
   0x62939dfc13ab <main+000f>      mov    QWORD PTR [rbp-0x10], rsi
   0x62939dfc13af <main+0013>      mov    eax, 0x0
   0x62939dfc13b4 <main+0018>      call   0x62939dfc1356 <header>
 → 0x62939dfc13b9 <main+001d>      mov    eax, 0x0
   0x62939dfc13be <main+0022>      call   0x62939dfc12a1 <set_timer>
   0x62939dfc13c3 <main+0027>      mov    eax, 0x0
   0x62939dfc13c8 <main+002c>      call   0x62939dfc12f3 <get_key>
   0x62939dfc13cd <main+0031>      mov    eax, 0x0
   0x62939dfc13d2 <main+0036>      call   0x62939dfc1326 <print_flag>
──────────────────────────────────────────────────────────────────────────
gef➤  set $rip=0x62939dfc13c3
gef➤  c
Continuing.
Creating key...
Finished
Printing flag:
hammy{u win- hammy}
```
Cool, we get the flag for skipping over the timer setup 

## Solution
1. Open the program in gdb.
2. Set a breakpoint before the call to `set_timer` in `main`.
3. When the breakpoint is hit, `set $rip=` to the address of the instruction just after the call to `set_timer` to skip over it.
4. Continue the program to get the flag.

## Key Takeaways
The intended solution is probably to discover the value of the key (which isn't very hard), skip over the call to `calculate_key`, and set `rdi` to the value of the key before the call to `decrypt_flag`. But why skip over `calculate_key` when we can skip over `set_timer`...
```
gef➤  disass calculate_key
Dump of assembler code for function calculate_key:
   0x000062939dfc125b <+0>:	endbr64 
   0x000062939dfc125f <+4>:	push   rbp
   0x000062939dfc1260 <+5>:	mov    rbp,rsp
   0x000062939dfc1263 <+8>:	mov    DWORD PTR [rbp-0x4],0xbd187fda
   0x000062939dfc126a <+15>:	sub    DWORD PTR [rbp-0x4],0x1
   0x000062939dfc126e <+19>:	cmp    DWORD PTR [rbp-0x4],0xde8c3fed   <--- the final key value
   0x000062939dfc1275 <+26>:	jne    0x62939dfc126a <calculate_key+15>
   0x000062939dfc1277 <+28>:	mov    eax,DWORD PTR [rbp-0x4]
   0x000062939dfc127a <+31>:	pop    rbp
   0x000062939dfc127b <+32>:	ret    
End of assembler dump.
```
