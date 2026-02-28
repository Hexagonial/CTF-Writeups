# Flag Hunters
Challenge Description:
> Lyrics jump from verses to the refrain kind of like a subroutine call. There's a hidden refrain this program doesn't print by default. Can you get it to print it? There might be something in it for you.

CTF: <b>picoCTF</b> (picoGym)<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> This program can easily get into undefined states. Don't be shy about Ctrl-C.
</details>
<details>
<summary>Hint 2</summary>

> Unsanitized user input is always good, right?
</details>
<details>
<summary>Hint 3</summary>

> Is there any syntax that is ripe for subversion?
</details>

## Procedure
Running the program prints out a line of the song lyrics every half second. A couple of seconds into the program you have to option to input something.
```
$ python3 lyric-reader.py 
Command line wizards, we’re starting it right,
Spawning shells in the terminal, hacking all night.
Scripts and searches, grep through the void,
Every keystroke, we're a cypher's envoy.
Brute force the lock or craft that regex,
Flag on the horizon, what challenge is next?

We’re flag hunters in the ether, lighting up the grid,
No puzzle too dark, no challenge too hid.
With every exploit we trigger, every byte we decrypt,
We’re chasing that victory, and we’ll never quit.
Crowd: HAMMY

Echoes in memory, packets in trace,
```
If you look at the source code (at the line marked with `(1)`), our input effectively becomes part of the lyrics.
```py
# Print lyrics
line_count = 0
lip = start
while not finished and line_count < MAX_LINES:
line_count += 1
for line in song_lines[lip].split(';'):     # <-------------- (2)
    if line == '' and song_lines[lip] != '':
        continue
    if line == 'REFRAIN':
        song_lines[refrain_return] = 'RETURN ' + str(lip + 1)
        lip = refrain
    elif re.match(r"CROWD.*", line): 
        crowd = input('Crowd: ')
        song_lines[lip] = 'Crowd: ' + crowd # <-------------- (1)
        lip += 1
    elif re.match(r"RETURN [0-9]+", line):
        lip = int(line.split()[1])
    elif line == 'END':
        finished = True
    else:
        print(line, flush=True)
        time.sleep(0.5)
        lip += 1
```
Another important observation is that the lyric reader iterates over the lyrics line by line, but delimits each line using the semicolon `;` character (see the line marked with `(2)` in the source code above). The beginning of the program appends a "secret intro" to the start of the lyrics, so `song_lines[0]` would point to the first line of the secret intro. Therefore, we want to somehow return to the first line of the song lyrics.
```py
secret_intro = \
'''Pico warriors rising, puzzles laid bare,
Solving each challenge with precision and flair.
With unity and skill, flags we deliver,
The ether’s ours to conquer, '''\
+ flag + '\n'


song_flag_hunters = secret_intro +\
'''

[REFRAIN]
...
```
If we craft an input ending with `;RETURN 0` we can cause the program to return to the first line of the song lyrics, which is the secret intro.
```
We’re chasing that victory, and we’ll never quit.
Crowd: HAMMY;RETURN 0

Echoes in memory, packets in trace,
Digging through the remnants to uncover with haste.
Hex and headers, carving out clues,
Resurrect the hidden, it's forensics we choose.
Disk dumps and packet dumps, follow the trail,
Buried deep in the noise, but we will prevail.

We’re flag hunters in the ether, lighting up the grid,
No puzzle too dark, no challenge too hid.
With every exploit we trigger, every byte we decrypt,
We’re chasing that victory, and we’ll never quit.
Crowd: HAMMY
Pico warriors rising, puzzles laid bare,
Solving each challenge with precision and flair.
With unity and skill, flags we deliver,
The ether’s ours to conquer, hammy{u win - hammy}
```

## Solution
1. For the crowd input, enter anything followed by `;RETURN 0`. Example:
    - `HAMMY;RETURN 0`
