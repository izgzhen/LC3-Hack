tokens = (
	'OP_ADD',
	'OP_AND',
	'OP_BR',
	'OP_JMP',
	'OP_LDR',
	'OP_TRAP',
	'OP_NOT',
	'OP_RET',
	'OP_JSR',
	'OP_JSRR',
	'OP_LD',
	'OP_LDI',
	'OP_LEA',
	'OP_RTI',
	'REG',
	'HEX',
	'DECIMAL',
	'N_HEX',
	'N_DECIMAL',
	'P_OP',
	)

opcode = {
	'ADD' : '0001',
	'AND' : '0101',
	'BR'  : '0000',
	'JMP' : '1100',
	'LDR' : '0110',
	'TRAP': '1111',
	'NOT' 	: '1001',
	'RET' 	: '1100',
	'JSR' 	: '0100',
	'JSRR' 	: '0100',
	'LD' 	: '0010',
	'LDI' 	: '1010',
	'LEA' 	: '1110',
	'RTI' 	: '1000'
}

popcode = {}