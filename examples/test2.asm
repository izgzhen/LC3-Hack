			.ORIG 		x3000
			;; Read the name
			LEA			R0, LOGIN_PRO
			PUTS
			LEA 		R1, NAME
			JSR 		READSTR

			;; Read the password
			LEA			R0, PWD_PRO
			PUTS
			LEA 		R1, PWD
			JSR			READSTR

			LD			R3, USERS	; The address of first user pointer
			BR 			READ_USER

NEXT_USER	ADD 		R3, R3, #1
READ_USER   LDR 		R4, R3, #0	; user list info
			BRz			FAILED_AUTH ; Not found
			LEA 		R1, NAME 	; inputted name

CHECK_NAME  LDR 		R5, R4, #0  ; ch1
			LDR 		R6, R1, #0  ; ch2
			NOT 		R6, R6
			ADD 		R6, R6, #1
			ADD 		R6, R6, R5 	; R6 = R5 - R6
			BRnp 		NEXT_USER 	; Match failed
			ADD 		R5, R5, #0	;
			BRz			READ_PWD ; if ch5 = 0, name passed
			ADD 		R4, R4, #1  ; next char
			ADD 		R1, R1, #1  ; next char
			BR 			CHECK_NAME

READ_PWD	ADD 		R4, R4, #1  ; Start of password
			LEA 		R1, PWD 	; Inputted password

CHECK_PWD	LDR 		R5, R4, #0	; ch1
			BRz			PASSED_AUTH ; if ch5 = 0, password passed
			LDR 		R6, R1, #0	; ch2
			ADD 		R6, R6, x-0C ; Encrypt
			NOT 		R6, R6
			ADD 		R6, R6, #1
			ADD 		R6, R6, R5 	; R6 = R5 - R6
			BRnp		FAILED_AUTH ; R5 != R6
			ADD 		R4, R4, #1  ; next char
			ADD 		R1, R1, #1  ; next char
			BR 			CHECK_PWD

FAILED_AUTH LEA			R0, FAILED_PROMPT
			PUTS
			HALT

PASSED_AUTH LEA 		R0, NAME
			PUTS
			LEA 		R0, PASSED_PROMPT
			PUTS
			HALT

; The READSTR Subroutine
READSTR 	ST 			R7, SAVER7
			ST 			R2, SAVER2
			ST 			R0, SAVER0
			ADD 		R2, R1, #0
LOOP		GETC
			OUT
			STR 		R0, R2, #0
			ADD			R0, R0, #-13 ; Line Feed
			BRz			ENDREAD
			ADD 		R2, R2, #1
			BRp 		LOOP
ENDREAD		AND 		R0, R0, #0
			STR 		R0, R2, #0
			LD 			R7, SAVER7
			LD 			R2, SAVER2
			LD 			R0, SAVER0
			RET
SAVER0		.FILL 		x0
SAVER2		.FILL 		x0
SAVER7		.FILL 		x0

; Auxiliary info
USERS 		.FILL		x4000
LOGIN_PRO	.STRINGZ	"\nLogin ID: "
PWD_PRO 	.STRINGZ 	"\nPassword: "
FAILED_PROMPT 	.STRINGZ 	"Invalid UserID/Password. Your login failed."
PASSED_PROMPT 	.STRINGZ 	", you have successfully logged in."
NAME		.BLKW 		#10
PWD			.BLKW 		#10
			.END