# Special
Challenge Description:
> Don't power users get tired of making spelling mistakes in the shell? Not anymore! Enter Special, the Spell Checked Interface for Affecting Linux. Now, every word is properly spelled and capitalized... automatically and behind-the-scenes! Be the first to test Special in beta, and feel free to tell us all about how Special streamlines every development process that you face. When your co-workers see your amazing shell interface, just tell them: That's Special (TM)

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Experiment with different shell syntax
</details>

## Procedure
Upon logging into the target machine, you're greeted with a fairly annoying shell that will auto-capitalize and spellcheck your input before running it. Additionally, absolute paths are restricted.
```
Special$ ls
Is 
sh: 1: Is: not found
Special$ ls -a
Is a 
sh: 1: Is: not found
Special$ cat
Cat 
sh: 1: Cat: not found
Special$ chmod
Child 
sh: 1: Child: not found
Special$ 
Special$ ls
Is 
sh: 1: Is: not found
Special$ ls -a
Is a 
sh: 1: Is: not found
Special$ cat
Cat 
sh: 1: Cat: not found
Special$ chmod
Child 
sh: 1: Child: not found
Special$ /bin/ls
Absolutely not paths like that, please!
```
There are some important things to note about how the shell works.
1. Capitalization is limited to the first character in your input. If the first character cannot be capitalized (e.g. it's a symbol) no change is made to it.
2. Spellcheck seems to ignore any input with too many symbols.
3. Absolute paths are banned, but not relative ones. You can just substitute a leading `/` with `../../../`.

Putting all this together, we can easily run the programs in `/bin` to probe our home directory and print the flag.
```
Special$ ../../../bin/pwd         
../../../bin/pwd 
/home/ctf-player
Special$ ../../../bin/ls ../../../home/ctf-player
../../../bin/ls ../../../home/ctf-player 
blargh
Special$ ../../../bin/ls ../../../home/ctf-player/blargh
../../../bin/ls ../../../home/ctf-player/blargh 
flag.txt
Special$ ../../../bin/cat ../../../home/ctf-player/blargh/flag.txt
../../../bin/cat ../../../home/ctf-player/blargh/flag.txt 
hammy{u win - hammy}
```

## Solution
1. Run this command:
    - `../../../bin/cat ../../../home/ctf-player/blargh/flag.txt`
