# The Add/On Trap
Challenge Description:
> What kind of information can an Add/On reach? Is it possible to exfiltrate them without me noticing? Do they really do what they say? Most importantly, when to eat? These and many other questions Add/On users should be asking themselves.

CTF: <b>picoCTF 2026</b><br>Points: <b>200</b><br>Difficulty: <b>Easy</b>

<b>[Jump to solution](#solution)</b>

## Hints
Here are the hints provided by the challenge author.
<details>
<summary>Hint 1</summary>

> What kind of file is one ending in .xpi?
</details>
<details>
<summary>Hint 2</summary>

> Which modern Python scheme uses url-safe Base64 32-byte keys?
</details>

## Procedure
The challenge gives us an `.xpi` file, which I find out typically holds compressed browser extensions after a quick search. We can extract the files from the xpi file using an online service and look at the contents. Among the files is an interesting one at `background/main.js`.
```js
// Secret key must be 32 url-safe base64-encoded bytes!
// TODO I must find a solution to remove the key from here, for now I'll leave it there because I need it to encrypt the webhook

function logOnCompleted(details) {
    console.log(`Information to exfiltrate: ${details.url}`);
    const key="cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="
    const webhookUrl='gAAAAABmfRjwFKUB-X3GBBqaN1tZYcPg5oLJVJ5XQHFogEgcRSxSis1e4qwicAKohmjqaD-QG8DIN5ie3uijCVAe3xiYmoEHlxATWUP3DC97R00Cgkw4f3HZKsP5xHewOqVPH8ap9FbE'
```

We find a base64 encoded string named `key` (which decodes to `picoCTF{you're on the right tra}`) and a `webhookUrl`.

Based on hint 2, I faintly recall seeing strings that started with `gAAAAAB` (or something similar) in the past but couldn't think of anything. Searching for `gAAAAAB` online (after scrolling past all the weird social media links) actually gives us the final clue: Python's cryptography library (specifically, Fernet). We can use the given key to decrypt the webhook URL:
```py
from cryptography.fernet import Fernet

key = "cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="
ciphertext = b"gAAAAABmfRjwFKUB-X3GBBqaN1tZYcPg5oLJVJ5XQHFogEgcRSxSis1e4qwicAKohmjqaD-QG8DIN5ie3uijCVAe3xiYmoEHlxATWUP3DC97R00Cgkw4f3HZKsP5xHewOqVPH8ap9FbE"

f = Fernet(key)

print(f.decrypt(ciphertext).decode())
```

## Solution
1. Extract the files from the `.xpi` and open `background/main.js`.
2. Decrypt the `webhookUrl` using the key and Python's cryptography (Fernet) library.

## Key Takeaways
New file type (`.xpi`) and how to work with it
