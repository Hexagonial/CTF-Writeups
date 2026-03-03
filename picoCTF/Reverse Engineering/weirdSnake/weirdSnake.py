
# Convert a string to a list of its decimal ASCII values
def listcomp(str):
    toReturn = []
    for char in str:
        toReturn.append(ord(char))
    return toReturn

# I hardcoded it in the wrong order LUL
input_list = [78, 9, 125, 104, 67, 0, 88, 43, 110, 43, 86, 4, 10, 49,
              7, 108, 8, 36, 110, 7, 70, 9, 4, 48, 23, 108, 32, 57, 
              0, 0, 3, 33, 49, 25, 32, 112, 0, 41, 54, 4]
input_list.reverse()

key_str = 't_Jo3'
key_list = listcomp(iter(key_str))

while len(key_list) < len(input_list):
    key_list.extend(key_list)

def listcomp(input_list, key_list):
    z = zip(input_list, key_list)
    toReturn = []
    for list_tuple in z:
        toReturn.append(list_tuple[0] ^ list_tuple[1])
    return toReturn

result = listcomp(input_list, key_list)
result_text = ''.join(map(chr, result))
print(result_text)
