# turing-machine

## A Python/Tkinter GUI based simulator of the Alan Turing *Universal Computing Machine*

## History

*David Hilbert* put forth the most influential list consisting of 23 unsolved problems at the International Congress of Mathematicians in Paris in 1900. In 1928 Hilbert proposed the Entscheidungs problem (decision problem). 

*Alan Mathison Turing*, born 1912, died 1954 (aged 41), was an English mathematician, computer scientist, logician, cryptanalyst, philosopher and theoretical biologist. He studied at University of Cambridge for his BA and MA and Princeton University for his PhD. 

In 1935/36, at the age of 22 and while studing at Cambridge, Alan Turing wanted to show that Hilbert’s view of the Entscheidungsproblem was not correct. To do this, he first needed to give a definition of an effective procedure, or algorithm. This he did through his definition of the hypothetical computing machines that we now call Turing machines. His 38 page paper, [*On Computable Numbers, With an Application to the Entscheidungsproblem*](https://www.wolframscience.com/prizes/tm23/images/Turing.pdf), which was published in the *Proceedings of the London Mathematical Society* journal in two parts, the first on 30 November and the second on 23 December.

*Emil Leon Post* (b. 1897 – d. 1954) was an American mathematician and logician. He developed a mathematical model of computation that was essentially equivalent to the Turing machine model. This model is sometimes called "Post's machine" or a Post–Turing machine.

The python/tkinter simulator is likely to be based around a combination of both Turing and Post hypothetical machines.

## Python/Tkinter GUI Turing Simulator.

* The simulator allows each frame on the tape to contain three symbols: Zero, One, or blank (which is indicated with an underscore.) When the tape frames contain multiple sets of binary data, then the blank frame acts as a delimiter to separate the data.

* The position of the read/write head on the simulator does not move. It is the tape that moves one frame at a time, left or right, over the read/write head. As this is not a physical machine, requiring frames of the tape to be erased, there is no "erase" head. To erase a zero or one from a frame, then an underscore is written to that frame.

* In programming the simulator, then a frame is read. What is read could be either zero, one or underscore/blank. Depending on what is read, then three separate commands can be written for each condition. These commands are: 1. What to write to the frame of the tape. 2. Which direction to move the tape after writing. 3. Which state in the programming code to jump to next.


* 
