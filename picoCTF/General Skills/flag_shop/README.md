# flag_shop
Challenge Description:
> There's a flag shop selling stuff, can you buy a flag?

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> Two's compliment can do some weird things when numbers get really big!
</details>

## Procedure
The target program is a shop simulation. We start with a balance of 1100.
```
$ nc fickle-tempest.picoctf.net 62606
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
1



 Balance: 1100 


Welcome to the flag exchange
We sell flags
```
There are two kinds of flags in stock, `Definitely not the flag` flags and a single 1337 flag. We probably want the 1337 flag since we can't afford it.
```
 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
1
These knockoff Flags cost 900 each, enter desired quantity
10

The final cost is: 9000
Not enough funds to complete purchase
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
2
1337 flags cost 100000 dollars, and we only have 1 in stock
Enter 1 to buy one1

Not enough funds for transaction
```
An important observation to make is that when buying multiple of the `Definitely not the flag` flags, the total cost is calculated before the purchase attempt is made instead of the flags being purchased one by one.

If the cost is stored in a signed integer, attempting to buy too many flags at once may cause the cost to wrap into the negatives. The maximum positive value for an integer is 2.147 billion something-or-other that I can never remember so we can estimate with 3 billion instead.
```
3000000000/900 = 3333333.3333...
```
Let's try buying 3.33 million flags.
```
 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
1
These knockoff Flags cost 900 each, enter desired quantity
3333333

The final cost is: -1294967596

Your current balance after transaction: 1294968696
```
Clearly 1100 >= -1.3 billion so the purchase succeeds. The program will simply <i>subtract</i> the cost from our balance, thus adding 1.3 billion to our balance. We can afford the 1337 flag now :3
```
 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
2
1337 flags cost 100000 dollars, and we only have 1 in stock
Enter 1 to buy one1
YOUR FLAG IS: hammy{u win - hammy}
```

## Solution
1. Buy 3333333 `Definitely not the flag` Flags.
2. Buy a 1337 flag.

