# Specialer
Challenge Description:
> Reception of Special has been cool to say the least. That's why we made an exclusive version of Special, called Secure Comprehensive Interface for Affecting Linux Empirically Rad, or just 'Specialer'. With Specialer, we really tried to remove the distractions from using a shell. Yes, we took out spell checker because of everybody's complaining. But we think you will be excited about our new, reduced feature set for keeping you focused on what needs it the most. Please start an instance to test your very own copy of Specialer.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What programs do you have access to?
</details>

## Procedure
This and SansAlpha have a similar procedure, but this challenge requires one additional bit of knowledge. When logging into the shell, we find that a lot of commands we are used to cannot be found.
```
Specialer$ ls
-bash: ls: command not found
Specialer$ cat
-bash: cat: command not found
Specialer$ cd
Specialer$ echo
```
Unlike SansAlpha we can thankfully include letters in our commands, and we find two existing commands: `cd` and `echo`. By <b>globbing</b> to probe around the environment, we can find a few directories where we are:
```
Specialer$ ./???? 
-bash: ./abra: Is a directory
Specialer$ ./[!a]???
-bash: ./[!a]???: No such file or directory
Specialer$ ./[!a]*  
-bash: ./sim: Is a directory
Specialer$ ./a[!b]*
-bash: ./ala: Is a directory
Specialer$ ./a[!l]*
-bash: ./abra: Is a directory
Specialer$ ./a[!lb]*
-bash: ./a[!lb]*: No such file or directory
```
After `cd`ing into each of the directories and probing them the same way, we discover that each directory has one or more `.txt` files. We can print the contents of `.txt` files by using `echo`, courtesy of https://stackoverflow.com/questions/22377792/how-to-use-echo-command-to-print-out-content-of-a-text-file 
- `echo "$(<text.txt)"`

The flag can be found in `~/ala/kazam.txt`.
```
Specialer$ echo "$(<kazam.txt)"
return 0 hammy{u win - hammy}
```

## Solution
1. Run this command:
    - `echo "$(<ala/kazam.txt)"`
