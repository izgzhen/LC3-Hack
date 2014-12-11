# How to write an assembler and a simulator {Draft & Research}?


[CPU](http://megalomaniacbore.blogspot.co.uk/2012/05/write-your-own-virtual-cpu-in-c-code.html )

> "Any computer can be programmed to emulate any other computer"
 

We'll actually implement a simple CPU (which  has some short cuts) that can load some numbers, add or subtract them from one another and store the result somewhere.  We'll make this CPU work in a linear sequence going from the first instruction through to the last given and we'll make it report any errors in the instructions.

## A summary about writing a rudimentary virtual CPU
From the article above, we can see that the central points are:

1. It is only a CPU, which can only do some arithmetic operations
2. The CPU will have some registers, for storing operands, indicate overflow or other status, and PC, IR
3. The instructions will be stored in a simple table, which is not necessarily the "memory" we means.

It would be simple, since it is mostly modeling the behavior, rather than structure.

## Look at source code of LC3 again
The LC3 simulator is actually two parts: One is the machines to be simulated, one is the helper functions, such as memory dump etc.

The C code is really messy ... But to analyze it, I will dump down the functions first, and only those as a pure simulator.

I have excerpted the important code in lc3sim.c

Next is lc3.def
