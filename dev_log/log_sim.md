LC-3 Simulator

Basic Component:
* Memory
* ALU
* Clock
* Control Signal

How to implement?
* Take full adventage of class
* Construct standard parts first
* Use interface similar to data path sheet


Dev Note 1:
I have implement a bunch of "basic ideas" of LC3 architecture. But I haven't fully used the basic property of Python's OOP yet.
I will try to implement the idea of "buffer", "bus" and "clock" next time

Dev Note 2:
I have implement the "Wires", "Buffer" and "Bus". Next step is a clock, which can sync all binded object through calling (which is different from real world) , like

for w in wires:
	w.write('1') # Every calling can be viewd as a clock cycle

the wire is a special type, which don't call 'write' of output but 'sync' of output

Dev Note 3:
The bus structure is done. Now you need to write the instruction loader and FSM, utilizing the six phases you'be written. First is FSM, this will be very similar to the Verilog description of LC3. 

Dev Note 4:
I faced some trouble in incoporating the FSM into the simulator's core. The main problem is that I can't come up a good plan of how to split and serialize the operations in the FSM of LC-3.

Maybe you should first do some virtual wiring, like wiring ALU to DR, SR and Op2, wiring fetchOperand to ALU's output, wiring fetch operand to IMM of IR and a virtual register file (maybe a class wrapping the register and provide some buffer and wring ports. Try this.)

The next step is clear, try some simple data movement instruction implementation, as well as control flow oens. Then reconstruct the code, so that your LC would be too big.

Try to decompose the different modules into seperate ones only prividing standard "bits interfaces". Utilize hte buffer, bus, wires to write a more generic ones.

You computer class should only contains loading modules, connect modules, config modules, drive modules and load instructions into memory.

Dev Note 5:
This night, I will extend the use of wire, trying to standardize the interface between different modules, and write a small document on this. But first, I will do some exercises.

Interface Purposal:

Now I have Bus, Buffer, Wires and Driver, four kinds of interfaces. In my opinion, they should be defined as following:

1. 'Bus' : with a fixed width, connected to different major modules in the system. Can be set to be written by one "speaker" and listened by unlimited "listener". Having a sole set of data, act passively (be written or read)

2. 'Buffer' : Used for buffer the input signal before producing any result. The result is instantly written to the output wires (prabably a combinatoral circuit like ALU). The 'data' will refresh every time the input wire's data changes (passively or actively? I can't define clearly now). The 'sync' will be connected to a 'driver' line, which is in turn hubbed to the 'Clock'. Every time the 'clock' steps, the 'sync' will be triggered, and the 'data' will be sent out. (another instant signal)

3. 'Wires' : Commonly used to connect different part, mostly 'instantly', it can be written passively, and when written, it will write the data down the calling chain.

4. 'Driver' : specially connect between a clock and a device. Everytime a '1' is written to the driver wire, it will trigger the named sync method of the deviced it is connected to. It only calls, not transmitting any data.

First, let us map the data or signal transmitting process of our model.

1. Wire:
	The wire is anything only can hold or transmit (or both) data, not processing. It be defined by its data pool (optinal) , input(unique) and output(pool), as well as a "mode"

	The mode can be passive or active, depending on:
		1. The passive one will have a data pool. Every time the upstream write a data to it, it will store the data internally. And it will not actively push the data to downstream. The downstream must load the data actively. In fact, it is like a prolonged Buffer. Maybe we should emerge this kind of wire with 'Buffer'?
		2. The active one is very similar to the a wire we commonly know. It does not store any data, it is a data deliver. Every time it is called with a piece of data, it will call is output(pool) by the argument called with it.

2. Bus
	The most significant difference between a bus and a active wire is that bus can has a pool of input, and some other facilities to help prevent multiple writing at the same time. In fact, it is like a directed broadcast system. Rememeber its n-in n-out characteristics.

3. Driver
	The driver does not transmit data, but transmit "control" by storing the method to call in a pool.

These abstractions will be very convenient in writing a simulator, but they are not constructed in a level similar to the real microarchitecture. Another flaw is the difference of interfaces. The wires should only be something deliver the data. Without special construction, like a buffer at the end of the wire, it should not have a storage ability. But this is a paradox .... Shit, this piece of software is far from perfection.

Let's talk about abstraction. The connect between wires could be implemented as make another object (or its member function or whatever.) as its own member. The signaling process is simulated by calling machanism. The data transferred is modeled as the argument passed then calling. And since it is a very natural "caller-callee" model, so we actually give the wire a one-direction driving ability.

And device has specific named, generic "port" member function which can deal with the data communication between it and wires. The input can be 'driven' by wires outside. If it is a simple combinational circuit, its port will pass the input as argument to the inner implementation of its logic funciton. When the result is returned, it si returned to the output port, which will distribute (or drive) the proper receiver.

In fact, if we constrct like that, there will be a calling chain till the end of the chain(when will it end?). It happens instantly after the clock has triggered the cycle.

By adding buffer[a minimum storage unit, which will sync every cycle] between the wire and combinational device, the result can be processed later (in the next cycle). So if you put n buffer, the information will go n time, the calling will be blocked.

OK, for the driver line ... I suppose it is redundant. Because it can be implemented by a common wire and another input port defination. The problem is semantic, since controling singal will look exactly the same way.

But due to our effort to generalize the model, so maybe it would be a good idea to de-abstract the concept of driver.


Ok, the abstraction is clear now. We have successfully build the general concept of "wire" and "buffer" and "device". The input model (being connected, callee), output(to connect, caller). The cycle model. The buffer model. The device port and inner implementation mode.

OK.

In fact, maybe you should write another library separately, maybe called eSim, which can be used to construct any kind of digital system.

# Dev Node 5
ReBuild:

1. A more generic Wire class
2. A more generic Buffer class
3. Build Bus upon Wire --> wrap a input pool and some control ability
4. Standardize the input and output port of devices
5. Build Driver into the device


# Dev Note 6
The problem is that I don't know what is the relationship between the FSM I built and the other modules. The FSM should only be a controller, and it is a director, which plays its role by the actionMux we developes.

The running of the machine, the so-called "step" will just be the FSM. other stuff will not control, but to sending signals back and forth. So this is a problem of how to develop this device in a more generic way.

The code is a messy now, combining both direct calling code and some premitive code. The problem is still how to design the interface.

Maybe I should rewrite this simulator.

# Dev Note 7
I have rewritten the whole simulator.

The mistake in the previous versions is the abstraction level. You should not simulator anything below the ISA level. So the "bus" and "wires" are stupid decisions.

Current version, v0.31, would be much better, with proper abstraction level and a powerful data class `Number`