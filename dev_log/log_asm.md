# Dev Note 1:

Now my goal in writing the LC-3 Hack would change a bit, since I found through the real code that this machine is very complex to build actually. So when An Hong said: build a assembler yourself, I can't really build a full-feature suite, which needs more than 5000 lines of code.

So, you should lower the goal, from LC-3 Hack to a Novice Hacking inspired by LC-3, since you have little ability implement the LC-3 ISA (Although it is already simple enough).


So, in the assembler, I will use a more rapid developing strategy. Here is a more detailed plan:

The assembler (In python)

1. Reconstruct the previous code in a modular, compact way. -- Before ICS test
2. Provide all supported instructions.  					-- Before the end of this week
3. Do some lexing work, such as Regex supporting, better
   (more robust) line parser, and do some tests 		 	-- Before end of this month

The simulator (In python)
1. Do a primitive kick-start intense hacking (2-3 hours)	-- After ICS test
2. Reconstruct its core logic								-- After GRE
3. Write a more complete featured version, incluing at least:
	* Clock Sync
	* Memory Pool
	* ALU module
	* Control Logic
	* Supporting Dynamic object file loading
	* Supporting: ADD, AND, NOT, LD, ST 					-- Before December


# Dev Note 2:

Some issues in reconstucting:

1. Namespace
2. Structure

The program has been divided into several modules and functions.

Next step is to clean the code. I willl leave this tomorrow.

# Dev Note 3:
I found the parsing seems being filled with redundent code ... you should make it better

# Dev Note 4:
I have written some regex for hex, bin, dec in 'transformer.py', But I still don't know the details of regex. I will write a better one when I get connected tomorrow.

Not good enought, I haven't considered the negative number problem. I will take care of that tomorrow morning. I have to go to sleep now. :)

# Dev Note 5:
Rewrite the whole assembler:

1. Use lexer and regex to parse & build symbol table
2. Use symbol table to facilitate the pass 2nd.
3. Maybe you can reuse the `Number` class in assembler?
