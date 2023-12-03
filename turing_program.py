#!/usr/bin/env python3
#
# turing_program.py
#
# This is a python library that contains Turing source code to program a
# Turing machine simulator to perform functions.
#
# This library is imported by the turing_machine.py program.
#
# Ian Stewart 2023-12-03
"""
Comment
Current State n, Next State n
Read 0,1 _, keep or 0 Write 1 or _. 1 write 0 or _, _ write 0 or 1.
Move left (l), move right (r), don't move (n = none).
Goto State n (1,2,3,4...)
State Halt (h)

    Code is returned as items in a python dictionary.

    δ(state current,0) = (state next, 1, R)

    Code is in similar manner to Turing document syntax, but is actually a
    python dictionary structure.
    Code in the format δ[0, 0]: 0, 0, 'l'
    i.e. δ[Step, Read]: Next Step, Write, direction,

Each function calls: def change_to_lower_case(δ)
This converts all coding to lower case and all data are strings.
"""
import sys
# Define symbols to simplify writing Turing code. Code can be written as
# case insensitive and characters don't need enclosure in quotes.
_ = "_" # Underscore as "blank" demiliter.
r = "r" # right
R = "R" # Right
l = "l" # left
L = "L" # Left
n = "n" # no move
N = "N" # No move
h = "h" # halt
H = "H" # Halt
c = "c" # Add c for comment as dictionary key.
C = "C" # Comment

# Notes:
#* = "*" # Don't move <-- fails. Use "n" for don't move.
#1 = "1" <-- SyntaxError: cannot assign to literal here.

def function_addition():
    """
    This returns the Turing code that performs the addition function on
    two binary operands.
    """
    δ = {}

    # Program to add numbers. Using Turing document coding style.
    #(State, Read is 0,1 or _) = (State Next, Write 0 or 1 or _, move direction)

    δ[0, c] = ("State 0:  Move right to end of first block of data")
    δ[0, 0] = 0, 0, r  # Move right if zeros
    δ[0, 1] = 0, 1, r  # Move right if ones
    δ[0, _] = 1, _, r  # Move right if underscores, past end of first block of data

    δ[1, c] = "State 1: Move right to end of second block of data"
    δ[1, 0] = 1, 0, r  # Move right if zeros. Stay at state 1
    δ[1, 1] = 1, 1, r  # Move right if ones. Stay at state 1.
    δ[1, _] = 2, _, l  # Move left if underscore. To be back on data. Goto state 2

    δ[2, c] = "State 2: Subtract one in binary"
    δ[2, 0] = 2, 1, l  # If 0, replace with 1, move left. Stay at state 2.
    δ[2, 1] = 3, 0, l  # If 1, replace with 0, move left, goto state 3.
    δ[2, _] = 5, _, r  # If underscore, keep underscore, move right. Goto state 5.

    δ[3, c] = "State 3: Move left to end of first block"
    δ[3, 0] = 3, 0, l  # If zero, keep, move left. Stay at State 3
    δ[3, 1] = 3, 1, l  # If one, keep and move left. Stay at state 3.
    δ[3, _] = 4, _, l  # If underscore, keep, move left. Goto state 4.

    δ[4, c] = "State 4: add one in binary."
    δ[4, 0] = 0, 1, r  # If zero change to one, move right. Goto State 0
    δ[4, 1] = 4, 0, l  # If one change to zero, move left. Stay on state 4
    δ[4, _] = 0, 1, r  # If underscore, change to one, move left. Goto State 0

    # Using lower case
    #δ[5, c] = "State 5: Clean up."
    #δ[5, 1] = 5, _, r  # If one change to underscore move right. Stay at State 5.
    #δ[5, _] = h, _, n  # If underscore, No move. Goto Halt State.

    # Using upper case C, H, R, & N. Note function converts to lower case.
    δ[5, C] = "State 5: Clean up."
    δ[5, 1] = 5, _, R  # If one change to underscore move right. Stay at State 5.
    δ[5, _] = H, _, N  # If underscore, No move. Goto Halt State.

    #print(δ)
    return change_to_lower_case(δ)

    #δ = change_to_lower_case(δ)
    #print(δ)
    #return δ


def function_subtraction():
    """
    TODO: Subtraction - Two operands
    Fill in Turing functions. Use for development of subtraction function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complement one and Move left
    δ[0, _] = h, _, n  # Halt if underscore


    return change_to_lower_case(δ)

def function_multiplication():
    """
    TODO: Multiplication - Two operands
    Fill in Turing functions. Use for development of multiplication function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complement one and Move left
    δ[0, _] = h, _, n  # Halt if underscore


    return change_to_lower_case(δ)


def function_division():
    """
    TODO: Division - Two operands
    Fill in Turing functions. Use for development of division function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complement one and Move left
    δ[0, _] = h, _, n  # Halt if underscore


    return change_to_lower_case(δ)


def function_dec():
    """
    Decrementation of a given number to zero, then halt.
    A single operand function
    """
    δ = {}

    δ[0, c] = "State 0 Move right to end of supplied operand."
    δ[0, 0] = 0, 0, r  # Move right if zeros
    δ[0, 1] = 0, 1, r  # Move right if ones
    δ[0, _] = 1, _, l  # Move left if underscore. To be back on data. Goto state 1

    δ[1, c] = "State 1: Subtract one in binary"
    δ[1, 0] = 1, 1, l  # If 0, replace with 1, move left. Stay at state 1.
    δ[1, 1] = 0, 0, r  # If 1, replace with 0, move right, goto state 0. #<-- could have another state ?
    δ[1, _] = 2, _, r  # If underscore, keep underscore, move right. Goto state 2.

    # In state 1, Gets to a 1. changes to a 0, but goes left to state 2
    # If state 2 is _ then go right and change 0 to underscore.
    # If state 2 is 1 or 0 go to state 0

    δ[2, c] = "State 2: Clean up."
    δ[2, 0] = 2, _, r  # If zero change to underscore move right. Stay at State 2.
    δ[2, 1] = 2, _, r  # If one change to underscore move right. Stay at State 2.
    δ[2, _] = h, _, n  # If underscore, No move. Goto Halt State.

    return change_to_lower_case(δ)


def function_dec1():
    """
    Work-in-progress. Trying to improve the way the Dec comes to a halt.
    Decrementation of a given number to zero, then halt.
    A single operand function
    """
    δ = {}

    δ[0, c] = "State 0 Move right to end of supplied operand."
    δ[0, 0] = 0, 0, r  # Move right if zeros
    δ[0, 1] = 0, 1, r  # Move right if ones
    δ[0, _] = 1, _, l  # Move left if underscore. To be back on data. Goto state 1

    δ[1, c] = "State 1: Subtract one in binary"
    δ[1, 0] = 1, 1, l  # If 0, replace with 1, move left. Stay at state 1.
    δ[1, 1] = 0, 0, r  # If 1, replace with 0, move right, goto state 0. #<-- could have another state ?
    δ[1, _] = 2, _, r  # If underscore, keep underscore, move right. Goto state 2.

    # In state 1, Gets to a 1. changes to a 0, but goes left to state 2
    # If state 2 is _ then go right and change 0 to underscore.
    # If state 2 is 1 or 0 go to state 0

    δ[2, c] = "State 2: clear leading zeros."
    δ[2, 0] = 2, _, r  # If zero change to underscore move right. Stay at State 2.
    δ[2, 1] = 2, _, r  # If one change to underscore move right. Stay at State 2.
    δ[2, _] = 2, _, r  # If underscore, No move. Goto Halt State.

    # Need another state. If state 2 was underscore, then go right and remove the zero

    δ[3, c] = "State 2: Clean up."
    δ[3, 0] = 3, _, r  # If zero change to underscore move right. Stay at State 2.
    δ[3, 1] = 3, _, r  # If one change to underscore move right. Stay at State 2.
    δ[3, _] = h, _, n  # If underscore, No move. Goto Halt State.

    return change_to_lower_case(δ)


def function_inc():
    """
    Given number increment it. Doesn't end.
    A single operand function.
    """
    δ = {}

    δ[0, c] = "State 0 Move right to end of supplied operand."
    δ[0, 0] = 0, 0, r  # Move right if zeros
    δ[0, 1] = 0, 1, r  # Move right if ones
    δ[0, _] = 1, _, l  # Move left if underscore. To be back on data. Goto state 1

    δ[1, c] = "State 1: add one in binary."
    δ[1, 0] = 0, 1, r  # If zero change to one, move right. Goto State 0
    δ[1, 1] = 1, 0, l  # If one change to zero, move left. Stay on state 1
    δ[1, _] = 0, 1, r  # If underscore, change to one, move right. Go to State 0

    return change_to_lower_case(δ)


def function_busy_beaver_3():
    """
    3 States - 2 symbol: 0,1. Halt in 14 Steps with 6 ones.
    Tape should be all ones at start?
    Code from: https://aturingmachine.com/examplesBB3.php
    """

    δ = {}

    # Could be a Halt no t and N
    δ[0,c] = "State 0: 3 State Busy Beaver"
    δ[0,0] = 1, 1, R
    #δ[0,1] = 0, 1, N  # No Halt.
    δ[0,1] = H, 1, N  # Corrected code to be No move and a Halt
    δ[0,_] = 1, 1, R

    δ[1,c] = "State 1: BB3 "
    δ[1,0] = 2,0, R
    δ[1,1] = 1,1, R
    δ[1,_] = 2,0, R

    δ[2,c] = "State 2: BB3 "
    δ[2,0] = 2,1, L
    δ[2,1] = 0,1, L
    δ[2,_] = 2,1, L

    return change_to_lower_case(δ)


def function_busy_beaver_4():
    """
    This returns the Turing code that performs the 4 state busy beaver.
    Initial data is "_" or "".
    (State, Read is 0,1 or _) = (State Next, Write 0 or 1 or _, move direction)

    https://en.wikipedia.org/wiki/Busy_beaver
    the machine must have at most two states in addition to the halting state, and
    the tape initially contains 0s only.
    The tape alphabet is {0, 1}, with 0 serving as the blank symbol.
    nm
    2-state     3-state     4-state     5-state     6-state
    2-symbol    6           21          107         ≥ 47176870  > 10⇈15

    See also: https://aturingmachine.com/examplesBB4.php
    """
    δ = {}

    δ[0, c] = ("State 0: 4 State Busy Beaver")
    δ[0, 0] = 0, _, n  # Read 0 and write underscore. Keep state 0, No move.
    δ[0, 1] = 1, 1, l  # Keep one, change state to 1, move right
    δ[0, _] = 1, 1, r  # read underscroe write 1. Change state to 1, move left

    δ[1, c] = "State 1: "
    δ[1, 0] = 0, _, n  # change 0 to _, don't move, cahnge state to 0.
    δ[1, 1] = 2, _, l  # Change 1 to underscore, move left, change state to 2
    δ[1, _] = 0, 1, l  # Change underscore to 1, move left, change  state to 0

    δ[2, c] = "State 2: "
    δ[2, 0] = 0, _, n  # change 0 to underscore, don't move, change state to 0.
    δ[2, 1] = 3, 1, l  # keep 1, move left, change state to 3
    δ[2, _] = h, 1, r  # change underscore to 1, move right, change state to Halt
    # Display doesn't show the abov e as having been executed
    #δ[2, _] = h, 1, n  # change underscore to 1, move right, change state to Halt

    δ[3, c] = "State 3: "
    δ[3, 0] = 0, _, n  # Change 0 to underscore, no move, change state to 0
    δ[3, 1] = 0, _, r  # change 1 to underscore, move right, change state to 0
    δ[3, _] = 3, 1, r  # change underscore to 1, move right, next state 3

    return change_to_lower_case(δ)


def function_p3():
    """
    Fill in Turing functions. Use for development of new P3 function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complemkent one and Move left
    δ[0, _] = h, _, n  # Halt if underscore

    return change_to_lower_case(δ)


def function_p4():
    """
    Fill in Turing functions. Use for development of new P4 function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complemkent one and Move left
    δ[0, _] = h, _, n  # Halt if underscore

    return change_to_lower_case(δ)

def function_p5():
    """
    Two operands
    Fill in Turing functions. Use for development of new P5 function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complemkent one and Move left
    δ[0, _] = h, _, n  # Halt if underscore


    return change_to_lower_case(δ)

def function_p6():
    """
    Two operands
    Fill in Turing functions. Use for development of new P6 function
    # Complements most left digit, moves left and halts.
    """
    δ = {}

    δ[0, c] = "State 0 Fill-in Unary function"
    δ[0, 0] = 0, 1, l  # Complement zero and Move left
    δ[0, 1] = 0, 0, l  # Complemkent one and Move left
    δ[0, _] = h, _, n  # Halt if underscore

    return change_to_lower_case(δ)


def change_to_lower_case(δ):
    """
    Ensure δ, transition function python dictionary, is only strings and all
    characters are lowercase.
    """
    trf = {}
    for k, v in δ.items():
        if k[1] == "c" or k[1] == "C":
            # Process comments...
            trf[str(k[0]).lower(), str(k[1]).lower()] = v
        else:
            # Process 0, 1 and underscore...
            trf[str(k[0]).lower(), str(k[1]).lower()] =(
                    str(v[0]).lower(), str(v[1]).lower(), str(v[2]).lower())
    #print(trf)
    return trf


'''
def function_xxx():
    """
    Template for additional Turing functions.
    Cut and paste this template then add Turing code. Eg. δ[0, 0] = 1, 0, R
    """

    δ = {}

    δ[0, c] = "State 0 Comment"
    δ[0, 0] =
    δ[0, 1] =
    δ[0, _] =

    δ[1, c] = "State 1 Comment"
    δ[1, 0] =
    δ[1, 1] =
    δ[1, _] =

    δ[2, c] = "State 2 Comment"
    δ[2, 0] =
    δ[2, 1] =
    δ[2, _] =

    return change_to_lower_case(δ)
'''
if __name__=="__main__":

    # For testing...
    function = function_addition()
    #function = function_busy_beaver_4()
    #function = function_busy_beaver_3()

    print(function)

    for key, item in function.items():
        print(key, item)

    sys.exit("\nNote: {} is a python library, and not a stand-alone program."
            .format(sys.argv[0]))


'''
Reference:
Turing Machine Examples. Written in a form of macro to be compiled in to Turing machine code...
https://people.hsc.edu/faculty-staff/robbk/Coms461/Lectures/Lectures%202016/Lecture%2027%20-%20Turing%20Machine%20More%20Examples.pdf

'''
