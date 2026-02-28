check = 'jU5t_a_sna_3lpm13g64f_u_4_m6r143'
password = list('aaaabbbbccccddddaaaabbbbccccdddd')

for i in range(0, 8):
	password[i] = check[i]

for i in range(8, 16):
	password[i] = check[23-i]

for i in range(16, 32, 2):
	password[i] = check[46-i]
	
for i in range(31, 16, -2):
	password[i] = check[i]
	
print(''.join(password))
