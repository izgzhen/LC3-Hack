;; test case 9 -- interrupt :
			.ORIG 		x2000
			ST 			R0, Save0
			AND 		R0, R0, #0
			LD 			R0, Save0
			RTI
Save0		.BLKW		#1
			.END