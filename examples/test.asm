		.ORIG	x3000
		AND		R0, R0, #0
		ADD		R0, R0, #15		; i=15
		LD 		R5, STED
ILP		AND		R2, R2, #0		; max = 0
		AND 	R3, R3, #0		; maxIndex = 0
		AND		R1, R1, #0
		ADD		R1, R1, #15 	; j = 15
		LD		R4, USTED
		ADD 	R4, R4, #15
JLP		NOT		R6, R2
		ADD 	R6, R6, #1 		; R6 = -max
		LDR 	R7, R4, #0 		; R7 = USTED[j]
		ADD		R4, R4, #-1		; R4 will keep up with j
		ADD 	R6, R6, R7 		; R6 = USTED[j] - max
		BRnz	END				; If R6 > 0, update max record

		AND		R3, R3, #0
		ADD 	R3, R1, #0		; maxIndex = j
		AND 	R2, R2, #0		;
		ADD 	R2, R7, #0 		; max = USTED[j], faster than LDR
END		ADD		R1, R1, #-1 	; j--
		BRzp	JLP				; if j >= 0 keep looooop

		STR 	R2, R5, #0 		; STED[i] = max
		ADD		R5, R5, #1  	; R5 will keep up with i
		AND 	R6, R6, #0 		; we need a zero register
		LD 		R7, USTED
		ADD		R7, R7, R3
		STR 	R6, R7, #0 		; USTED[maxIndex] = 0
		ADD 	R0, R0, #-1 	; i--
		BRzp	ILP				; if i >= 0 keep looooop

		AND 	R1, R1, #0 		; ANum = 0
		AND 	R2, R2, #0 		; BNum = 0
		AND 	R0, R0, #0
		ADD		R0, R0, #15 	; R0 = 15
		LD		R5, STED
		ADD 	R5, R5, #15 	; R5 points to final element
LOOP	ADD		R3, R0, #-3 
		BRp 	NEXTIF 			; if i > 3, jump out
		LDR 	R3, R5, #0 		; R3 = STED[i]
		LD 		R6, ALIMIT
		ADD 	R6, R6, R3 		 
		BRn 	NEXTIF			; if STED[i] < 85, jump out
		ADD 	R1, R1, #1 		; if never jump out, the score is 'A'
		BRnzp	LOOPCK
NEXTIF	ADD		R3, R0, #-7 	; if i > 7, jump out
		BRp 	LOOPCK
		LDR 	R3, R5, #0 		; R3 = STED[i]
		LD 		R6, BLIMIT
		ADD 	R6, R6, R3
		BRn 	LOOPCK			; if STED[i] < 75, jump out
		ADD		R2, R2, #1 		; if never jump out, the score is 'B'
LOOPCK	ADD		R5, R5, #-1 	; pointer--
		ADD		R0, R0, #-1 	; i--
		BRzp 	LOOP
		STI		R1, ANUM 		; Store ANum
		STI 	R2, BNUM 		; Store BNum
		HALT
USTED	.FILL	x3200
STED	.FILL	x4000
ANUM	.FILL	x4100
BNUM 	.FILL	x4101
ALIMIT	.FILL	#-85
BLIMIT	.FILL 	#-75
		.END