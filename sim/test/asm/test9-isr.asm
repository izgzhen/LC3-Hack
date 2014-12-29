;; test case 9 -- interrupt :
			.ORIG 		x2000
			ST 			R0, Save0
			ST 			R7, Save7
			LD 			R0, ANOTHER
			OUT
			LD 			R0, Save0
			LD			R7, Save7
			RTI
Save0		.BLKW		#1
Save7		.BLKW		#1
ANOTHER		.FILL		x0062	;'b'
			.END