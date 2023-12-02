#!/usr/bin/env python3
#
# turing_machine.py
# Requires: turing_program.py
#
# Using a GUI simulate a Turing machine.
# Includes a calculator style user interface to the Turing machine.
# Code written for the Turing machine resides in turing_program.py
#
# Ian Stewart 2023-11-22
#
# TODO:
# Last line of code become a comment that stores parameters. Thus don't need a separate config file.
# Two operand, one operand, operator only, etc. paths

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

# Import a0ddition code as a dictionary. Eg.
# {(0, 'c'): 'State 0:  Move right to end of first block of data',
# (0, 0): (0, 0, 'r'), (0, 1): (1, 1, 'r'), (0, '_'): (1, '_', 'r'),

# Load functions
addition = turing_program.function_addition()
#print(addition)

bb3 = turing_program.function_busy_beaver_3()
bb4 = turing_program.function_busy_beaver_4()
dec = turing_program.function_dec()
inc = turing_program.function_inc()
#print(bb3)
#print(addition)

# Label Constants

TITLE = "Turing Machine - Calculator"
F1_TEXT = "Turing Machine"
F2_TEXT = "Calculator Simulator Interface"

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
        #self.setup_testing_move_tape_frame()
        self.setup_calculator_input_frame()
        #self.setup_frames()
        #self.setup_button()
        #self.update_hex_bin_dec_display()
        self.setup_information_display()

        self.reset_tape()

        # GUI should now be displayed. Read for data/function input.
        self.update()
        #self.update_idletasks()



        '''
        update(self)
        Enter event loop until all pending events have been processed by Tcl.

        update_idletasks(self)
        Enter event loop until all idle callbacks have been called.
        '''
        #time.sleep(1)

        """

        initial_data = '1_1' # initial data 1 space 1 or 2 space 2, etc.
        initial_data = '11_10'
        #initial_data = '_'
        initial_data = '11111'

        program = dec #inc #dec #addition #bb4 #bb4 # bb3 addition
        """
        #tm = TuringMachine(program, initial_data)
        #tm.run_turing_program()  # Can pass a max iteration value
        # 10010 H

        #self.setup_turing_machine(program, initial_data )

        #self.run_turing_program()

        # Provide autostart for debugging.
        #self.auto_start()


    def auto_start(self):
        """
        When Turing_machone.py is launched, then it starts automatically in
        performing a function.
        E.g. Selects addition functionand applies operand data.
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


    #def __init__(self, program, initial_data, state=0):
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

        # Which function to perform???
        #self.trf = addition
        #self.trf = bb #turing_program.function_busy_beaver_4()
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



    def move_tape(self): #, direction):
        """
        TODO: Rename to tape_update

        self.tape_dict appears to move right or left one position
        self.tape_labels display a new section of self.tape_dict
        and self.tape_frames get renumbered.
        Total of 21 labels.
        direction = "L" or "R" from turing instruction
        """

        #if direction.lower() == "l":
        #    self.head_position -= 1
        #else:
        #    self.head_position += 1

        # -11 to +11 of head position. index 0 to 20
        for index, i in enumerate(range(self.head_position - TAPE_RANGE, self.head_position + TAPE_RANGE + 1)):
            self.tape_frames[index].config(text=str(i))
            self.tape_labels[index].config(text=self.tape_dict[i])


    def setup_frame_1(self):
        """
        Setup the Turing frames.
        1. Main Turing set of frames
        1A. Turing Tape display
        1B. Turing Programming information
        2. Turing Calculator style interface.
        """
        #style = ttk.Style()

        # Configure Frame 1 - Main Turing Machine Frame
        self.style.configure("F1.TFrame", relief="solid", borderwidth=2,  padding=(5,5,5,5), labelmargins=5) #  padding=(5,5),
        self.style.configure("F1.TFrame.Label", font=('Helvetica', 14), ) # ,foreground="blue<--Changes frame label colour"
        #f1 = ttk.Labelframe(root, text=F1_TEXT, style="F1.TFrame", width = 800, height = 200,)self.parent
        f1 = ttk.Labelframe(self.parent, text=F1_TEXT, style="F1.TFrame", width = 800, height = 200,)
        f1.grid(row=0, column=0,  sticky="nsew", padx=5, pady=5) # padx=(20, 10), pady=(20, 10),padx=(5, 5), pady=(5, 5),

        # Configure Frame 1A - Tape Display
        self.style.configure("F1A.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F1A.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F1A.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F1A.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f1a = ttk.Labelframe(f1, text=F1A_TEXT, style="F1A.TFrame", width = 800, height = 200,)
        self.f1a.grid(row=0, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        # Configure Frame 1B - Code Information Display
        self.style.configure("F1B.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5),labelmargins=5)# labelmargins=20)
        self.style.configure("F1B.TFrame.Label", font=('Helvetica', 14), )
        #style.configure("F1B.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #style.configure("F1B.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f1b = ttk.Labelframe(f1, text=F1B_TEXT, style="F1B.TFrame", width = 800, height = 200,)
        self.f1b.grid(row=1, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        # Configure Frame 1C - Code Comment
        self.style.configure("F1C.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5),labelmargins=5)# labelmargins=20)
        self.style.configure("F1C.TFrame.Label", font=('Helvetica', 14), )
        #style.configure("F1B.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #style.configure("F1B.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f1c = ttk.Labelframe(f1, text=F1C_TEXT, style="F1C.TFrame", width = 800, height = 200,)
        self.f1c.grid(row=2, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        # Configure Frame 2 - Calculator Style Input
        #self.style.configure("F2.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.style.configure("F2.TFrame", relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)
        self.style.configure("F2.TFrame.Label", font=('Helvetica', 14),)
        f2 = ttk.Labelframe(self.parent, text=F2_TEXT, style="F2.TFrame", width = 800, height = 200,)
        f2.grid(row=1, column=0,  sticky="nsew", padx=5, pady=5) # padx=(5, 5), pady=(5, 5),

        # Configure Frame 2A - Calculator Display
        self.style.configure("F2A.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2A.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F2A.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2A.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f2a = ttk.Labelframe(f2, text=F2A_TEXT, style="F2A.TFrame", width = 800, height = 200,)
        self.f2a.grid(row=0, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        # Configure Frame 2A1 - Hex Display
        self.style.configure("F2A1.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2A1.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F2A1.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2A1.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f2a1 = ttk.Labelframe(self.f2a, text=F2A1_TEXT, style="F2A1.TFrame", width = 300, height = 200,)
        self.f2a1.grid(row=0, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        self.label_hex = ttk.Label(self.f2a1, text="", font=('Helvetica', 14))
        self.label_hex.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2A2 - Binary Display
        self.style.configure("F2A2.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2A2.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F2A2.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2A2.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f2a2 = ttk.Labelframe(self.f2a, text=F2A2_TEXT, style="F2A2.TFrame", width = 300, height = 200,)
        self.f2a2.grid(row=0, column=1,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        self.label_binary = ttk.Label(self.f2a2, text="", font=('Helvetica', 14))
        self.label_binary.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2A3 - Decimal Display
        self.style.configure("F2A3.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2A3.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F2A3.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2A3.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f2a3 = ttk.Labelframe(self.f2a, text=F2A3_TEXT, style="F2A2.TFrame", width = 300, height = 200,)
        self.f2a3.grid(row=0, column=2,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        self.label_decimal = ttk.Label(self.f2a3, text="", font=('Helvetica', 14))
        self.label_decimal.grid(row=0, column=0, stick="nsew")

        # Configure Frame 2B - Calculator Input
        self.style.configure("F2B.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5)# labelmargins=20)
        self.style.configure("F2B.TFrame.Label", font=('Helvetica', 14),)
        #self.style.configure("F2B.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F2B.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f2b = ttk.Labelframe(f2, text=F2B_TEXT, style="F2B.TFrame", width = 800, height = 200,)
        self.f2b.grid(row=1, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),


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
        """
        button_setup_list = [] # text, row, column,

        button_setup_list.append(["F", 0, 0])
        button_setup_list.append(["E", 0, 1])
        button_setup_list.append(["D", 0, 2])
        button_setup_list.append(["C", 0, 3])

        button_setup_list.append(["B", 1, 0])
        button_setup_list.append(["A", 1, 1])
        button_setup_list.append(["9", 1, 2])
        button_setup_list.append(["8", 1, 3])

        button_setup_list.append(["7", 2, 0])
        button_setup_list.append(["6", 2, 1])
        button_setup_list.append(["5", 2, 2])
        button_setup_list.append(["4", 2, 3])

        button_setup_list.append(["3", 3, 0])
        button_setup_list.append(["2", 3, 1])
        button_setup_list.append(["1", 3, 2])
        button_setup_list.append(["0", 3, 3])

        # spacer is column 4

        button_setup_list.append(["Inc",0,5])
        button_setup_list.append(["Dec",0,6])
        button_setup_list.append(["+",1,5])
        button_setup_list.append(["-",1,6])
        button_setup_list.append(["*",2,5])
        button_setup_list.append(["//",2,6])
        button_setup_list.append(["=",3,5])
        button_setup_list.append(["Clear",3,6])

        # spacer is column 7

        button_setup_list.append(["P1",0,8])
        button_setup_list.append(["P2",0,9])
        button_setup_list.append(["P3",1,8])
        button_setup_list.append(["P4",1,9])
        button_setup_list.append(["P5",2,8])
        button_setup_list.append(["P6",2,9])



        for button_list in button_setup_list:
            self.style.configure("B2A.TButton",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5, font=('Helvetica', 14),)
            self.button_2a = ttk.Button(self.f2b, text=button_list[0], style="B2A.TButton", command=lambda i=button_list[0]: self.calculator_cb(i), width = 5,) # height = 25,)
            self.button_2a.grid(row=button_list[1], column=button_list[2], sticky="nsew",)

        # Stop and Go are separate as they don't have
        #button_setup_list.append(["Go",3,8])
        #button_setup_list.append(["Stop",3,9])
        self.button_go = ttk.Button(self.f2b, text="Go", style="B2A.TButton",)
        self.button_go.grid(row=3, column=8, sticky="nsew",)
        self.button_stop = ttk.Button(self.f2b, text="Stop", style="B2A.TButton",)
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

        #current_value = tk.IntVar()  #DoubleVar(),  variable=current_value, orient="vertical"
        #self.speed = ttk.LabeledScale(self.f2b1, from_=0, to=100, command=self.slider_changed)
        self.speed = ttk.Scale(self.f2b1, from_=0, to=100,  orient="vertical", command=self.slider_changed)
        self.speed.grid(row=0, column=0)
        # Set the speed to 50 i.e. 50/100. Which is 0.5 + 0.5 = 1 second per state cycle
        #print("self.speed.get():", self.speed.get())
        self.speed.set(50)

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


    def calculator_cb(self, button):
        """
        #print("got here")
        #print(dir(button))
        print(button)  # 2,3 4... etc label on the button
        #print(dir(self.button_2a.config(items)))
        FEDC    Inc Dec    P1 P2
        BA98    +   -      P3 P4
        7654    *   //     P5 P6
        3210    =  Clear   Go Stop

        # An operand is also referred to as "one of the inputs (quantities) for an operation"
        self.is_operand_1 = False
        self.is_operand_2 = False
        self.is_operator = False

        # TODO: Catagories: E.g. Addition is 2 operand, Dec is one operand. Busy Beaver is 0 operands.
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

        elif button in ["Inc", "Dec",]:
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


        elif button in ["+", "-", "*", "//",]:
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





        elif button in ["P1", "P2", "P3", "P4","P5", "P6" ]:
            print("button is function {}".format(button))

        elif button == "Clear":
            print("button is command: {}".format(button))
            self.reset_tape() # Also clears variables.


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

        self.style.configure("F1AA.TFrame", relief="solid", borderwidth=1,) # padding=(5), ) #width = 10, height = 10, labelmargins=20)
        self.style.configure("F1AA.TFrame.Label", font=('Helvetica', 8),  foreground="darkgreen",)
        count = 0

        for index, value in enumerate(self.frame_list): # frame_list = [0,1,2,3,4...]
            # Frame Needs width and height No auto sized. labelanchor- lowercase (nw,n s,e,w) etc.
            self.tape_frames.append(ttk.Labelframe(self.f1a, text=str(value), style="F1AA.TFrame", labelanchor ="s",)) # width = 30, height = 40, )) #.Label" ))

            # This works
            #tape_frames[count].grid(row=1, column = count + 1)
            #count +=1
            # And this works...
            self.tape_frames[index].grid(row=0, column=index,)



        # This works
        self.style.configure("TAPE.TLabel", relief="solid" , font=('Helvetica', 35), stipple=0, borderwidth=0, padding=(5)) #, 5),) ## bordercolor="green") # Bordercolor doesn't work

        #style.configure("TAPE.TLabel", relief="solid" , font=('Helvetica', 25), stipple=0, borderwidth=1, padding=(5)) #, 5),) ## bordercolor="green") # Bordercolor doesn't work
        #style.configure("TAPE.TLabel", foreground="yellow", background="red",  relief="solid" , font=('Helvetica', 25), stipple=0, borderwidth=1, padding=(5)) #, 5),) ## bordercolor="green") # Bordercolor doesn't work

        self.style.configure("HEAD.TLabel", foreground="red", background="yellow",  relief="solid" , font=('Helvetica', 35), stipple=0, borderwidth=0, padding=(5)) #, 5),)
        #style.configure("HEAD.TLabel", foreground="red", background="yellow",  relief="solid" , font=('Helvetica', 25), stipple=0, borderwidth=1, padding=(5)) #, 5),)
        for index, key in enumerate(self.tape_list):
            if index == TAPE_RANGE:
                # Was f1aa
                self.tape_labels.append(ttk.Label(self.tape_frames[index], text=str(key), style="HEAD.TLabel"))
            else:
                self.tape_labels.append(ttk.Label(self.tape_frames[index], text=str(key), style="TAPE.TLabel"))


            self.tape_labels[index].grid(row=0, column=0, sticky="nswe")

        #for index, key in enumerate(tape_frames()):
        #    key.grid(row=0, column = 0)

        # Add initial data of 0 at position 10
        self.tape_labels[TAPE_RANGE].config(text="0")

    '''
    def setup_testing_move_tape_frame(self):
        """
        F3_TEXT = "Testing"
        F4_TEXT = "Coding"

                    # ←→ ◄► ᐸᐳ←→ ⇐⇒ <>
        F3A_BUTTON_1_TEXT = "◄"
        F3A_BUTTON_2_TEXT = "►"


        test if the tape can be moved OK
        Insert a Frame with two arrow buttons for tape direction.
        Setup in self.f3
        Uses: F3A_BUTTON_2_TEXT F3A_BUTTON_3_TEXT
        self.f3a = frame for direction arrows
        """
        pass
        # Configure Frame 3A - For Direction Arrows
        self.style.configure("F3A.TFrame",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5,) # font=('Helvetica', 14),)
        self.style.configure("F3A.TFrame", foreground="yellow", background="orange",  relief="solid", borderwidth=2, padding=(5),)# labelmargins=20)
        #self.style.configure("F1A.TFrame.Label", font=('Helvetica', 14), foreground="yellow", background="blue",)
        self.f3a = ttk.Labelframe(self.f3, text=F3A_TEXT, style="F3A.TFrame",) # width = 800, height = 200,)
        self.f3a.grid(row=0, column=0,  sticky="nsew") # padx=(5, 5), pady=(5, 5),

        # Left direction button
        self.style.configure("B3A.TButton",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5, font=('Helvetica', 14),)
        self.button_3a = ttk.Button(self.f3a, text=F3A_BUTTON_1_TEXT, style="B3A.TButton", command=self.test_move_tape) # width = 80,) # height = 20,)
        self.button_3a.grid(row=0, column=0, sticky="nsew",)

        # Right direction button
        self.style.configure("B3A.TButton",  relief="solid", borderwidth=2, padding=(5,5,5,5), labelmargins=5, font=('Helvetica', 14),)
        self.button_3b = ttk.Button(self.f3a, text=F3A_BUTTON_2_TEXT, style="B3A.TButton", command=self.test_move_tape )# width = 80,) # height = 20,)
        self.button_3b.grid(row=0, column=1, sticky="nsew",)

    '''
#===== Junk Code =====
    def setup_frames(self):
        # frame for button --------------- frame 0 / button
        self.button_frame0 = ttk.LabelFrame(self, text="Azure dark Theme App", padding=(20, 10))
        self.button_frame0.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

    def setup_button(self):
        self.accentbutton = ttk.Button(
        self.button_frame0,
        text="CLick to open new window",
        style="Accent.TButton",
        command=lambda: self.new_window(Win2)
        )
        self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")


    def new_window(self,winclass):
        if self.win2_status == 0:
            try:
                if self.win2.status == 'normal': # if it's not created yet
                    self.win2.focus_force()
            except:
                    self.win2 = tk.Toplevel(root) # create
                    Win2(self.win2) # populate
                    self.win2_status = 1

class Win2:
    def __init__(self, _root):
        self.root = _root
        self.root.geometry("300x300+500+200")
        self.root["bg"] = "navy"
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        print("Window destroyed")
        app.win2_status = 0
        self.root.destroy()

#===== End Junk Code ======


if __name__ == "__main__":
    root = tk.Tk()
    app = Turing(root)


    """
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    """
    root.mainloop()


"""
dir(self.parent)

['_Misc__winfo_getint
_Misc__winfo_parseitem
__class__
__delattr__
__dict__
__dir__
__doc__
__eq__
__format__
__ge__
__getattr__
__getattribute__
__getitem__
__gt__
__hash__
__init__
__init_subclass__
__le__
__lt__
__module__
__ne__
__new__
__reduce__
__reduce_ex__
__repr__
__setattr__
__setitem__
__sizeof__
__str__
__subclasshook__
__weakref__
_bind
_configure
_displayof
_getboolean
_getconfigure
_getconfigure1
_getdoubles
_getints
_grid_configure
_gridconvvalue
_last_child_ids
_loadtk
_nametowidget
_noarg_
_options
_register
_report_exception
_root
_subst_format
_subst_format_str
_substitute
_tclCommands
_tkloaded
_w
_windowingsystem
after
after_cancel
after_idle
anchor
aspect
attributes
bbox
bell
bind
bind_all
bind_class
bindtags
cget
children
client
clipboard_append
clipboard_clear
clipboard_get
colormapwindows
columnconfigure
command
config
configure
deiconify
deletecommand
destroy
event_add
event_delete
event_generate
event_info
focus
focus_displayof
focus_force
focus_get
focus_lastfor
focus_set
focusmodel
forget
frame
geometry
getboolean
getdouble
getint
getvar
grab_current
grab_release
grab_set
grab_set_global
grab_status
grid
grid_anchor
grid_bbox
grid_columnconfigure
grid_location
grid_propagate
grid_rowconfigure
grid_size
grid_slaves
group
iconbitmap
iconify
iconmask
iconname
iconphoto
iconposition
iconwindow
image_names
image_types
keys
lift
loadtk
lower
mainloop
manage
master
maxsize
minsize
nametowidget
option_add
option_clear
option_get
option_readfile
overrideredirect
pack_propagate
pack_slaves
place_slaves
positionfrom
propagate
protocol
quit
readprofile
register
report_callback_exception
resizable
rowconfigure
selection_clear
selection_get
selection_handle
selection_own
selection_own_get
send
setvar
size
sizefrom
slaves
state
title
tk
tk_bisque
tk_focusFollowsMouse
tk_focusNext
tk_focusPrev
tk_setPalette
tk_strictMotif
tkraise
transient
unbind
unbind_all
unbind_class
update
update_idletasks
wait_variable
wait_visibility
wait_window
waitvar
winfo_atom
winfo_atomname
winfo_cells
winfo_children
winfo_class
winfo_colormapfull
winfo_containing
winfo_depth
winfo_exists
winfo_fpixels
winfo_geometry
winfo_height
winfo_id
winfo_interps
winfo_ismapped
winfo_manager
winfo_name
winfo_parent
winfo_pathname
winfo_pixels
winfo_pointerx
winfo_pointerxy
winfo_pointery
winfo_reqheight
winfo_reqwidth
winfo_rgb
winfo_rootx
winfo_rooty
winfo_screen
winfo_screencells
winfo_screendepth
winfo_screenheight
winfo_screenmmheight
winfo_screenmmwidth
winfo_screenvisual
winfo_screenwidth
winfo_server
winfo_toplevel
winfo_viewable
winfo_visual
winfo_visualid
winfo_visualsavailable
winfo_vrootheight
winfo_vrootwidth
winfo_vrootx
winfo_vrooty
winfo_width
winfo_x
winfo_y
withdraw
wm_aspect
wm_attributes
wm_client
wm_colormapwindows
wm_command
wm_deiconify
wm_focusmodel
wm_forget
wm_frame
wm_geometry
wm_grid
wm_group
wm_iconbitmap
wm_iconify
wm_iconmask
wm_iconname
wm_iconphoto
wm_iconposition
wm_iconwindow
wm_manage
wm_maxsize
wm_minsize
wm_overrideredirect
wm_positionfrom
wm_protocol
wm_resizable
wm_sizefrom
wm_state
wm_title
wm_transient
wm_withdraw']

"""

"""
https://python-course.eu/applications-python/turing-machine.php

Formal Definition of a Turing machine

A deterministic Turing machine can be defined as a 7-tuple

M = (Q, Σ, Γ, δ, b, q0, qf)

with

    Q is a finite, non-empty set of states
    Γ is a finite, non-empty set of the tape alphabet
    Σ is the set of input symbols with Σ ⊂ Γ
    δ is a partially defined function, the transition function:
    δ : (Q \ {qf}) x Γ → Q x Γ x {L,N,R}
    b ∈ &Gamma \ Σ is the blank symbol
    q0 ∈ Q is the initial state
    qf ∈ Q is the set of accepting or final states


Example: Binary Complement function

Let's define a Turing machine, which complements a binary input on the tape,
i.e. an input "1100111" e.g. will be turned into "0011000".
Σ = {0, 1}
Q = {init, final}
q0 = init
qf = final

Function Definition     Description
δ(init,0) = (init, 1, R)    If the machine is in state "init" and a 0 is read by the head, a 1 will be written, the state will change to "init" (so actually, it will not change) and the head will be moved one field to the right.
δ(init,1) = (init, 0, R)    If the machine is in state "init" and a 1 is read by the head, a 0 will be written, the state will change to "init" (so actually, it will not change) and the head will be moved one field to the right.
δ(init,b) = (final, b, N)   If a blank ("b"), defining the end of the input string, is read, the TM reaches the final state "final" and halts.

# https://sandipanweb.wordpress.com/2020/08/08/simulating-a-turing-machine-with-python-and-executing-programs/
     for line in program.splitlines():
       s, a, r, d, s1 = line.split(' ')
       self.trf[s,a] = (r, d, s1)

Write in python dictionary format?:
self.transiton_function[state_initial, a] = (state_accepting, r ,direction)
self.transiton_function[state_initial, read] = (state_accepting, write, direction)

State   Symbol Read     Write Instruction   Move Instruction    Next State
δ(S1,       0)      = ( 1,                         R              S2)

https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/one.html
https://www.britannica.com/technology/Turing-machine

he proved in his seminal paper “On Computable Numbers, with an Application to the Entscheidungsproblem [‘Halting Problem’]” (1936) that no such universal mathematical solver could ever exist.

In 1936 an English mathematician, Alan Mathison Turing, in a paper published in the Proceedings of the London Mathematical Society (“On Computable Numbers with an Application to the Entscheidungsproblem”),
https://plato.stanford.edu/entries/turing-machine/

A Turing machine then, or a computing machine as Turing called it

Turing’s original definition is a machine capable of a finite set of configurations q1,…,qn (the states of the machine, called m-configurations by Turing). It is supplied with a one-way infinite and one-dimensional tape divided into squares each capable of carrying exactly one symbol. At any moment, the machine is scanning the content of one square r which is either blank (symbolized by S0) or contains a symbol S1,…,Sm with S1=0 and S2=1.

 Thus, Post introduced a modified version of the Turing machine. The most important differences between Post’s and Turing’s definition are:

    Post’s Turing machine, when in a given state, either prints or moves and so its transition rules are more ‘atomic’ (it does not have the composite operation of moving and printing).

 Note that Post’s reformulation of the Turing machine is very much rooted in his Post 1936. (Some of) Post’s modifications of Turing’s definition became part of the definition of the Turing machine in standard works such as Kleene 1952 and Davis 1958.

  Today, standard definitions of Turing machines are, in some respects, closer to Post’s Turing machines than to Turing’s machines.

Around 1920–21 Emil Post developed different but related types of production systems in order to develop a syntactical form which would allow him to tackle the decision problem for first-order logic. One of these forms are Post canonical systems C which became later known as Post production systems.


Amongst Turing’s contributions which are today considered as pioneering, the 1936 paper on Turing machines stands out as the one which has the largest impact on computer science. However, recent historical research shows also that one should treat the impact of Turing machines with great care and that one should be careful in retrofitting the past into the present.

https://en.wikipedia.org/wiki/Emil_Leon_Post
Emil Leon Post
Emil L Post

Turing, A.M., 1936–7, “On Computable Numbers, With an Application to the Entscheidungsproblem”, Proceedings of the London Mathematical Society, s2-42: 230–265; correction ibid., s2-43: 544–546 (1937). doi:10.1112/plms/s2-42.1.230 and doi:10.1112/plms/s2-43.6.544

https://plato.stanford.edu/archives/fall2018/entries/turing-machine/

 5-tuple formulation

A common way to describe Turing machines is to allow the machine to both write and move its head in the same transition. This formulation requires the 4-tuples of the original formulation to be replaced by 5-tuples

    ⟨ State0, Symbol, Statenew, Symbolnew, Move ⟩

where Symbolnew is the symbol written, and Move is one of « and ».

Again, this additional freedom does not result in a new definition of Turing-computable. For every one of the new machines there is one of the old machines with the same properties.



Turing's principal papers appear amidst those of Gödel, Church, Post and others. T

Initials AMT


https://aturingmachine.com/

https://www.youtube.com/watch?v=E3keLeMwfHY

DIsplay leds: State Position Step / Erase Write Read
(Erase state not noramlly shown as a 1 overwrites a 0, etc.


Issue with phydicsl machine is that the 3 heads (read/write/erase) are not all at one position.

https://www.newscientist.com/article/mg23130803-200-how-alan-turing-found-machine-thinking-in-the-human-mind/



    University of Cambridge (BA, MA)
    Princeton University (PhD)



In mid-April 1936
IN 1935, Alan Turing set out to build a reputation by outflanking the world’s leading mathematician. Turing was 22 years old, and a new fellow at Cambridge. His target, David Hilbert, was the venerated University of Göttingen professor who had single-handedly set the research agenda for 20th-century mathematics.

 how Turing dashed one of Hilbert’s great ambitions with a masterful proof – in the course of which he inadvertently invented the modern computer.

https://en.wikipedia.org/wiki/David_Hilbert
Hilbert died in 1943

Hilbert put forth the most influential list consisting of 23 unsolved problems at the International Congress of Mathematicians in Paris in 1900.

 In this paper, Turing reformulated Kurt Gödel's 1931 results on the limits of proof and computation, replacing Gödel's universal arithmetic-based formal language with the formal and simple hypothetical devices that became known as Turing machines. The Entscheidungsproblem (decision problem) was originally posed by German mathematician David Hilbert in 1928.

 This paper has been called "easily the most influential math paper in history".[55]

==
 Turing wanted to show that Hilbert’s view of the Entscheidungsproblem was not correct.
 To recap: He first needed to give a definition of an effective procedure, or algorithm.
 This he did through his definition of what we now call Turing machines.

==
Gödel's work

Hilbert and the mathematicians who worked with him in his enterprise were committed to the project. His attempt to support axiomatized mathematics with definitive principles, which could banish theoretical uncertainties, ended in failure.

https://en.wikipedia.org/wiki/Kurt_G%C3%B6del

Gödel demonstrated that any non-contradictory formal system, which was comprehensive enough to include at least arithmetic, cannot demonstrate its completeness by way of its own axioms. In 1931 his incompleteness theorem showed that Hilbert's grand plan was impossible as stated. The second point cannot in any reasonable way be combined with the first point, as long as the axiom system is genuinely finitary.


https://www.wolframscience.com/prizes/tm23/images/Turing.pdf

Hilbertian Entscheidungsproblem

Turing's statement still implies five atomic operations. At a given instruction (m-configuration) the machine:

    observes the tape-symbol underneath the head
    based on the observed symbol goes to the appropriate instruction-sequence to use
    prints symbol Sj or erases or does nothing
    moves tape left, right or not at all
    goes to the final m-configuration for that symbol

 Hao Wang
Wang (1957, but presented to the ACM in 1954) is often cited (cf. Minsky (1967), p. 200) as the source of the "program formulation" of binary-tape Turing machines using numbered instructions from the set

    write 0
    write 1
    move left
    move right
    if scanning 0 then go to instruction i
    if scanning 1 then go to instruction j

From wikipedia of Turing...

Between the springs of 1935 and 1936, at the same time as Church, Turing worked on the decidability of problems, starting from Godel's incompleteness theorems.

Finally, on 28 May of that year, he finished and delivered his 36-page paper for publication called "On Computable Numbers, with an Application to the Entscheidungsproblem".[53] It was published in the Proceedings of the London Mathematical Society journal in two parts, the first on 30 November and the second on 23 December


In this paper, Turing reformulated Kurt Gödel's 1931 results on the limits of proof and computation, replacing Gödel's universal arithmetic-based formal language with the formal and simple hypothetical devices that became known as Turing machines. The Entscheidungsproblem (decision problem) was originally posed by German mathematician David Hilbert in 1928. Turing proved that his "universal computing machine" would be capable of performing any conceivable mathematical computation if it were representable as an algorithm. He went on to prove that there was no solution to the decision problem by first showing that the halting problem for Turing machines is undecidable: it is not possible to decide algorithmically whether a Turing machine will ever halt. This paper has been called "easily the most influential math paper in history".[55]

====

#style = ttk.Style()
# https://pythonprogramming.altervista.org/tkinter-open-a-new-window-and-just-one/
# https://www.meetup.com/nzpug-hamilton/events/294627541/



"""
