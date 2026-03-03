from pwn import *

context.log_level = 69

TOKEN_LENGTH = 20
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Seed our random with value currentTime and generate the token
def get_random(currentTime):
    random.seed(currentTime)  # seeding with current time + adjustment
    s = ""
    for i in range(TOKEN_LENGTH):
        s += random.choice(ALPHABET)
    return s

# Send our token
def send_token(token):
    target.recvuntil(b'exit):')
    target.sendline(token)

# Generate 50 random tokens seeding the random with a value within [time, time+49] + adjustment.
def generate_tokens(adjustment):
    currentTime = int(time.time() * 1000) + adjustment
    tokens = []
    for ping_adjustment in range(0, 50):
        tokens.append(get_random(currentTime + ping_adjustment))
    return tokens

win = False
clock_sync_adjustment = -300

while not win:
    tokens = generate_tokens(clock_sync_adjustment)
    target = remote("verbal-sleep.picoctf.net", 51352)
    #target = process(["python3", "./token_generator.py"]) # To test locally
    for i in range(min(len(tokens), 50)):
        send_token(tokens[i])
        response = target.recvline()
        if b"correct" in response:
            print(target.recvall().decode())
            win = True
            break
    target.close()
    clock_sync_adjustment += 10
    print("Adjustment: " + str(clock_sync_adjustment))