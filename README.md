Mightex CMOS Camera Python Program and Arduino Laser Diode Controller

This Python script interfaces with the Mightex SCE-BG04-U CMOS and controls
and external Arduino which switches three laser diodes connected to active
low drivers.

The software consists of two pieces, the main control program and the Arduino
software which acts as a host to accept commands over serial from the main
program.

The main program was created using the Mightex USB SDK.
