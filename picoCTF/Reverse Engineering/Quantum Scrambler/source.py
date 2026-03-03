
# A and L are lists of all the flag characters in hex
# ['0x61', '0x62', '0x63', '0x64', '0x65', '0x66']
def scramble(L):
  A = L
  i = 2
  while (i < len(A)):
    #print("i="+str(i) + ":\t" + colored_str(A,i))

    # Merge the two elements preceding A[i] by converting it to [A[i-2], A[i-1]]
    A[i-2] += A.pop(i-1)
    #print("\t" + colored_str(A,i))

    A[i-1].append(A[:i-2])
    #print("\t" + colored_str(A,i))
    i += 1
    
  return L

# Print out array A with the colorIndexth element colroed red.
def colored_str(A, colorIndex):
  toReturn = "["
  i = 0
  while i < len(A)-1:
    if i == colorIndex:
      toReturn += "\033[91m{}\033[00m".format(str(A[i])) + ", "
    else:
      toReturn += str(A[i]) + ", "
    i += 1
  
  if i == colorIndex:
    toReturn += "\033[91m{}\033[00m]".format(str(A[i]))
  else:
    toReturn += str(A[len(A)-1])
  i += 1

  while i <= colorIndex:
    if i == colorIndex:
      toReturn += ", \033[91m[]\033[00m]"
    else:
      toReturn += ", []"
    i += 1
  
  return toReturn

# Returns a list of all the flag characters in hex (string)
def get_flag(flag = open('flag.txt', 'r').read()):
  flag = flag.strip()
  hex_flag = []
  for c in flag:
    hex_flag.append([str(hex(ord(c)))])

  return hex_flag

def main():
  flag = get_flag("hammy{u win - hammy}")
  cypher = scramble(flag)
  print(cypher)

if __name__ == '__main__':
  main()
