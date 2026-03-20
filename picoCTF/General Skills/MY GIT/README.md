# MY GIT
Challenge Description:
> I have built my own Git server with my own rules!

CTF: <b>picoCTF 2026</b>
<br>Points: <b>50</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> How do you specify your Git username and email?
</details>

## Procedure
Cloning the repository and reading README.md shows:
```
$ cat README.md 
# MyGit

### If you want the flag, make sure to push the flag!

Only flag.txt pushed by ```root:root@picoctf``` will be updated with the flag.

GOOD LUCK!
```

Our task is to push a file `flag.txt` as `root:root@picoctf`. In the `challenge` directory, can use the following sequence of commands for this:
```
$ touch flag.txt
$ git add flag.txt
$ git commit --author="root <root@picoctf>"
$ git push
git@foggy-cliff.picoctf.net's password: 
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 4 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 297 bytes | 297.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: Author matched and flag.txt found in commit...
remote: Congratulations! You have successfully impersonated the root user
remote: Here's your flag: hammy{u win - hammy}
```

## Solution
```
$ touch flag.txt
$ git add flag.txt
$ git commit --author="root <root@picoctf>"
$ git push
```

## Key Takeaways
