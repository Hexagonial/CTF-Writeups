# vault-door Series
Challenge Description:
> Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project. The laboratory is protected by a series of locked vault doors. Each door is controlled by a computer and requires a password to open. Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors, but one of our junior agents obtained the source code for each vault's computer! You will need to read the source code for each level to figure out what the password is for that vault door.

CTF: <b>picoCTF</b> (picoGym)

### Introduction
This is an introductory series of challenges to reading Java code and reversing what it's doing. Since most of the solutions are simple I'm just gonna bundle all of the challenges into one writeup.

All of the challenges have the same format: You input the password (WITH the picoCTF{} wrapper), your input is processed, and if the result of the processing matches what is expected you found the flag. E.g., if the correct password is `picoCTF{hammy_hammy}` then the flag is `picoCTF{hammy_hammy}`.

### Navigation
1. [vault-door-training](#vault-door-training)
2. [vault-door-1](#vault-door-1)
3. [vault-door-3](#vault-door-3)
4. [vault-door-4](#vault-door-4)
5. [vault-door-5](#vault-door-5)
6. [vault-door-6](#vault-door-6)
7. [vault-door-7](#vault-door-7)
8. [vault-door-8](#vault-door-8)

## vault-door-training
The correct password is in plaintext in the source code. All that's left to do is wrap it in the `picoCTF{}` wrapper.
```java
public boolean checkPassword(String password) {
    return password.equals("w4rm1ng_Up_w1tH_jAv4_000AXPNPN0i");
}
```

[Back to Navigation](#navigation)
## vault-door-1
The password check function checks each index of the password to see if it matches the expected value, except it does so out of order. You can either manually piece together the password or write a script to parse this code. Depending on your scripting ability both might take the same amount of time 
```java
public boolean checkPassword(String password) {
    return password.length() == 32 &&
            password.charAt(0)  == 'd' &&
            password.charAt(29) == '7' &&
            password.charAt(4)  == 'r' &&
            password.charAt(2)  == '5' &&
            password.charAt(23) == 'r' &&
            password.charAt(3)  == 'c' &&
            password.charAt(17) == '4' &&
            password.charAt(1)  == '3' &&
            password.charAt(7)  == 'b' &&
            password.charAt(10) == '_' &&
            password.charAt(5)  == '4' &&
            password.charAt(9)  == '3' &&
            password.charAt(11) == 't' &&
            password.charAt(15) == 'c' &&
            password.charAt(8)  == 'l' &&
            password.charAt(12) == 'H' &&
            password.charAt(20) == 'c' &&
            password.charAt(14) == '_' &&
            password.charAt(6)  == 'm' &&
            password.charAt(24) == '5' &&
            password.charAt(18) == 'r' &&
            password.charAt(13) == '3' &&
            password.charAt(19) == '4' &&
            password.charAt(21) == 'T' &&
            password.charAt(16) == 'H' &&
            password.charAt(27) == '4' &&
            password.charAt(30) == '3' &&
            password.charAt(25) == '_' &&
            password.charAt(22) == '3' &&
            password.charAt(28) == 'd' &&
            password.charAt(26) == 'a' &&
            password.charAt(31) == '6';
}
```

[Back to Navigation](#navigation)
## vault-door-3
This password checker takes your input and scrambles it according to the for loops. All the processing involves is direct mapping of input indices to output indices, so the easiest way to find the password is to write a script that takes the expected output and applies the same transformations.
```java
public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    char[] buffer = new char[32];
    int i;
    for (i=0; i<8; i++) {
        buffer[i] = password.charAt(i);
    }
    for (; i<16; i++) {
        buffer[i] = password.charAt(23-i);
    }
    for (; i<32; i+=2) {
        buffer[i] = password.charAt(46-i);
    }
    for (i=31; i>=17; i-=2) {
        buffer[i] = password.charAt(i);
    }
    String s = new String(buffer);
    return s.equals("jU5t_a_sna_3lpm13g64f_u_4_m6r143");
}
```
[Back to Navigation](#navigation)
## vault-door-4
The password check in this part simply encodes the epxected password in different ASCII bases - decimal, hexadecimal, octal, and no encoding. Just using an ASCII table to convert the representations to readable text is enough.
```java
public boolean checkPassword(String password) {
    byte[] passBytes = password.getBytes();
    byte[] myBytes = {
        106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
        0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
        0142, 0131, 0164, 063 , 0163, 0137, 0142, 064 ,
        'e' , '9' , '4' , '3' , 'c' , '3' , 'a' , '0' ,
    };
    for (int i=0; i<32; i++) {
        if (passBytes[i] != myBytes[i]) {
            return false;
        }
    }
    return true;
}
```

[Back to Navigation](#navigation)
## vault-door-5
The password checker first URL encodes the input, then base64 encodes the result of that. Therefore we can just base64 decode the expected result and URL decode the result of that.
```java
public boolean checkPassword(String password) {
    String urlEncoded = urlEncode(password.getBytes());
    String base64Encoded = base64Encode(urlEncoded.getBytes());
    String expected = "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
                    + "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
                    + "JTM0JTVmJTYyJTY1JTM5JTY2JTMxJTMwJTYxJTM0";
    return base64Encoded.equals(expected);
}
```
[Back to Navigation](#navigation)
## vault-door-6
The password check for this part applies XOR operations to a hard-coded array of bytes `myBytes`. Each byte of the input XORed with `0x55` must equal the corresponding value of `myBytes`. If `x ^ y = z` then `z ^ y = x` so we can get the password by XORing all the bytes in `myBytes` with `0x55`.
```java
public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    byte[] passBytes = password.getBytes();
    byte[] myBytes = {
        0x3b, 0x65, 0x21, 0xa , 0x38, 0x0 , 0x36, 0x1d,
        0xa , 0x3d, 0x61, 0x27, 0x11, 0x66, 0x27, 0xa ,
        0x21, 0x1d, 0x61, 0x3b, 0xa , 0x2d, 0x65, 0x27,
        0xa , 0x67, 0x65, 0x67, 0x62, 0x6c, 0x6d, 0x66,
    };
    for (int i=0; i<32; i++) {
        if (((passBytes[i] ^ 0x55) - myBytes[i]) != 0) {
            return false;
        }
    }
    return true;
}
```
[Back to Navigation](#navigation)
## vault-door-7
The password checker in this part converts the 32 byte input into eight 4 byte chunks, and stores the 4 byte chunks as integers. The easiest way to solve this (if doing it by hand) is to convert the decimals to hexadecimal, then from hexadecimal to text by processing 1 byte at a time using an ASCII table or online converter.
```java
public int[] passwordToIntArray(String hex) {
    int[] x = new int[8];
    byte[] hexBytes = hex.getBytes();
    for (int i=0; i<8; i++) {
        x[i] = hexBytes[i*4]   << 24
                | hexBytes[i*4+1] << 16
                | hexBytes[i*4+2] << 8
                | hexBytes[i*4+3];
    }
    return x;
}

public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    int[] x = passwordToIntArray(password);
    return x[0] == 1096770097
        && x[1] == 1952395366
        && x[2] == 1600270708
        && x[3] == 1601398833
        && x[4] == 1716808014
        && x[5] == 1734287392
        && x[6] == 942891831
        && x[7] == 876032566;
}
```
[Back to Navigation](#navigation)
## vault-door-8
Since the source code is "obfuscated" with horrible formatting, it's best to run the code through a code formatter before trying to analyze it. The password checker in this part iterates over every character in the input, scrambling the bits in each character according to `scramble`. The `switchBits` method simply swaps the two bits at positions `p1` and `p2`.

It's easiest to write a script that iterates over each bit of `expected` and applies the same bit swapping transformations in reverse.
```java
public char[] scramble(String password) {
    char[] a = password.toCharArray();
    for (int b = 0; b < a.length; b++) {
      char c = a[b];
      c = switchBits(c, 1, 2);
      c = switchBits(c, 0, 3);
      c = switchBits(c, 5, 6);
      c = switchBits(c, 4, 7);
      c = switchBits(c, 0, 1); 
      c = switchBits(c, 3, 4);
      c = switchBits(c, 2, 5);
      c = switchBits(c, 6, 7);
      a[b] = c;
    }
    return a;
  }
  public char switchBits(char c, int p1, int p2)
  ...
  public boolean checkPassword(String password) {
    char[] scrambled = scramble(password);
    char[] expected = {0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4, 0xF0,
        0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86, 0xD0, 0xA5, 0x45, 0x96, 0x27,
        0xB5, 0x77, 0x94, 0xC1, 0x95, 0xE0, 0xA4, 0xA5, 0x95, 0xF0, 0xE0};
    return Arrays.equals(scrambled, expected);
  }
```
[Back to Navigation](#navigation)

