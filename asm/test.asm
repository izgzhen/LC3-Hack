		.ORIG		x3000
		AND			R1, R1, #10
		LD			R1, NEW
		LD 			R1, NEW
		LDI			R1, NEW
		PUTS
NEW 	.STRINGZ 	"hellow, world"
		.END