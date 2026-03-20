# Password Profiler
Challenge Description:
> We intercepted a suspicious file from a system, but instead of the password itself, it only contains its SHA-1 hash. Using OSINT techniques, you are provided with personal details about the target. Your task is to leverage this information to generate a custom password list and recover the original password by matching its hash.

CTF: <b>picoCTF 2026</b><br>Points: <b>100</b><br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> [CUPP](https://github.com/Mebus/cupp/tree/master) is a Python tool for generating custom wordlists from personal data.
</details>

## Procedure
The password can be found using CUPP's interactive mode (`-i`), manually entering the given information, and selecting `Y` to all the generation options (except the keywords option, since we're not given any additional context).
```
$ python3 cupp.py -i
 ___________ 
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\   
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
                            [ Mebus | https://github.com/Mebus/]


[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: Alice
> Surname: Johnson
> Nickname: AJ
> Birthdate (DDMMYYYY): 15071990


> Partners) name: Bob
> Partners) nickname: 
> Partners) birthdate (DDMMYYYY): 


> Child's name: Charlie
> Child's nickname: 
> Child's birthdate (DDMMYYYY): 


> Pet's name: 
> Company name: 


> Do you want to add some key words about the victim? Y/[N]: 
> Do you want to add special chars at the end of words? Y/[N]: Y
> Do you want to add some random numbers at the end of words? Y/[N]:Y
> Leet mode? (i.e. leet = 1337) Y/[N]: Y

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to alice.txt, counting 29372 words.
> Hyperspeed Print? (Y/n) : n
[+] Now load your pistolero with alice.txt and shoot! Good luck!

$ python3 check_password.py 
Password found: hammy{u win - hammy}
```

## Solution
1. Use CUPP's interactive mode (`-i`) and enter all the information given with all options enabled (except manually entering keywords) to get a password list containing the password. No need to change the configuration.
2. Rename the list to `passwords.txt`.
3. Run `python3 check_password.py`

## Key Takeaways
Another brute-forcing tool under my belt
