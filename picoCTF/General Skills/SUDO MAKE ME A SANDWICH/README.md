# SUDO MAKE ME A SANDWICH
Challenge Description:
> Can you read the flag? I think you can!

CTF: <b>picoCTF 2026</b><br>Points: <b>50</b><br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What is sudo?
</details>
<details>
<summary>Hint 2</summary>

> How do you know what permission you have?
</details>

## Procedure
When logged into the server, running `ls -l` shows a file `flag.txt` that is owned and only readable by `root`.
```
ctf-player@challenge:~$ ls -l
total 4
-r--r----- 1 root root 31 Mar  9 21:32 flag.txt
```
Running `sudo -l` shows we have privileges to run `emacs` as root.
```
ctf-player@challenge:~$ sudo -l
Matching Defaults entries for ctf-player on challenge:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User ctf-player may run the following commands on challenge:
    (ALL) NOPASSWD: /bin/emacs
```
We can escalate privileges to read `flag.txt` by:
1. Run `sudo /bin/emacs`
2. Move your cursor over `Visit New File` and press Enter
3. Finish the file path at the bottom of the screen to be `/home/ctf-player/flag.txt`

## Solution
1. Run `sudo /bin/emacs`
2. Move your cursor over `Visit New File` and press Enter
3. Finish the file path at the bottom of the screen to be `/home/ctf-player/flag.txt`

