# Hidden Cipher 2
Challenge Description:
> The flag is right in front of you... kind of. You just need to solve a basic math problem to see it. But to get the real flag, you’ll have to understand how that math answer is used.

CTF: <b>picoCTF 2026</b>
<br>Points: <b>100</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Focus on what the program does with your correct answer. Is it reused later?
</details>
<details>
<summary>Hint 2</summary>

> Disassembling or decompiling tools (Ghidra, IDA) can help reveal the exact transformation on the flag.
</details>

## Procedure
I got lazy and spun up BinaryNinja right from the get go and kind of regret it because (as Hint 2 suggests) it just tells you the answer. It actually makes things a lot easier to understand since apparently modulus operations get compiled into some crazy multiplication/shift amalgamations.

When running the program, it asks you for the answer to a math question and then prints some encoded flag values. Both the question and encoded values change every run so we can guess that the encoded values depend on the math question somehow.
```
$ nc crystal-peak.picoctf.net 49354
What is 1 + 6? 7
Encoded flag values:
784, 735, 693, 777, 469, 588, 490, 861, 763, 364, 812, 728, 665, 686, 357, 728, 343, 770, 700, 665, 693, 343, 784, 728, 357, 798, 665, 714, 399, 350, 714, 392, 336, 357, 707, 875
```

If we look at decompiled `main`, we can see that it generates a math question, asks you for the answer, and seemingly passes the correct answer into `encode_flag`.
```
00401674        char var_29
00401674        int32_t var_28
00401674        int32_t var_24
00401674        int32_t correct_answer = generate_math_question(&var_29, &var_28, &var_24)
00401697        printf(format: "What is %d %c %d? ", zx.q(var_28), zx.q(sx.d(var_29)), zx.q(var_24))
004016a6        fflush(fp: __TMC_END__)
004016c9        int32_t input_answer
004016c9        int32_t result
004016c9        
004016c9        if (__isoc23_scanf(&data_40201d, &input_answer, &data_40201d) != 1)
004016d5            puts(str: "Invalid input. Exiting.")
004016da            result = 1
004016c9        else if (correct_answer == input_answer)
00401709            void* flag_buf = read_flag_file("flag.txt")
00401709            
00401717            if (flag_buf != 0)
0040172c                encode_flag(flag_buf, correct_answer)
```

`encode_flag` simply prints out each character of the flag, multiplied by the correct answer.
```
0040149c    int64_t encode_flag(void* flag_buf, int32_t correct_answer)

004014b9        puts(str: "Encoded flag values:")
004014be        int32_t i = 0
004014be        
00401535        while (*(flag_buf + sx.q(i)) != 0)
004014ef            printf(format: "%d", zx.q(sx.d(*(flag_buf + sx.q(i))) * correct_answer), 
004014ef                &data_40201d)
004014ef            
00401509            if (*(flag_buf + sx.q(i) + 1) != 0)
0040151a                printf(format: ", ")
0040151a            
0040151f            i += 1
0040151f        
00401543        return putchar(c: 0xa)
```

Therefore all we need to do is divide all the encoded flag values by the answer, and convert the results to text.
```
$ python3 hiddencipher2.py 
hammy{u win - hammy}
```

## Solution
1. Divide all the encoded flag values by the correct answer to the math problem, then convert the results to text.
