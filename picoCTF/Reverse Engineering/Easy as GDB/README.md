# Easy as GDB
Challenge Description:
> The flag has got to be checked somewhere...

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Hard</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> https://sourceware.org/gdb/onlinedocs/gdb/Basic-Python.html#Basic-Python
</details>
<details>
<summary>Hint 2</summary>

> With GDB Python, I can guess wrong flags faster than ever before!
</details>

## Procedure
The hints really point you in the right direction for this challenge. Unlike most of the other challenges I've solved, this one is definitely not meant to be manually reversed in full, and is a much more hostile version of the OTP Implementation challenge. Trying to reverse all the obscure functions will take forever, so we need a different approach.

Combining the hints, the challenge title, and the binary name (brute), the intended approach is likely to brute force the flag by finding where the (mutated) input is checked against the (mutated) flag.

When opening the binary in gdb the locations and names of all the functions are hidden. It will be easier to analyze in a decompiler like BinaryNinja. If we take a look at the decompilation of `main` (which I have replaced the placeholder names for most symbols here), we can see the input we give undergoes a series of mutations and then is checked in some function at the end of `main`.
```c
int32_t main(int32_t argc, char** argv, char** envp)

    void* const __return_addr_1 = __return_addr
    int32_t* var_10 = &argc
    char* buf = calloc(n: 0x200, elem_size: 1)
    printf("input the flag: ")
    fgets(buf, 0x200, *stdin)
    size_t _0x1e = strnlen("z.nh", 0x200)  // Result is 0x1e
    char* mutated_buf = sus1(buf, _0x1e)
    sus2(mutated_buf, _0x1e, 1)
    
    if (check(mutated_buf, _0x1e) != 1)
        puts(str: "Incorrect.")
    else
        puts(str: "Correct!")
    
    return 0
```
BinaryNinja misinterprets the argument to the call to `strnlen` as being `z.nh` when it's really some string of characters 30 bytes long. The 5th character is probably some non-text character so both gdb and BinaryNinja cut off their guess at what the string is there.

The function `sus1` and `sus2` put your input through a series of crazy mutations (including cutting it off at ~33 bytes long) that, upon analyzing them for a bit, are clearly not meant to be reversed or worth reversing. The only thing we need to take away from observing these mutations is that they don't perform any transposing. That is, changing one byte of your input only causes its corresponding byte in the mutation to be affected. This will make brute-forcing the flag much more viable.

Let's take a closer look at the `check` function. It's called with the semi-final mutation of our input after it's run through `sus1` and `sus2`.
```c
int32_t check(char* mutated_buf, size_t _0x1e)

    char* final_mutated_buf = calloc(n: _0x1e + 1, elem_size: 1)
    strncpy(final_mutated_buf, mutated_buf, _0x1e)
    sus2(final_mutated_buf, _0x1e, 0xffffffff)
    char* expected_mutation = calloc(n: _0x1e + 1, elem_size: 1)
    strncpy(expected_mutation, "z.nh", _0x1e)
    sus2(expected_mutation, _0x1e, 0xffffffff)
    puts(str: "checking solution...")
    
    for (void* i = nullptr; i u< _0x1e; i += 1)
        if (*(i + final_mutated_buf) != *(i + expected_mutation))
            return 0xffffffff
    
    return 1
```
`check` makes two final mutations to our input by cutting it off at a length of 30 bytes and running it through `sus2` one last time for good measure. Then, it loads the expected mutation (i.e., what the flag turns into when put through all the same mutations as our input) and compares it to our input's final mutation. If they match, we have the flag. The corresponding disassembly for the comparison in the `if` statement is as follows:
```
0x56555978: mov    edx, DWORD PTR [ebp-0x10]
0x5655597b:	mov    eax,DWORD PTR [ebp-0x14]
0x5655597e:	add    eax,edx
0x56555980:	movzx  edx,BYTE PTR [eax]
0x56555983:	mov    ecx,DWORD PTR [ebp-0xc]
0x56555986:	mov    eax,DWORD PTR [ebp-0x14]
0x56555989:	add    eax,ecx
0x5655598b:	movzx  eax,BYTE PTR [eax]
0x5655598e:	cmp    dl,al
```
The instruction at address `0x5655598e` makes the ultimate comparison between corresponding indices of the mutations. At this address we can read in the values of `$al` and `$dl` and compare them - if they are different, we guessed this particular character of our input incorrectly. Else, we are correct and we can assume this character is part of the flag.

Thanks to gdb's `set disable-randomization on` feature, we can have all addresses be static across all runs, making brute-forcing a lot easier. The plan of attack is as follows:
- For each index <i>i</i> of the flag:
    - For each possible character guess <i>c</i> (ASCII values 32 to 126):
        - Set a breakpoint at address `0x5655598e`
        - Execute the program with the input `[known flag characters][c]`
        - Ignore <i>i</i> hits of the breakpoint. On the <i>i</i>th hit:
            - Check the values of registers `$al` and `$dl`
            - If they match, <i>c</i> is a correct guess and is part of the flag.

We can brute-force the flag's value using gdb's Python API. After a TON of wrestling with the API and trying to get things to work, the working script is in `easy-as-gdb.py`. It is run with `gdb -q -x easy-as-gdb.py brute`.

## Solution
1. Brute-force the flag by leveraging gdb's Python API to examine the registers at the check at `0x5655598e` (ensuring that gdb is disabling adress randomization)

## Key Takeaways
This was my first tussle with the gdb Python API, and it seems useful. I'll probably go re-solve OTP Implementation using the Python API as an exercise