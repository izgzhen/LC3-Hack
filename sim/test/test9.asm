;; test case 9 : 
			.ORIG 		x3000
			LD 			R6, SSP			; Load Supervisor Stack Pointer

			LD 			R0, IRS
			LD			R1, KBINT
			STR 		R0, R1, #0 		; Set vector

PRINT		LD 			R0, SET
			STI 		R0, KBSR 	; Set Bit

SET 		.FILL 		x4000
KBINT		.FILL		x0180
KBSR    	.FILL 		xFE00
IRS			.FILL 		x2000
SSP			.FILL 		x3000
			.END