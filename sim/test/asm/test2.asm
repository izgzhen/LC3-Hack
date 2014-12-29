;; test case 2 : passed
		.ORIG 	x3000
		LDI 	R1, A
		; test: R1
		LEA 	R1, A
		ADD 	R1, R1, 1
		LDR 	R2, R1, #0
		; test: R2
A		.FILL	x3005	
B		.FILL   #10
		.END
