# M1n10n'5_53cr37
Challenge Description:
> Get ready for a mischievous adventure with your favorite Minions! 🕵️‍♂️💥 They’ve been up to their old tricks, and this time, they've hidden the flag in a devious way within the Android source code. Your task is to channel your inner Minion and dive into the disassembled or decompiled code. Watch out, because these little troublemakers have hidden the flag in multiple sneaky spots or maybe even pulled a fast one and concealed it in the same location! Put on your overalls, grab your magnifying glass, and get cracking. The Minions have left clues, and it's up to you to follow their trail and uncover the flag. Can you outwit these playful pranksters and find their secret? Let the Minion mischief begin!

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Do you know how to disassemble an apk file?
</details>
<details>
<summary>Hint 2 (honestly misleading)</summary>

> Any interesting source files?
</details>

## Procedure
Running the APK on an emulator (which I did not have, and referred to the first portion of another writeup for) gives you an image saying `Look into me my Banana Value is interesting`.

If you `grep` for `banana` in the decompiled APK files, you'll find an interesting value in `resources/res/values/strings.xml`.
```
$ grep -nri 'banana'
minions.apk/resources/res/values/public.xml:3780:    <public type="string" name="Banana" id="0x7f0f0000" />
minions.apk/resources/res/values/strings.xml:3:    <string name="Banana">NBQW23LZPN2SA53JNYQC2IDIMFWW26L5</string>
```
This is a base-32 encoded string that we can just run through a base-32 decoder and get the flag.

## Solution
1. Decompile the APK (I used the VS Code `Decompiler` extension)
2. Find the secret string by grepping for `Banana` in the decompiled apk files.

## Key Takeaways
Sadly I had to refer to the first part of another writeup for my first real lead since I didn't have any Android emulators, but from this challenge I learned of more decompiled APK files that could be of note (`resources/res/values`). Also, this is actually the first time I've run into base 32. I always recognize base 64 through the typical trailing `=` signs, and base 32 seems to share the same indicator with a more limited alphabet.
