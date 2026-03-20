from pwn import *

context.log_level = 69

target = remote("green-hill.picoctf.net", 62271)

ember_sigil = 0x8049176
glyph_conflux = 0x804919a
astral_spark = 0x80491c1
binding_word = 0x80491e3

def send_answer():
    # Read in the procedure we need the address for
    target.recvuntil(b'procedure \'')
    spell = target.recvuntil(b'\'', drop=True).decode()

    # if statements are more secure but i got lazy. surely picoctf wouldn't attack me
    to_send = eval(spell)
    
    # Send it when given the prompt
    target.recvuntil(b'=>')
    target.send(p32(to_send))

# We get 3 questions
send_answer()
send_answer()
send_answer()
print(target.recvall().decode().strip())