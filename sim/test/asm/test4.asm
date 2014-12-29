;; test case 4 : passed
		.ORIG 	x3000
		AND 	R1, R1, #0
		ADD 	R1, R1, #10
		AND 	R2, R2, #0
LOOP 	ADD 	R2, R2, R1
		ADD 	R1, R1, #-1
		BRp		LOOP
		ST 		R2, RESULT
		; test: x3007 >> x0037
RESULT 	.BLKW 	#1
		.END