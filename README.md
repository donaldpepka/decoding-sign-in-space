# decoding-sign-in-space
This repository contains code that replicates the solution to SETI's [A Sign in Space](https://asignin.space/) project's decoding phase. I will emphasize that I did not find the original solution, but have simply reproduced it out of curiosity and enjoyment.

The original, encrypted message can be found in [data17.txt](https://github.com/donaldpepka/decoding-sign-in-space/blob/main/data17.txt). The decryption algorithm is a Margolus neighborhood Block Cellular Automaton. At each step, each 2-by-2 block rotates counter-clockwise twice if and only if it contains 1 "live" cell (in this case, a cell set to 1 in the encrypted message). This repeats for 6,625 steps. The file [Decoder.py](https://github.com/donaldpepka/decoding-sign-in-space/blob/main/Decoder.py) does all of the lifting: it formats the raw message, runs and animates the BCA, and saves each time step as an image file. These images may then be turned into an animated .gif by running [animation in space.py](https://github.com/donaldpepka/decoding-sign-in-space/blob/main/animation%20in%20space.py).

For viewing purposes, the original and final message are included below.

![Original message; resembles a star field or constellation with five star clusters](https://github.com/donaldpepka/decoding-sign-in-space/blob/main/images/sign_0.png?raw=true)

![Final message; resembles an organic compound of some sort, with five molecules](https://github.com/donaldpepka/decoding-sign-in-space/blob/main/images/sign_6625.png?raw=true)
