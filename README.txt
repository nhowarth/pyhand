PyHand: An interactive, 3-D wireframe animation of a humanoid hand. 
CIS 192 - Python Programming - Final Project
Nick Howarth <nhowarth@seas.upenn.edu>

Requirements:  
python, pygame

How it works:
A still-frame of the hand model is referred to as a "frame." Each frame is
composed of 21 coordinate points, so the number of lines in the input file must
be a multiple of 21. The program breaks the input file into frames. 
For each frame, each point is projected from 3D to 2D. Lines are then drawn
between the lines to replicate the fingers. 
The hand model can be rotated around 3 axes by pressing certain keys on the 
keyboard (see next section). If there are multiple frames in the input file,
the hand can be animated by pressing the space bar to enable play mode. 
The program will display the motion frame-by-frame at a frame rate of 5 fps
(frame rate can be modified by altering argument to self.clock.tick in run).
Upon reaching the end of the list of joint positions, play mode will again be
disabled until the space bar is pressed again. The user may rotate the hand
regardless of whether play mode is enabled.  

To use:
On the command line, run:  python pyhand.py <hand_coordinate_file>
(Sample:  python pyhand.py hand.txt)

<hand_coordinate_file> must be in following format (spaces not necessary):

I0x, I0y, I0z
I1x, I1y, I1z
I2x, I2y, I2z
I3x, I3y, I3z
M0x, M0y, M0z
... # M1-M3
R0x, R0y, R0z
... # R1-R3
P0x, P0y, P0z
... # P1-P3
T0x, T0y, T0z
T1x, T1y, T1z
T2x, T2y, T2z
W0x, W0y, W0z
W1x, W1y, W1z
... # next frame(s)

where I = index, M = middle, R = ring, P = pinky, T = thumb, W = wrist,
0 = fingertip, 1 = first joint from fingertip, 2 = second joint from fingertip,
3 = 3rd joint from fingertip (N/A for thumb), 
and x, y, and z represent the x-, y-, and z-coordinates of the joint.
Exception: W0 represents the wrist, and W1 represent some point on the forearm.

Once running in pygame environment:
-  Can rotate about x-axis by pressing 'h' / 'l' on the keyboard.
-  Can rotate about y-axis by pressing 'u' / 'n' on the keyboard.
-  Can rotate about z-axis by pressing 'j' / 'k' on the keyboard.
-  Start animation by pressing SPACE bar on the keyboard.

To verify invalid input file format checking, run:
-  python pyhand.py bad1.txt
-  python pyhand.py bad2.txt
