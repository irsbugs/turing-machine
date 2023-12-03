#!/usr/bin/env python3
#
# turing_machine.py
# Requires: turing_program.py
#
# Using a GUI simulate a Turing machine.
# Includes a calculator style user interface to the Turing machine.
# Code written for the Turing machine resides in turing_program.py
#
# Ian Stewart 2023-12-03
#
# TODO:
#
# Fix up halt for BB4
# Last line of code become a comment that stores parameters. Thus don't need a separate config file.
# Have a help window on launch?
# Have hover pop-up messageboxes.
#

import tkinter as tk
from tkinter import ttk
import sys
import time

try:
    import turing_program
except:
    print("This program, {}, requires the file 'turing_program.py' to reside "
            "in the directory, '{}'.".format(sys.argv[0], sys.path[0]))
    sys.exit("\nExiting...")

# Import Turing code as a dictionary. Eg.
# {(0, 'c'): 'State 0:  Move right to end of first block of data',
# (0, 0): (0, 0, 'r'), (0, 1): (1, 1, 'r'), (0, '_'): (1, '_', 'r'), ...}

# Load Turing functions (python dictionaries) from turing _program library.
# Unary opration functions - One operand
dec = turing_program.function_dec()
inc = turing_program.function_inc()
p3 = turing_program.function_p3()
p4 = turing_program.function_p4()

# Binary operations functions - two operands
addition = turing_program.function_addition()
subtraction = turing_program.function_subtraction()
multiplication = turing_program.function_multiplication()
division = turing_program.function_division()
p5 = turing_program.function_p5()
p6 = turing_program.function_p6()

# Function only
bb3 = turing_program.function_busy_beaver_3()
bb4 = turing_program.function_busy_beaver_4()


# Label Constants

TITLE = "Turing Machine - Calculator"
FRAME1_TEXT = "Turing Machine"
FRAME2_TEXT = "Simulator Interface"

F1A_TEXT = "Tape"
F1AA_TEXT = "10"
L1AA_TEXT = "0"
F1B_TEXT = "Instruction Counter and Code Information"
F1C_TEXT = "Instruction Comment"

F2A_TEXT = "Display"
F2A1_TEXT = "Hex"
F2A2_TEXT = "Binary"
F2A3_TEXT = "Decimal"
F2B_TEXT = "Input"
F2B1_TEXT = "Speed"

F1BL1_TEXT = "Counter"
F1BL2_TEXT = "Instruction"
F1BL3_TEXT = "Head Position"
F1BL4_TEXT = "Current State"
F1BL5_TEXT = "Next State"
F1BL6_TEXT = "Read"
F1BL7_TEXT = "Write"
F1BL8_TEXT = "Direction"
F1BL20_TEXT = "Comment"

# Calculator P-buttons text
P1_TEXT = "BB3"
P2_TEXT = "BB4"
P3_TEXT = "P3"
P4_TEXT = "P4"
P5_TEXT = "P5"
P6_TEXT = "P6"
P7_TEXT = "Go"
P8_TEXT = "Stop"

# Calculator F-buttons text
F1_TEXT = "Inc"
F2_TEXT = "Dec"
F3_TEXT = "+"
F4_TEXT = "-"
F5_TEXT = "*"
F6_TEXT = "//"
F7_TEXT = "="
F8_TEXT = "Clear"


# Default settings.
TAPE_RANGE = 10 # Default.
TAPE_RANGE = 16 # 16 is better
# Tape length may be changed. Default of 1000 is a range from -500 to +500.
TAPE_LENGTH = 1000
MAX_ITERATION = 9999


class Turing(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.style = ttk.Style()

        self.parent = parent
        #self.parent.wm_geometry("1000x1000+0+0")
        #self.parent.resizable(width=1200, height=600)
        #self.parent.minsize(width=1200, height=1000)
        self.parent.wm_title(TITLE)
        #self.init_tape()

        self.head_position = 0

        self.is_operand_1 = False
        self.is_operand_2 = False
        self.is_operator = False
        self.is_execute = False
        self.operand_1 = ""
        self.operand_2 = ""
        self.operator = ""

        self.delay=0

        self.setup_frame_1()
        self.setup_tape_frame()
        self.setup_calculator_input_frame()

        #self.update_hex_bin_dec_display()
        self.setup_information_display()

        self.reset_tape()

        '''
        TKinter window updating...
        self.update()
        Enter event loop until all pending events have been processed by Tcl.

        self.update_idletasks()
        Enter event loop until all idle callbacks have been called.
        '''
        # GUI should now be displayed. Ready for data/function input.
        self.update()
        #self.update_idletasks()

        # Provide autostart for debugging.
        # Remove commment and edit auto_start function
        #self.auto_start()


    def auto_start(self):
        """
        When Turing_machine.py is launched, then it starts automatically in
        performing a function.
        E.g. Selects addition function and applies operands from initial_data.
        Edit this function to autostart a function under test.
        Remove the comment above from #self.auto_start()
        """
        self.state = "0" #str(state)

        # Define thew autostart function.
        self.trf = {}
        self.trf = dec #inc #dec #addition #bb4 #bb4 # bb3 addition

        # Setup the initial data.
        #initial_data = '11_10'
        #initial_data = '_'
        initial_data = '11111'


        # Create self.tape_dict as a dictionary with keys from -500 to +501
        # The value for a key can be 0 or 1 or the underscore / delimiter.
        self.tape_dict = {}
        for i in range((TAPE_LENGTH // 2 * -1), (TAPE_LENGTH // 2 + 1)):
            self.tape_dict[i] = "_"

        # Set the midpoint of the tape to a value of 0
        self.tape_dict[0] = "0"

        # Position the head at the mid point of the tape. i.e. 0.
        self.head_position = 0

        # Write intital data starting at 0 position on the tape.
        for index, value in enumerate(initial_data):
            self.tape_dict[index] = value

        self.run_turing_program()


    def setup_turing_machine(self, program, initial_data, state=0):
        """
        Initialize tape dictionary, load data, select function, load functions
        code into trf dictionary. set start state.
        Set head at start point
        """
        self.trf = {}  # trf - transition function dictionary. Turing code

        self.state = str(state)

        # Create self.tape_dict as a dictionary with keys from -500 to +501
        # The value for a key can be 0 or 1 or the underscore / delimiter.
        self.tape_dict = {}
        for i in range((TAPE_LENGTH // 2 * -1), (TAPE_LENGTH // 2 + 1)):
            self.tape_dict[i] = "_"

        # Set the midpoint of the tape to a value of 0
        self.tape_dict[0] = "0"

        # Position the head at the mid point of the tape. i.e. 0.
        self.head_position = 0

        # Write intital data starting at 0 position on the tape.
        for index, value in enumerate(initial_data):
            self.tape_dict[index] = value

        #print(self.tape_dict)

        self.trf = program

        #print("self.trf:", self.trf)
        #print("self.trf['0','1']:", self.trf["0","1"])
        #sys.exit()


    def step(self, iteration_counter):
        """
        Execution of each step
        Requires:
        self.tape, (1001 underscores with data starting at 500 - string
        self.tape_dict = -500 to +500
        self.trf (loaded with program),
        self.state, (Initially 0 - First state is 0)
        self.head_position (Int - position on the tape)
        iteration_counter ( passed by run() )

        self.f1bl11.configure(text="")  # Counter
        self.f1bl12.configure(text="")  # Instruction
        self.f1bl13.configure(text="")  # Head Position
        self.f1bl14.configure(text="")  # Current State
        self.f1bl15.configure(text="")  # Next State
        self.f1bl16.configure(text="")  # Read
        self.f1bl17.configure(text="")  # Write
        self.f1bl18.configure(text="Right") # Direction
        self.f1cl21.configure(text=self.trf.get((self.state, "c")))  # Comment

        # TODO: Reflect Tape content in display
        """
        if self.state != 'h':
         # assert self.head_position >= 0 and self.head_position < len(self.tape) here
            """
            X = self.tape[self.head_position]
            print("type(self.head_position):", type(self.head_position))
            print("First X", X ) # string
            print("type(self.tape):", type(self.tape))  # string
            """
            self.f1bl11.configure(text=iteration_counter)  # Counter
            self.f1bl13.configure(text=self.head_position)  # Head Position
            self.f1bl14.configure(text=self.state)  # Current State


            # Read the data at the head position. E.g. "0", "1" or "_"
            X = self.tape_dict[self.head_position]
            self.f1bl16.configure(text=X)  # Read
            print("self.state:", self.state, ", X:", X)

            # Print the comment...
            self.f1cl21.configure(text=self.trf.get((self.state, "c"))) # Comment
            print(self.trf.get((self.state, "c")))

            # Get the action items of the state and character read from tape.
            action = self.trf.get((self.state, X))

            #s = "δ{}={})".format((self.state, X), self.trf.get((self.state, X)))
            s = "{}{}".format((self.state, X), self.trf.get((self.state, X)))
            self.f1bl12.configure(text=s)  # Instruction
            #self.f1bl12.configure(text=(self.state, X) + self.trf.get((self.state, X)))  # Instruction

            p = self.state  # Current state

            print("action:", action)
            if action:
                # Get 3 x items, next state, character to write, tape dictection from action tuple
                q, Y, D = action
                self.f1bl15.configure(text=q)  # Next State
                self.f1bl17.configure(text=Y)  # Write
                # Expand r, l, n.
                if D == "r":
                    direction = "right"
                elif D == "l":
                    direction = "left"
                elif D == "n":
                    direction = "none"
                else:
                    direction = D
                self.f1bl18.configure(text=direction) # Direction
                self.update()

                # Write change of 0,1 or _ to tape
                self.tape_dict[self.head_position] = Y
                # Update so that what was written can be seen
                self.move_tape()
                # Pause
                time.sleep(self.delay)
                self.update()

                # If L or R move head. Else N for no move.
                if D != 'n':  # * is "No move". Change to use "n" for "No move"
                    self.head_position = self.head_position + (1 if D == 'r' else -1)

            print("self.head_position:", self.head_position)

            # Move the head position
            self.move_tape()
            # Pause
            time.sleep(self.delay)
            self.update()

            # Set next state
            self.state = q

            print(iteration_counter, ":", p, X, q, Y, D, ":" )

            # Perform the stop/go button polling routine
            # Stop pressed?
            if "pressed" in self.button_stop.state():
                print("Stop pressed")
                #self.root.update()

                while True:
                    # Go pressed?
                    if "pressed" in self.button_go.state():
                        print("Button Go pressed. Exiting Stop loop")
                        break
                    print("Stop loop")
                    self.parent.update()
                    time.sleep(0.2)


    def run_turing_program(self, max_iter=MAX_ITERATION):
        """
        Run a Turing program.
        Test for a halt instruction to force exit from program
        Test for a loop witrh excessive iterations and no halt.
        """
        iteration_counter = 0
        while self.state != 'h' and iteration_counter < max_iter: # prevent infinite loop
            self.step(iteration_counter)
            iteration_counter += 1

            # Get all data from the tape. Ignore leading and trailing underscores
            for k, v in self.tape_dict.items():
                if v != "_":
                    tape_data_start = k
                    break
            for k, v in reversed(self.tape_dict.items()):
                if v != "_":
                    tape_data_end = k
                    break
            s = ""
            for i in range(tape_data_start, tape_data_end + 1):
                s += self.tape_dict[i]

            # Update the display with first field of the contents of tape
            # S could be of zero length?
            # S could contain one or more underscore delimiters, if so pass the first
            s_list = s.split("_")
            if len(s_list) != 0:
                print("s_list[0]:", s_list[0])
                self.update_hex_bin_dec_display_code_running(s_list[0])

            # Display data
            print("Data length:", len(s))
            print(iteration_counter, ":", s, ":", self.state)  # E.g. 101 : 10000___1 : 5

        #print(iteration_counter, ":", s, ":", self.state)  # E.g. 101 : 10000___1 : 5


    def calculator_cb(self, button):
        """
        #print("got here")
        #print(dir(button))
        #print(button)  # 2,3 4... etc label on the button
        #print(dir(self.button_2a.config(items)))

        FEDC    Inc Dec    BB3 BB4
        BA98    +   -      P3  P4
        7654    *   //     P5  P6
        3210    =  Clear   Go  Stop

        # An operand is also referred to as "one of the inputs (quantities) for an operation"
        self.is_operand_1 = False
        self.is_operand_2 = False
        self.is_operator = False

        # Catagories: E.g. Addition is 2 operands, Dec 1 operand. Busy Beaver is 0 operands.
        """

        if button in ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]:
            print("button is numeric: {}".format(button))

            if self.is_operator:
                self.is_operand_2 = True
                self.operand_2 += button
            else:
                self.is_operand_1 = True
                self.operand_1 += button

            print(self.operand_1, self.operator, self.operand_2)
            self.update_hex_bin_dec_display()

        elif button in ["BB3", "BB4"]:
            # Neither unary or binary. Todo: Clear all data, no zero
            # Busy Beaver 3 state or 4 state
            print("button is operator: {}".format(button))

            self.is_operator = True
            self.operator = button
            print(self.operand_1, self.operator)

            # For BB3, setup and call the run_turing_prog
            if self.operator =="BB3":
                self.trf = bb3
                self.state = "0"
                self.run_turing_program()

            # For BB4, setup and call the run_turing_prog
            # TODO: Code for bb4 needs to be fixed at the halt.
            if self.operator =="BB4":
                self.trf = bb4
                self.state = "0"
                self.run_turing_program()


        elif button in ["Inc", "Dec", "P3", "P4"]:
            # Unary operators, only one operand is supplied.
            # Does not need = to start execution.
            # TODO: Add Square root, Negate, Complement, absolute?

            if not self.is_operand_1:
                return

            print("button is operator: {}".format(button))

            self.is_operator = True
            self.operator = button
            print(self.operand_1, self.operator)


            print("Unary Execute: ", self.operand_1, self.operator)
            # [2:] removes the 0b in the returned binary string
            print("Unary Execute: ", bin(int(self.operand_1, 16))[2:], self.operator, )
            print("Unary Execute: ", int(self.operand_1, 16), self.operator,)

            self.update_hex_bin_dec_display()

            # Write binary data to tape
            for i in range((TAPE_LENGTH // 2 * -1), (TAPE_LENGTH // 2 + 1)):
                self.tape_dict[i] = "_"

            tape_input_data_str = bin(int(self.operand_1, 16))[2:]
            tape_input_data_list = list(tape_input_data_str)

            for index, item in enumerate(tape_input_data_list):
                self.tape_dict[index] = item

            #print(self.tape_dict, len(self.tape_dict))
            for index, i in enumerate(range(self.head_position -TAPE_RANGE, self.head_position + TAPE_RANGE + 1)):
                self.tape_frames[index].config(text=str(i))
                self.tape_labels[index].config(text=self.tape_dict[i])

            # For Decrement, setup and call the run_turing_prog
            if self.operator =="Dec":
                self.trf = dec
                self.state = "0"
                self.run_turing_program()

            # For Increment, setup and call the run_turing_prog
            if self.operator =="Inc":
                self.trf = inc
                self.state = "0"
                self.run_turing_program()

            # For P3, setup and call the run_turing_prog
            if self.operator =="P3":
                self.trf = p3
                self.state = "0"
                self.run_turing_program()

            # For P4, setup and call the run_turing_prog
            if self.operator =="P4":
                self.trf = p4
                self.state = "0"
                self.run_turing_program()

        elif button in ["+", "-", "*", "//", "P5", "P6"]:
            # Binary operators. 2 x operands and then = to start execution
            print("button is operator: {}".format(button))
            # Operand_1 must have been entered before operator.
            if not self.is_operand_1:
                return
            if self.is_operand_1 and self.is_operand_2:
                return
            if self.is_operand_1 and self.is_operator:
                return
            self.is_operator = True
            self.operator = button

            print(self.operand_1, self.operator)
            self.update_hex_bin_dec_display()

        elif button == "=":
            print("button is executor: {}".format(button))
            self.is_execute = True

            print("Execute: ", self.operand_1, self.operator, self.operand_2)
            # [2:] removes the 0b in the returned binary string
            print("Execute: ", bin(int(self.operand_1, 16))[2:], self.operator, bin(int(self.operand_2, 16))[2:],)
            print("Execute: ", int(self.operand_1, 16), self.operator, int(self.operand_2, 16),)

            self.update_hex_bin_dec_display()

            # Write binary data to tape
            for i in range((TAPE_LENGTH // 2 * -1), (TAPE_LENGTH // 2 + 1)):
                self.tape_dict[i] = "_"

            tape_input_data_str = bin(int(self.operand_1, 16))[2:] + "_" + bin(int(self.operand_2, 16))[2:]
            tape_input_data_list = list(tape_input_data_str)

            for index, item in enumerate(tape_input_data_list):
                self.tape_dict[index] = item

            #print(self.tape_dict, len(self.tape_dict))
            for index, i in enumerate(range(self.head_position -TAPE_RANGE, self.head_position + TAPE_RANGE + 1)):
                self.tape_frames[index].config(text=str(i))
                self.tape_labels[index].config(text=self.tape_dict[i])


            # For addition, setup and call the run_turing_prog
            if self.operator =="+":
                self.trf = addition
                self.state = "0"
                self.run_turing_program()

            # For subtraction, setup and call the run_turing_prog
            if self.operator =="-":
                self.trf = subtraction
                self.state = "0"
                self.run_turing_program()

            # For multiplication, setup and call the run_turing_prog
            if self.operator =="*":
                self.trf = multiplication
                self.state = "0"
                self.run_turing_program()

            # For division, setup and call the run_turing_prog
            if self.operator =="//":
                self.trf = division
                self.state = "0"
                self.run_turing_program()

            # For P5 function, setup and call the run_turing_prog
            if self.operator =="P5":
                self.trf = p5
                self.state = "0"
                self.run_turing_program()

             # For P6 function, setup and call the run_turing_prog
            if self.operator =="P6":
                self.trf = p6
                self.state = "0"
                self.run_turing_program()

        elif button == "Clear":
            print("button is command: {}".format(button))
            self.reset_tape() # Also clears variables.


    def move_tape(self): #, direction):
        """
        TODO: Rename to tape_update ?

        self.tape_dict appears to move right or left one position
        self.tape_labels display a new section of self.tape_dict
        and self.tape_frames get renumbered.
        Total labels is based on TAPE_RANGE.
        direction = "L" or "R" from turing instruction
        """

        # E.g. -16 to +16 of head position, when TAPE_RANGE = 16
        for index, i in enumerate(range(self.head_position - TAPE_RANGE, self.head_position + TAPE_RANGE + 1)):
            self.tape_frames[index].config(text=str(i))
            self.tape_labels[index].config(text=self.tape_dict[i])


    def slider_changed(self, event):
        """
        Top of slider is 0 - i.e. Fast 0 - no delay
        Bottom of slider is 100 i.e. Slow 1 second delay.
        """
        print("int(self.speed.get()):", int(self.speed.get()))
        self.delay =  (int(self.speed.get())) / 100


    def reset_tape(self):
        """
        Reset the tape to underscore, with position zero set to zero.
        """
        # Re-initialize the tape_dict
        self.tape_dict = {}

        # head_position to 0 reset tape_dict to underscore and 0.
        for i in range((TAPE_LENGTH // 2 * -1), (TAPE_LENGTH // 2 + 1)):
            self.tape_dict[i] = "_"

        # Set the midpoint of the tape to a value of 0
        self.tape_dict[0] = "0"

        self.head_position = 0

        # Update the frames displayed
        for index, i in enumerate(range(self.head_position - TAPE_RANGE, self.head_position + TAPE_RANGE + 1)):
            self.tape_frames[index].config(text=str(i))
            self.tape_labels[index].config(text=self.tape_dict[i])

        # Clear fields.
        self.is_operand_1 = False
        self.is_operand_2 = False
        self.is_operator = False
        self.is_execute = False
        self.operand_1 = ""
        self.operand_2 = ""
        self.operator = ""
        self.label_hex.config(text="")
        self.label_binary.config(text="")
        self.label_decimal.config(text="")

        self.f1bl11.configure(text="")  # Counter
        self.f1bl12.configure(text="")  # Instruction
        self.f1bl13.configure(text="")  # Head Position
        self.f1bl14.configure(text="")  # Current State
        self.f1bl15.configure(text="")  # Next State
        self.f1bl16.configure(text="")  # Read
        self.f1bl17.configure(text="")  # Write
        self.f1bl18.configure(text="")  # Direction
        self.f1cl21.configure(text="")  # Comment


    def update_hex_bin_dec_display_code_running(self, data_string):
        """
        Update the display with the contents of the tape,
        with underscores removed.

        Labels updated...
        self.label_hex.config(text=s)
        self.label_binary.config(text=s)
        self.label_decimal.config(text=s)
        """
        # This has already bee done.
        data_list = data_string.split("_")
        # Remove empty fields from a list
        data_list = list(filter(None, data_list))

        # Hex
        s = ""
        for data in data_list:
            s += hex(int(data, 2))[2:]+ ", "
        s = s[:-2]
        self.label_hex.config(text=s)

        # Binary
        s = ""
        for data in data_list:
            s += data + ", "
        s = s[:-2]
        self.label_binary.config(text=s)

        # Decimal
        s = ""
        for data in data_list:
            s += str(int(data, 2)) + ", "
        s = s[:-2]
        self.label_decimal.config(text=s)


    def update_hex_bin_dec_display(self):
        """
        Update the Calculator Display labels.
        Depends on how far through creating the calculation.
        self.label_hex.config(text=)
        self.label_binary.config(text=s)
        self.label_decimal.config(text=s)

        """
        if self.is_execute:
            self.label_hex.config(text="{} {} {} = ".format(self.operand_1, self.operator, self.operand_2))
            # [2:] removes the 0b in the returned binary string
            s = "{} {} {} = ".format(bin(int(self.operand_1, 16))[2:], (self.operator), bin(int(self.operand_2, 16))[2:])
            self.label_binary.config(text=s)
            s = "{} {} {} = ".format(int(self.operand_1, 16), self.operator, int(self.operand_2, 16),)
            self.label_decimal.config(text=s)
            return

        if self.is_operator and self.is_operand_2:
            self.label_hex.config(text="{} {} {}".format(self.operand_1, self.operator, self.operand_2))
            # [2:] removes the 0b in the returned binary string
            s = "{} {} {}".format(bin(int(self.operand_1, 16))[2:], (self.operator), bin(int(self.operand_2, 16))[2:])
            self.label_binary.config(text=s)
            s = "{} {} {}".format(int(self.operand_1, 16), self.operator, int(self.operand_2, 16),)
            self.label_decimal.config(text=s)
            return

        if self.is_operator:
            self.label_hex.config(text="{} {}".format(self.operand_1, self.operator, self.operand_2))
            # [2:] removes the 0b in the returned binary string
            s = "{} {}".format(bin(int(self.operand_1, 16))[2:], self.operator)
            self.label_binary.config(text=s)
            s = "{} {}".format(int(self.operand_1, 16), self.operator,)
            self.label_decimal.config(text=s)
            return

        self.label_hex.config(text="{}".format(self.operand_1,))
        s = "{}".format(bin(int(self.operand_1, 16))[2:])
        self.label_binary.config(text=s)
        s = "{}".format(int(self.operand_1, 16),)
        self.label_decimal.config(text=s)


    #===== Remaining methods are for tkinter "setup" =====
    def setup_frame_1(self):
        """
        Setup the Turing frames.
        1. Main Turing set of frames
        1A. Turing Tape display
        1B. Turing Programming information
        2. Turing Calculator style interface.
        """
        # Configure Frame 1 - Main Turing Machine Frame
        self.style.configure("F1.TFrame", relief="solid", borderwidth=2,  padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F1.TFrame.Label", font=('Helvetica', 14), )
        f1 = ttk.Labelframe(self.parent, text=FRAME1_TEXT, style="F1.TFrame", width = 800, height = 200,)
        f1.grid(row=0, column=0,  sticky="nsew", padx=5, pady=5)

        # Configure Frame 1A - Tape Display
        self.style.configure("F1A.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F1A.TFrame.Label", font=('Helvetica', 14),)
        self.f1a = ttk.Labelframe(f1, text=F1A_TEXT, style="F1A.TFrame", width = 800, height = 200,)
        self.f1a.grid(row=0, column=0,  sticky="nsew")

        # Configure Frame 1B - Code Information Display
        self.style.configure("F1B.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5),labelmargins=5)
        self.style.configure("F1B.TFrame.Label", font=('Helvetica', 14), )
        self.f1b = ttk.Labelframe(f1, text=F1B_TEXT, style="F1B.TFrame", width = 800, height = 200,)
        self.f1b.grid(row=1, column=0,  sticky="nsew")

        # Configure Frame 1C - Code Comment
        self.style.configure("F1C.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5),labelmargins=5)
        self.style.configure("F1C.TFrame.Label", font=('Helvetica', 14), )
        self.f1c = ttk.Labelframe(f1, text=F1C_TEXT, style="F1C.TFrame", width = 800, height = 200,)
        self.f1c.grid(row=2, column=0,  sticky="nsew")

        # Configure Frame 2 - Calculator Style Input
        self.style.configure("F2.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2.TFrame.Label", font=('Helvetica', 14),)
        f2 = ttk.Labelframe(self.parent, text=FRAME2_TEXT, style="F2.TFrame", width = 800, height = 200,)
        f2.grid(row=1, column=0,  sticky="nsew", padx=5, pady=5)

        # Configure Frame 2A - Calculator Display
        self.style.configure("F2A.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2A.TFrame.Label", font=('Helvetica', 14),)
        self.f2a = ttk.Labelframe(f2, text=F2A_TEXT, style="F2A.TFrame", width = 800, height = 200,)
        self.f2a.grid(row=0, column=0,  sticky="nsew")

        # Configure Frame 2A1 - Hex Display
        self.style.configure("F2A1.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2A1.TFrame.Label", font=('Helvetica', 14),)
        self.f2a1 = ttk.Labelframe(self.f2a, text=F2A1_TEXT, style="F2A1.TFrame", width = 300, height = 200,)
        self.f2a1.grid(row=0, column=0,  sticky="nsew")

        self.label_hex = ttk.Label(self.f2a1, text="", font=('Helvetica', 14))
        self.label_hex.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2A2 - Binary Display
        self.style.configure("F2A2.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2A2.TFrame.Label", font=('Helvetica', 14),)
        self.f2a2 = ttk.Labelframe(self.f2a, text=F2A2_TEXT, style="F2A2.TFrame", width = 300, height = 200,)
        self.f2a2.grid(row=0, column=1,  sticky="nsew")

        self.label_binary = ttk.Label(self.f2a2, text="", font=('Helvetica', 14))
        self.label_binary.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2A3 - Decimal Display
        self.style.configure("F2A3.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2A3.TFrame.Label", font=('Helvetica', 14),)
        self.f2a3 = ttk.Labelframe(self.f2a, text=F2A3_TEXT, style="F2A2.TFrame", width = 300, height = 200,)
        self.f2a3.grid(row=0, column=2,  sticky="nsew")

        self.label_decimal = ttk.Label(self.f2a3, text="", font=('Helvetica', 14))
        self.label_decimal.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2B - Calculator Input
        self.style.configure("F2B.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2B.TFrame.Label", font=('Helvetica', 14),)
        self.f2b = ttk.Labelframe(f2, text=F2B_TEXT, style="F2B.TFrame", width = 800, height = 200,)
        self.f2b.grid(row=1, column=0,  sticky="nsew")


        # Configure Frame 3
        #self.style.configure("F3.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5), labelmargins=5)
        #self.style.configure("F3.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        #self.f3 = ttk.Labelframe(self.parent, text=F3_TEXT, style="F3.TFrame", width = 800, height = 200,)
        #self.f3.grid(row=2, column=0, sticky="NSEW")


    def setup_information_display(self):
        """
        Configure contents of Frame 1B - Code Information Display
        Setup the labels for display of code execution information
        Counter, Instruction, Head Position, Current State, Next State, Read, Write, Direction,

        self.f1b = ttk.Labelframe(f1, text=F1B_TEXT, style="F1B.TFrame", width = 800, height = 200,)
        self.f1b.grid(row=1, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        self.f1bl11.configure(text="")  # Counter
        self.f1bl12.configure(text="")  # Instruction
        self.f1bl13.configure(text="")  # Head Position
        self.f1bl14.configure(text="")  # Current State
        self.f1bl15.configure(text="")  # Next State
        self.f1bl16.configure(text="")  # Read
        self.f1bl17.configure(text="")  # Write
        self.f1bl18.configure(text="")  # Direction
        self.f1bl21.configure(text="")  # Comment
        """
        self.f1bl1 = ttk.Label(self.f1b, text=F1BL1_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl1.grid(row=0, column=0,)
        self.f1bl2 = ttk.Label(self.f1b, text=F1BL2_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl2.grid(row=0, column=1)
        self.f1bl3 = ttk.Label(self.f1b, text=F1BL3_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl3.grid(row=0, column=2)
        self.f1bl4 = ttk.Label(self.f1b, text=F1BL4_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl4.grid(row=0, column=3)
        self.f1bl5 = ttk.Label(self.f1b, text=F1BL5_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl5.grid(row=0, column=4)
        self.f1bl6 = ttk.Label(self.f1b, text=F1BL6_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl6.grid(row=0, column=5)
        self.f1bl7 = ttk.Label(self.f1b, text=F1BL7_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl7.grid(row=0, column=6)
        self.f1bl8 = ttk.Label(self.f1b, text=F1BL8_TEXT, borderwidth=2, font=('Helvetica', 12), anchor="center")
        self.f1bl8.grid(row=0, column=7)


        self.f1bl11 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl11.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
        self.f1bl12 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl12.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))
        self.f1bl13 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl13.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))
        self.f1bl14 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl14.grid(row=1, column=3, padx=(5, 5), pady=(5, 5))
        self.f1bl15 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl15.grid(row=1, column=4, padx=(5, 5), pady=(5, 5))
        self.f1bl16 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl16.grid(row=1, column=5, padx=(5, 5), pady=(5, 5))
        self.f1bl17 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl17.grid(row=1, column=6, padx=(5, 5), pady=(5, 5))
        self.f1bl18 = ttk.Label(self.f1b, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 13, anchor="center")
        self.f1bl18.grid(row=1, column=7, padx=(5, 5), pady=(5, 5))

        # Instruction Comment - Insert in F1C
        #self.f1cl20 = ttk.Label(self.f1c, text=F1BL20_TEXT, borderwidth=2, font=('Helvetica', 12),) # anchor="w", justify=tk.LEFT)
        #self.f1cl20.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        self.f1cl21 = ttk.Label(self.f1c, text="", borderwidth=2, font=('Helvetica', 12), relief="groove", width = 120, anchor="w")
        self.f1cl21.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))


    def setup_calculator_input_frame(self):
        """
        Calculator style of frame to control Turing Machine.
        # Frame 2A
        Buttons in the frame
        0123 4  5   6   7  8  9    10  11
        ------------------------------------------
        FEDC    Inc Dec    P1 P2       Speed Frame
        BA98    +   -      P3 P4
        7654    *   //     P5 P6
        3210    =  Clear   Go Stop

        True/False if button is to be enabled or disabled
        """
        button_setup_list = [] # text, row, column,

        button_setup_list.append(["F", 0, 0, True,])
        button_setup_list.append(["E", 0, 1, True,])
        button_setup_list.append(["D", 0, 2, True,])
        button_setup_list.append(["C", 0, 3, True,])

        button_setup_list.append(["B", 1, 0, True,])
        button_setup_list.append(["A", 1, 1, True,])
        button_setup_list.append(["9", 1, 2, True,])
        button_setup_list.append(["8", 1, 3, True,])

        button_setup_list.append(["7", 2, 0, True,])
        button_setup_list.append(["6", 2, 1, True,])
        button_setup_list.append(["5", 2, 2, True,])
        button_setup_list.append(["4", 2, 3, True,])

        button_setup_list.append(["3", 3, 0, True,])
        button_setup_list.append(["2", 3, 1, True,])
        button_setup_list.append(["1", 3, 2, True,])
        button_setup_list.append(["0", 3, 3, True,])

        # spacer is column 4

        # Function set of buttons. E.g. + - * // =
        button_setup_list.append([F1_TEXT, 0, 5, True,])
        button_setup_list.append([F2_TEXT, 0, 6, True,])
        button_setup_list.append([F3_TEXT, 1, 5, True,])
        button_setup_list.append([F4_TEXT, 1, 6, False,]) # - Subtraction
        button_setup_list.append([F5_TEXT, 2, 5, False,]) # * Multiplication
        button_setup_list.append([F6_TEXT, 2, 6, False,]) # // Division
        #button_setup_list.append([F4_TEXT, 1, 6, True,]) # - Subtraction
        #button_setup_list.append([F5_TEXT, 2, 5, True,]) # * Multiplication
        #button_setup_list.append([F6_TEXT, 2, 6, True,]) # // Division
        button_setup_list.append([F7_TEXT, 3, 5, True,])
        button_setup_list.append([F8_TEXT, 3, 6, True,])

        # spacer is column 7

        # Programming set of buttons. Busy beaver. Plus Go/Stop
        button_setup_list.append([P1_TEXT, 0, 8, True])
        button_setup_list.append([P2_TEXT, 0, 9, True])
        button_setup_list.append([P3_TEXT, 1, 8, True])
        button_setup_list.append([P4_TEXT, 1, 9, True])
        button_setup_list.append([P5_TEXT, 2, 8, True])
        button_setup_list.append([P6_TEXT, 2, 9, True])

        for button_list in button_setup_list:
            self.style.configure("B2A.TButton",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5, font=('Helvetica', 14),)
            self.button_2a = ttk.Button(self.f2b, text=button_list[0], style="B2A.TButton", command=lambda i=button_list[0]: self.calculator_cb(i), width = 5,)
            # Button is either enabled or disabled based on button_list[3] value of True/False.
            if button_list[3]:
                self.button_2a.state(["!disabled"])
            else:
                self.button_2a.state(["disabled"])

            self.button_2a.grid(row=button_list[1], column=button_list[2], sticky="nsew",)

        # Stop and Go are separate as they don't have command callback on click
        self.button_go = ttk.Button(self.f2b, text=P7_TEXT, style="B2A.TButton",)
        self.button_go.grid(row=3, column=8, sticky="nsew",)
        self.button_stop = ttk.Button(self.f2b, text=P8_TEXT, style="B2A.TButton",)
        self.button_stop.grid(row=3, column=9, sticky="nsew",)

        # Add the spacers between sections. Columns 4 and 7
        spacer1 = ttk.Label(self.f2b, text="    ")
        spacer1.grid(row=0, column=4)
        spacer2 = ttk.Label(self.f2b, text="    ")
        spacer2.grid(row=0, column=7)
        spacer3 = ttk.Label(self.f2b, text="    ")
        spacer3.grid(row=0, column=10)

        # Add a speed control in a frame
        self.style.configure("F2B1.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2B1.TFrame.Label", font=('Helvetica', 14),)
        self.f2b1 = ttk.Labelframe(self.f2b, text=F2B1_TEXT, style="F2B1.TFrame", width = 80, height = 200,)
        self.f2b1.grid(row=0, rowspan=4, column=11,  sticky="nsew")

        self.speed = ttk.Scale(self.f2b1, from_=0, to=100,  orient="vertical", command=self.slider_changed)
        self.speed.grid(row=0, column=0)
        # Set the speed to 50 i.e. 50/100. Which is 0.5 + 0.5 = 1 second per state cycle
        #print("self.speed.get():", self.speed.get())
        self.speed.set(50)


    def setup_tape_frame(self):
        """
        Setup the frames inside the Tape Frame (1A)
        """
        pass

        # Array of frames containing an array of labels.
        self.tape_list = ''.join(['_']*(2 * TAPE_RANGE + 1))
        self.frame_list = list(range(-TAPE_RANGE, TAPE_RANGE +1))

        self.tape_labels = []
        self.tape_frames = []
        #print(frame_list)

        self.style.configure("F1AA.TFrame", relief="solid", borderwidth=1,)
        self.style.configure("F1AA.TFrame.Label", font=('Helvetica', 8),  foreground="darkgreen",)
        count = 0

        for index, value in enumerate(self.frame_list): # frame_list = [0,1,2,3,4...]
            # Frame Needs width and height No auto sized. labelanchor- lowercase (nw,n s,e,w) etc.
            self.tape_frames.append(ttk.Labelframe(self.f1a, text=str(value), style="F1AA.TFrame", labelanchor ="s",))
            self.tape_frames[index].grid(row=0, column=index,)

        self.style.configure("TAPE.TLabel", relief="solid" , font=('Helvetica', 35), stipple=0, borderwidth=0, padding=(5))
        self.style.configure("HEAD.TLabel", foreground="red", background="yellow",  relief="solid" , font=('Helvetica', 35), stipple=0, borderwidth=0, padding=(5))

        for index, key in enumerate(self.tape_list):
            if index == TAPE_RANGE:
                self.tape_labels.append(ttk.Label(self.tape_frames[index], text=str(key), style="HEAD.TLabel"))
            else:
                self.tape_labels.append(ttk.Label(self.tape_frames[index], text=str(key), style="TAPE.TLabel"))

            self.tape_labels[index].grid(row=0, column=0, sticky="nswe")

        # Add initial data of 0 at position 10
        self.tape_labels[TAPE_RANGE].config(text="0")


if __name__ == "__main__":
    root = tk.Tk()
    app = Turing(root)
    root.mainloop()

"""
References:

https://python-course.eu/applications-python/turing-machine.php

https://aturingmachine.com/

https://www.youtube.com/watch?v=E3keLeMwfHY

https://sandipanweb.wordpress.com/2020/08/08/simulating-a-turing-machine-with-python-and-executing-programs/

https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/one.html

https://www.britannica.com/technology/Turing-machine

https://plato.stanford.edu/entries/turing-machine/

https://plato.stanford.edu/archives/fall2018/entries/turing-machine/

https://en.wikipedia.org/wiki/David_Hilbert

https://en.wikipedia.org/wiki/Kurt_G%C3%B6del

https://en.wikipedia.org/wiki/Alan_Turing

https://en.wikipedia.org/wiki/Emil_Leon_Post

https://www.newscientist.com/article/mg23130803-200-how-alan-turing-found-machine-thinking-in-the-human-mind/

https://www.wolframscience.com/prizes/tm23/images/Turing.pdf

"""
