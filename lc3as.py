# Assembler for LC-3 ISA
import sys
import assembler

asm = assembler.assembler(sys.argv[1])
asm.generate()