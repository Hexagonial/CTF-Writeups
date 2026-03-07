
alphabet_min = 32
alphabet_max = 127 # Exclusive
ALPHABET = ""

# Populate the alphabet with all keyboard-inputtable characters except a few that confuse gdb
for i in range(alphabet_min, alphabet_max):
    char = chr(i)
    if char not in ["\"", "\\", "`", "#", "^"]:
        ALPHABET += chr(i)

# 0x1e, determined by reversing the function in which the flag is checked
FLAG_LENGTH = 30

# This script is meant to be run by gdb using the -x option
import gdb
import queue

# Custom Breakpoint class to implement our own handler for what to do when hitting the breakpoint
class Breakpoint(gdb.Breakpoint):
    def __init__(self, breakpoint_result, curr_index, *args):
        super().__init__(*args)
        self.curr_index = curr_index
        self.hits = 0
        self.breakpoint_result = breakpoint_result
        self.silent = True

    def stop(self):
        # Ignore the first curr_index hits since we know they will be correct
        if (self.hits == self.curr_index):
            mutated_char = gdb.parse_and_eval("$dl")
            expected_char = gdb.parse_and_eval("$al")
            success = mutated_char == expected_char
            self.breakpoint_result.put(success)

            # The main loop expects every True to be followed by a False, but the program terminates after 30 characters are correct
            if success and self.curr_index == FLAG_LENGTH-1: 
                self.breakpoint_result.put(False)

            return False
        else:
            self.hits += 1

# Ensure code addresses are not randomized by PIE so breakpoints are consistent
gdb.execute("set disable-randomization on")

# Brute force every character of the flag until the mutated version of our input matches the expected mutation used in the check
flag = "picoCTF{"

# gdb executions run in their own thread, need some form of thread sync to manage it
breakpoint_result = queue.Queue()

for curr_index in range(len(flag), FLAG_LENGTH):
    for possible_char in ALPHABET:
        # 0x5655598e: $dl holds our mutated char, $al holds the expected mutation
        breakpoint = Breakpoint(breakpoint_result, curr_index, '*0x5655598e')
        attempt = flag + possible_char
        print("Attempt: \"" + attempt + "\"")
        gdb.execute("r <<< \"" + attempt + "\"")

        correct_guess = breakpoint_result.get(timeout=2)
        breakpoint.delete()

        if correct_guess == True:
            flag += possible_char
            print("Flag updated: {}".format(flag))

            # Every True should be followed by a False except the last index in which we put an extra False manually
            breakpoint_result.get(timeout=1)
            break

print("Final flag: " + flag)