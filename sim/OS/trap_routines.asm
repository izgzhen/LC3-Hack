;; LC3-OS	TRAP routines
			.ORIG 		x0200
			AND 		R1, R1, #0	; HALT --> modify MCR's RUN latch
			STI 		R1, OS_MCR
OS_MCR 		.FILL		xFFFE
			RET

TRAP_GETC	LDI			R0, OS_KBSR
			BRzp		TRAP_GETC
			LDI			R0, OS_KBDR
			RET

TRAP_OUT 	ST			R1, Save1
OUT_WAIT 	LDI			R1, OS_DSR		
			BRzp		OUT_WAIT
			STI			R0, OS_DDR		
			LD 			R1, Save1
			RET

Save1		.BLKW 		#1
OS_KBSR		.FILL		xFE00
OS_KBDR		.FILL		xFE02
OS_DSR		.FILL		xFE04
OS_DDR		.FILL		xFE06
			.END