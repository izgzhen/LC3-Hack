;; test case 3 : passed
		.ORIG	x3000
		AND 	R1, R1, #0
		ADD 	R1, R1, #10
		STI 	R1, A
		; test: x3006 >> x000a
		LEA 	R2, B
		ADD 	R2, R2, #1
		STR 	R1, R2, #1
		; test: x3009 >> x000a
A 		.FILL 	x3007
B 		.BLKW	#1
		.END