# weirdSnake
Challenge Description:
> I have a friend that enjoys coding and he hasn't stopped talking about a snake recently. He left this file on my computer and dares me to uncover a secret phrase from it. Can you assist?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Download and try to reverse the python bytecode.
</details>
<details>
<summary>Hint 2</summary>

> https://docs.python.org/3/library/dis.html
</details>

## Procedure
The link provided in hint 2 (in addition to http://vega.lpl.arizona.edu/python/lib/bytecodes.html) will be invaluable to anyone completely new to reading Python Bytecode instructions (me), so we can refer to that for each instruction. Additionally, we can leverage the `dis` library to write some Python code and see what the corresponding bytecode is to confirm or deny any of our assumptions about the bytecode.
```py
from dis import dis

def test():
    x = 3
    y = 4
    if x < y:
        test1(5)
    else:
        test2(6)

def test1(z):
    pass

def test2(z):
    pass

print(dis(test))
```

Let's begin by analyzing the first section ("line number") of the bytecode. The first section loads 40 constants and stores them in a list called `input_list`.

The next 5 sections perform the following:
- Section 2 loads a constant `'J'` and stores it into `key_str`.
- Section 3 loads a constant `'_'` and prepends it to `key_str` (`key_str = '_' + key_str`).
- Section 4 loads a constant `'o'` and adds it to `key_str` (`key_str = key_str + 'o'`).
- Section 5 loads a constant `'3'` and adds it to `key_str`.
- Section 6 loads a constant `t` and prepends it to `key_str`.

At this point, if we execute sections 2-6 `key_str` holds `t_Jo3`. The next sections perform:
- Section 9 calls `key_list = listcomp(iter(key_str))`. We'll discover what `listcomp` does later.
- Section 11 performs `len(key_list) < len(input_list)` and jumps to address 162 (section 15) if false.
- Section 12 performs `key_list.extend(key_list)` and returns to section 11.
- Section 15 performs `result = listcomp(zip(input_list, key_list))`.
- Section 18 performs `result_text = ''.join(map(chr, result))` and returns NULL.

Now we get to see the disassembly of `listcomp`. Judging from the bytecode containing two disassemblies for `listcomp` at two different addresses, we can assume that `listcomp` is redefined partway through the code. Both versions of `listcomp` take in one argument: an iterator.

The first version of `listcomp` (section 9) is called with a string iterator from the previous section 9: `key_list = listcomp(iter(key_str))`. It initializes an empty list, loads what I assume is the argument iterator, then performs something similar to the following:
```py
result = []
for c in str_iter:
    result.append(ord(c))
return result
```
So it converts every character in `key_str` to its decimal ASCII value and stores the results in a list.

The second version of `listcomp` takes a [zip](https://www.geeksforgeeks.org/python/zip-in-python/) iterator that iterates over the `input_list` and `key_list` lists simultaneously. This version is called in the previous section 15: `result = listcomp(zip(input_list, key_list))`. It also begins by initializing an empty list, retrieiving the argument iterator, and performs the following:
```py
result = []
for list_tuple in iter:
    a = list_tuple[0]
    b = list_tuple[1]
    result.append(a ^ b)
return result
```

The list result of the second call to `listcomp` is used in the previous section 18, where a string is constructed by mapping all the decimal values in the result list to string characters, and concatenating all the characters into the flag.<br>
`result_text = ''.join(map(chr, result))`

Now that we've more or less determined what all the parts of the bytecode do, we can just implement it in Python and get the flag.
```
$ python3 weirdSnake.py 
hammy{u win - hammy}
```

## Solution
1. Determine what each section of the bytecode is doing and then re-implement it in Python. See the procedure.

## Key Takeaways
I learned a lot about Python bytecode, seeing as this was my first dance with it.
