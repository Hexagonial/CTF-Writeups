# Secure Password Database
Challenge Description:
> I made a new password authentication program that even shows you the password you entered saved in the database! Isn't that cool?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>200</b>
<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> How does the hashing algorithm work?
</details>

## Procedure
From a quick look in BinaryNinja, the program asks you for the password (as well as its length), and then asks you to input its hash. If you can calculate your own password's hash, you get the flag.
```
0040168c            if (make_secret(&var_e5) != rax_30)
00401734                free(rax_2)
00401739                result = 0
0040168c            else
004016a6                int64_t rax_34 = fopen("flag.txt", &data_4020f9)
```
Since no obfuscation is done to your input or the flag, you can just dynamically reverse the program in gdb to get the expected secret value for a given password. Here's what the expected hash value is for a password that's just a newline and 1 byte long:
```
Please set a password for your account:

How many bytes in length is your password?
1
You entered: 1
Your successfully stored password:
10 0 
```
```
→ 0x57c5f021c672 <main+02a2>      call   0x57c5f021c35e <make_secret>
...
gef➤  ni
0x000057c5f021c677 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
──── registers ────
$rax   : 0xd3770d6251b31be2
```
The expected hash for a password that's just 1 byte `\n` is 0xd3770d6251b31be2 = 15237662580160011234.

```
Please set a password for your account:

How many bytes in length is your password?
1
You entered: 1
Your successfully stored password:
10 0 
Enter your hash to access your account!
15237662580160011234
hammy{u win - hammy}
```

## Solution
1. Enter just a newline for your password.
2. Set your password to be 1 byte long.
3. Enter `15237662580160011234` for the hash.
