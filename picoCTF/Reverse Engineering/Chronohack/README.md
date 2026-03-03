# Chronohack
Challenge Description:
> Can you guess the exact token and unlock the hidden flag? Our school relies on tokens to authenticate students. Unfortunately, someone leaked an important file for token generation. Guess the token to get the flag.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Medium</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> https://www.epochconverter.com/
</details>
<details>
<summary>Hint 2</summary>

> https://learn.snyk.io/lesson/insecure-randomness/
</details>
<details>
<summary>Hint 3</summary>

> Time tokens generation
</details>
<details>
<summary>Hint 4</summary>

> Generate tokens for a range of seed values very close to the target time
</details>

## Procedure
This looks to be another seeded PRNG-based problem like the `seed-sPRiNG` problem from the Binary Exploitation section (so, not sure why this is in the Reverse Engineering section). The solution is very similar except we have a new issue - this problem seeds the random with Python's `time.time()`, which has a finer granularity than C's `time(NULL)` function in that it gives a float value (the challenge limits it to millisecond granularity). Fortunately this challenge only generates one token and gives us 50 tries to guess it, meaning we can generate 50 tokens within a range of the current time to account for latency.

The goal is to seed our random with the same value as the target server. However, due to network latency and possible clock desync between us and the target server as well as the granularity of Python's `time.time()` function being in milliseconds, this requires more luck. Because the target server gives us 50 tries to guess one token, we can generate 50 different tokens to try, with each token being generated using a random seeded with a value <i>close to</i> the current time.

According to the source code, all tokens have a length of 20. Therefore the general strategy is:
1. Set an integer `clock_sync_adjustment` to -300 or so (in my successful attempt, I set it to -1000 which was quite overkill since it succeeded once at -60 and once at 10. It can vary based on your ping to the server)
2. While we haven't gotten the flag, do:
    - Make a new connection to the server.
    - Set a variable `currentTime = int(time.time()*1000)`
    - Create an empty list of tokens. For all values of `ping_adjustment` in [0, 49], do:
        - Seed our random with `currentTime + clock_sync_adjustment + ping_adjustment`
        - Generate a token of length 20 (basically, copy the source code's token generation) and add it to the list.
    - Send all 50 tokens.
    - Close the connection to the server.
    

## Solution
1. Set an integer `clock_sync_adjustment` to -300 or so (in my successful attempt, I set it to -1000 which was quite overkill since it succeeded around -60. It will vary based on your ping to the server)
2. While we haven't gotten the flag, do:
    - Make a new connection to the server.
    - Set a variable `currentTime = int(time.time()*1000)`
    - Create an empty list of tokens. For all values of `ping_adjustment` in [0, 49], do:
        - Seed our random with `currentTime + clock_sync_adjustment + ping_adjustment`
        - Generate a token of length 20 (basically, copy the source code's token generation) and add it to the list.
    - Send all 50 tokens.

(Yeah either just look at my working exploit or read the procedure)

## Key Takeaways
Due to the granularity of Python's `time.time()`, this PRNG challenge got me thinking in terms of ping and network latency. When I make a connection to the server, the server will seed its random with its current time and then send me the challenge. There is latency between the time it seeds its random and the time my machine receives the challenge, so it could make sense that I'd have to seed my random with a time value slightly less than my actual current time. Alternatively (because I programming the exploit in a slightly non-deterministic way) my machine could seed its random before my initial request to the server is received, so a seed greater than the actual current time could work as well.
