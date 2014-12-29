;; test case 6
		.ORIG 		x3000
		AND 		R1, R1, #0
		JSR 		ADDONE
		LEA 		R2, ADDTWO
		JSRR 		R2
		; test R1 >> x0001
		ADD 		R1, R1, #0
		; test R1 >> x0003
A 		.BLKW		#1
ADDONE	ADD 		R1, R1, #1
		RET
ADDTWO 	ADD 		R1, R1, #2
		RET
		.END