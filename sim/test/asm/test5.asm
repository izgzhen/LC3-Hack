; test case 5 : passed
		.ORIG 		x3000
		ADD 		R1, R1, #10
		LEA 		R2, SUB
		JMP 		R2
A		.BLKW		#1
SUB		ST 			R1, A
		.END