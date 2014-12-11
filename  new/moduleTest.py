import modules

Wire = modules.Wire

''' --- ALU TEST --- '''
# wa = Wire()
# wb = Wire()
# wo = Wire()
# w2 = FakeWire()
# alu = ALU(2, 16, resource.operations)

# wa.connect(alu.operand1)
# wb.connect(alu.operand2)
# wo.connect(alu.opMux)
# alu.connect(w2)

# wa.write('1000100010001000')
# wb.write('0001000100010001')
# wo.write('10') # +
# alu.sync()

''' --- RegFile TEST --- '''
# regMuxin = Wire()
# WEin = Wire()
# LDEin = Wire()
# output = FakeWire()
# regs = RegFile(8, 3, 16)

# WEin.connect(regs.WEin)
# LDEin.connect(regs.LDEin)
# regMuxin.connect(regs.regMuxin)
# regs.connect(output)

# WEin.write('1')
# regMuxin.write('001')
# regs.write('1'*16)
# WEin.write('0')
# regMuxin.write('000')
# LDEin.write('1')
# regMuxin.write('001')
# regs.sync()
# LDEin.write('0')

''' --- Memory  ---'''
# MARin = Wire()
# MDRin = Wire()
# WEin = Wire()
# LDEin = Wire()
# output = modules.FakeWire()
# mem = modules.Memory(16, 16)

# MARin.connect(mem.MAR)
# MDRin.connect(mem.MDR)
# WEin.connect(mem.WE)
# LDEin.connect(mem.LDE)
# mem.connect(output)

# MARin.write('0' * 15 + '1')
# MDRin.write('1' * 16)
# WEin.write('1')
# mem.sync()
# WEin.write('0')

# MDRin.write('0' * 16)
# LDEin.write('1')
# mem.sync()
# LDEin.write('0')