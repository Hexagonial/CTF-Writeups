# Undo
Challenge Description:
> Can you reverse a series of Linux text transformations to recover the original flag?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>100</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> For text translation and character replacement, see tr command documentation.
</details>

## Procedure
This is a short challenge that teaches you the `tr` command.
```
===Welcome to the Text Transformations Challenge!===

Your goal: step by step, recover the original flag.
At each step, you'll see the transformed flag and a hint.
Enter the correct Linux command to reverse the last transformation.

--- Step 1 ---
Current flag: KW5xOW45OG43LWZhMDFnQHplMHNmYTRlRy1nazNnLXRhMWZlcmlyRShTR1BicHZj
Hint: Base64 encoded the string.
Enter the Linux command to reverse it: base64 -d 
Correct!

--- Step 2 ---
Current flag: )nq9n98n7-fa01g@ze0sfa4eG-gk3g-ta1ferirE(SGPbpvc
Hint: Reversed the text.
Enter the Linux command to reverse it: rev
Correct!

--- Step 3 ---
Current flag: cvpbPGS(Eriref1at-g3kg-Ge4afs0ez@g10af-7n89n9qn)
Hint: Replaced underscores with dashes.
Enter the Linux command to reverse it: tr '-' '_'
Correct!

--- Step 4 ---
Current flag: cvpbPGS(Eriref1at_g3kg_Ge4afs0ez@g10af_7n89n9qn)
Hint: Replaced curly braces with parentheses.
Enter the Linux command to reverse it: tr '()' '{}'
Correct!

--- Step 5 ---
Current flag: cvpbPGS{Eriref1at_g3kg_Ge4afs0ez@g10af_7n89n9qn}
Hint: Applied ROT13 to letters.
Enter the Linux command to reverse it: tr '[a-z][A-Z]' '[n-za-m][N-ZA-M]'
Correct!

Congratulations! You've recovered the original flag:
>>> hammy{u win - hammy}
```

## Solution
1. See the procedure
