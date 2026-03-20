# Piece by Piece
Challenge Description:
> After logging in, you will find multiple file parts in your home directory. These parts need to be combined and extracted to reveal the flag.

CTF: <b>picoCTF 2026</b>
<br>Points: <b>50</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
No hints are provided by the challenge author.

## Procedure
Reading `instructions.txt` tells us the flag was originally stored in a single zip file, which was split into multiple parts.
```
ctf-player@pico-chall$ ls -a
.   .cache    instructions.txt	part_ab  part_ad
..  .profile  part_aa		part_ac  part_ae
ctf-player@pico-chall$ cat instructions.txt 
Hint:

- The flag is split into multiple parts as a zipped file.
- Use Linux commands to combine the parts into one file.
- The zip file is password protected. Use this "supersecret" password to extract the zip file.
- After unzipping, check the extracted text file for the flag.
```

We can piece the zip file back together using `>>` (append) in combination with `cat`. There's probably a much better/easier way but this is the first way I thought of. The password for the zip file is as stated in instructions.txt.
```
$ mv part_aa flag.zip
ctf-player@pico-chall$ cat part_ab >> flag.zip
ctf-player@pico-chall$ cat part_ac >> flag.zip
ctf-player@pico-chall$ cat part_ad >> flag.zip
ctf-player@pico-chall$ cat part_ae >> flag.zip 
ctf-player@pico-chall$ unzip flag.zip
Archive:  flag.zip
[flag.zip] flag.txt password: 
 extracting: flag.txt                
ctf-player@pico-chall$ cat flag.txt
hammy{u win - hammy}
```

## Solution
1. Run the following commands. The password is `supersecret` as stated in `instructions.txt`.
```
$ mv part_aa flag.zip
ctf-player@pico-chall$ cat part_ab >> flag.zip
ctf-player@pico-chall$ cat part_ac >> flag.zip
ctf-player@pico-chall$ cat part_ad >> flag.zip
ctf-player@pico-chall$ cat part_ae >> flag.zip 
ctf-player@pico-chall$ unzip flag.zip
Archive:  flag.zip
[flag.zip] flag.txt password: 
 extracting: flag.txt                
ctf-player@pico-chall$ cat flag.txt
```

## Key Takeaways
You can also use globbing to piece the zip back together in one line since globbing parses files in lexicographic order.
```
cat part_* > flag.zip
```

