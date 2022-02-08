# photons-game

## The game

This is a sandbox game I wrote 3.5 years ago using Python and Tkinter, when I was only starting to program.
The game lets you build an optical circuit.
You can make a Turing complete system out of simple building blocks such as laser beams and mirrors. For examples, take a look at `screenshots/`.


The code is not very well-written, pretty convoluted, and amazingly CPU-hungry.
I'm releasing this for posterity to see if I improved over the years : - )

P.S. This README is modern, I didn't bother writing documentation back then!

## How to run the simulator

0. Make sure you have Python 3 installed (any modern version will do)
1. Clone the repo
2. Navigate into the repo folder
3. Run `python3 phoSim.py`
4. You should see a file selection window. Pick the `logic_demo_gates.pickle` file.
5. Use the arrow keys to navigate around the field. Navigate to the bottom to see a full adder circuit

## How to run the editor

6. Run `python3 phoEdit.py`
7. You will see a window prompting you to select a board size. Just click "Create"
8. Press Left mouse button to place a block
9. Press Right mouse button to place a block
10. Press `R` to rotate a block under the cursor
11. Select `Libraries` -> `Change block type` to change the block type
12. Try recreating some of the logic gates
13. Select `File` -> `Save` to save the level to a file
14. Close the editor. Now you can open the level in the simulator
