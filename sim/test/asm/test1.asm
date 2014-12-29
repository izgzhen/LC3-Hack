; test case one : passed
; output: x3008 >> FFF9

		.ORIG 	x3000
		LD		R1, A
		LD 		R2, B
		ADD 	R3, R1, R2
		ADD 	R3, R3, #3
		NOT 	R4, R3
		AND 	R1, R1, #0
		NOT 	R1, R1
		AND		R5, R4, R1
		ST 		R5, C
A		.FILL	#1
B		.FILL 	#2
C		.BLKW	#1
		.END