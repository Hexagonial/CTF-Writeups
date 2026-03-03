# picoCTF - Easy Reverse Engineering Problems

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Easy-Medium</b>

## Navigation
This is a collection of solutions for the reverse engineering problems whose solutions are concise enough to not warrant needing their own writeup.
1. [ASCII FTW](#ascii-ftw)
2. [bloat.py](#bloatpy)
2. [crackme-py](#crackme-py)
3. [FactCheck](#factcheck)
4. [Fresh Java](#fresh-java)
21. [keygenme-py](#keygenme-py)
4. [patchme.py](#patchmepy)
4. [Reverse](#reverse)
5. [Safe Opener](#safe-opener)
    - [Safe Opener](#safe-opener-1)
    - [Safe Opener 2](#safe-opener-2)
5. [Shop](#shop)
5. [timer](#timer)
6. [unpackme.py](#unpackmepy)

## ASCII FTW
If you disassemble `main` in gdb, you can see the flag being loaded character by character. Placing a breakpoint at `*main+151` and examining the contents of `$rsp` shows the flag.
```
   0x0000000000001184 <+27>:	mov    BYTE PTR [rbp-0x30],0x70
   0x0000000000001188 <+31>:	mov    BYTE PTR [rbp-0x2f],0x69
   0x000000000000118c <+35>:	mov    BYTE PTR [rbp-0x2e],0x63
   ...
   0x00000000000011f4 <+139>:	mov    BYTE PTR [rbp-0x14],0x41
   0x00000000000011f8 <+143>:	mov    BYTE PTR [rbp-0x13],0x44
   0x00000000000011fc <+147>:	mov    BYTE PTR [rbp-0x12],0x7d
   0x0000000000001200 <+151>:	movzx  eax,BYTE PTR [rbp-0x30]
```
```
$rsp   : 0x00007ffd22bb48b0  →  "hammy{u win - hammy}"
```

## bloat.py
This function in the source code seems to be performing the check on your input. If you inject a `print` statement you can determine the correct password without having to manually piece it together.
```py
def arg133(arg432):
  # print(a[71]+a[64]+a[79]+a[79]+a[88]+a[66]+a[71]+a[64]+a[77]+a[66]+a[68])
  if arg432 == a[71]+a[64]+a[79]+a[79]+a[88]+a[66]+a[71]+a[64]+a[77]+a[66]+a[68]:
    return True
  else:
    print(a[51]+a[71]+a[64]+a[83]+a[94]+a[79]+a[64]+a[82]+a[82]+a[86]+a[78]+\
a[81]+a[67]+a[94]+a[72]+a[82]+a[94]+a[72]+a[77]+a[66]+a[78]+a[81]+\
a[81]+a[68]+a[66]+a[83])
    sys.exit(0)
    return False
```

## crackme-py
Inject your own call to `decode_secret(bezos_cc_secret)` and run the program to get the flag.

## FactCheck
If you step through main (using gef) you can see the flag get built in real time at a stack address. At some point this memory address gets cleared out, so if you try to skip to the end of main it won't be there anymore.
```
0x00007ffd5e0c2760│+0x0010: 0x000058abd6760ed0  →  "hammy{u win - hammy}"	 ← $rax, $rdi
0x00007ffd5e0c2768│+0x0018: 0x0000000000000020 (" "?)
0x00007ffd5e0c2770│+0x0020: 0x000000000000002e ("."?)
0x00007ffd5e0c2778│+0x0028: 0x0000000000000000
0x00007ffd5e0c2780│+0x0030: 0x00007ffd5e0c2790  →  0x000073d90d020030  →  0x000073d90d021468  →  0x000073d90d01dcf0  →  0x000073d90ceaf830  →  <__cxxabiv1::__vmi_class_type_info::~__vmi_class_type_info()+0000> endbr64 
0x00007ffd5e0c2788│+0x0038: 0x0000000000000001
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x58abba27b853 <main+05ca>      mov    esi, 0x7d
   0x58abba27b858 <main+05cf>      mov    rdi, rax
   0x58abba27b85b <main+05d2>      call   0x58abba27b100 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEpLEc@plt>
 → 0x58abba27b860 <main+05d7>      mov    ebx, 0x0
```

## Fresh Java
If you decompile the `.class` file (I used VS Code's `Decompiler` extension), you get a Java file that checks each character of the password to see if it matches the flag's corresponding character.
```java
...
} else if (var2.charAt(6) != 'F') {
    System.out.println("Invalid key");
} else if (var2.charAt(5) != 'T') {
    System.out.println("Invalid key");
} else if (var2.charAt(4) != 'C') {
    System.out.println("Invalid key");
} else if (var2.charAt(3) != 'o') {
    System.out.println("Invalid key");
} else if (var2.charAt(2) != 'c') {
    System.out.println("Invalid key");
} else if (var2.charAt(1) != 'i') {
    System.out.println("Invalid key");
} else if (var2.charAt(0) != 'p') {
    System.out.println("Invalid key");
} else {
    System.out.println("Valid key");
}
```

## keygenme-py
The license key input is checked in `check_key`. More specifically, the license key is the flag (`picoCTF{}` wrapper and all), and `check_key` checks to see if your input is the same length as the flag and that the tail end (the random hex bytes that are typically added to the ends of flags) is as expected. You can inject this print statement at the start of `check_flag` to get the expected value.
```py
print(hashlib.sha256(username_trial).hexdigest()[4]+ \
        hashlib.sha256(username_trial).hexdigest()[5]+ \
        hashlib.sha256(username_trial).hexdigest()[3]+ \
        hashlib.sha256(username_trial).hexdigest()[6]+ \
        hashlib.sha256(username_trial).hexdigest()[2]+ \
        hashlib.sha256(username_trial).hexdigest()[7]+ \
        hashlib.sha256(username_trial).hexdigest()[1]+ \
        hashlib.sha256(username_trial).hexdigest()[8])
```
Replace the `xxxxxxxx` in `picoCTF{1n_7h3_kk3y_of_xxxxxxxx}` with the printed value to get the flag.

## patchme.py
The password can be found in plaintext but broken up in the source code. Just put it back together.
```py
if( user_pw == "ak98" + \
                "-=90" + \
                "adfjhgj321" + \
                "sleuth9000"):
    print("Welcome back... your flag, user:")
```

## Reverse
Using the `strings` command on the binary reveals the flag in plaintext.
```
$ strings ret
...
Enter the password to unlock this file: 
You entered: %s
Password correct, please see flag: hammy{u win - hammy}
```

## Safe Opener
This is a two-part challenge.
### Safe Opener 1
The flag is encoded in base 64 in the given source code (without the `picoCTF{}` wrapper).
```java
public static boolean openSafe(String password) {
    String encodedkey = "cGwzYXMzX2wzdF9tM18xbnQwX3RoM19zYWYz";
    
    if (password.equals(encodedkey)) {
        System.out.println("Sesame open");
        return true;
    }
    else {
        System.out.println("Password is incorrect\n");
        return false;
    }
}
```

### Safe Opener 2
The flag can be found in plaintext if you open the `.class` file in a text editor or use `cat SafeOpener.class`.

## Shop
The program has an integer overflow problem/does not check user input. If you choose to sell an item and choose a negative amount to sell, the negative amount will always be less than the amount you own (any negative number is less than 0) so the sale will be successful.
```
You have 40 coins
	Item		Price	Count
(0) Quiet Quiches	10	12
(1) Average Apple	15	8
(2) Fruitful Flag	100	1
(3) Sell an Item
(4) Exit
Choose an option: 
3
Your inventory
(0) Quiet Quiches	10	0
(1) Average Apple	15	0
(2) Fruitful Flag	100	0
What do you want to sell? 
2
How many?
-1
You have -60 coins
```
If you "sell" enough items such that your balance goes below -2147483648, your balance will overflow to 2147483647 and you can afford the flag. The flag will be given in decimal characters, so you need to convert it to text using an ASCII table.

## timer
If you decompile the APK (I used VS Code's `Decompiler` extension), you find the flag in plaintext in `sources/com/example/timer/BuildConfig.java`.
```java
package com.example.timer;
/* loaded from: classes3.dex */
public final class BuildConfig {
    public static final String APPLICATION_ID = "com.example.timer";
    public static final String BUILD_TYPE = "debug";
    public static final boolean DEBUG = Boolean.parseBoolean("true");
    public static final int VERSION_CODE = 1;
    public static final String VERSION_NAME = "hammy{u win - hammy}";
}
```

## unpackme.py
Replace the `exec` with `print` to see the decrypted source code, which has the flag in plaintext.
```py
payload = b'gAAAAABkzWGWvEp8gLI9AcIn5o-ahDUwkTvM6EwF7YYMZlE-_Gf9rcNYjxIgX4b0ltY6bcxKarib2ds6POclRwCwhsRb1LOXVt4Q3ePtMY4BmHFFZlIHLk05CjwigT7hiI9p3sH9e7Cpk1uO90xbHbuy-mfi3nkmn411aBgwxyWpJvykpkuBIG_nty6zbox3UhbB85TOis0TgM0zG4ht0-GUW4wTq2_5-wkw3kV1ZAisLJHzF-Z9oLMmwFZU0UCAcHaBTGDF5BnVLmUeCGTgzVLSNn6BmB61Yg=='

key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())    # <------- Replace "exec" with "print"
```
```
$ python3 unpackme.flag.py 

pw = input('What\'s the password? ')

if pw == 'batteryhorse':
  print('hammy{u win - hammy}')
else:
  print('That password is incorrect.')
```
