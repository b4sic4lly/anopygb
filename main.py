'''
Created on Sep 21, 2015

@author: mft
'''
from debug import *
from bitarray import bitarray

print "Starting AnoPyGB..."

'''
intenablereg = bytearray(1)
ram = bytearray(8*1024)
ioports = bytearray(76)
spritemem = bytearray(160)
echoram = bytearray(8*1024)
internalram = bytearray(8*1024)
switchram = bytearray(8*1024)
videoram = bytearray(8*1024)
rom = bytearray(32*1024)
'''





class register():
    def __init__(self, value, size):
        # size in bit
        self.value = value
        self.size = size
        
    def getlow(self):
        return self.value&0x00ff
        
    def gethigh(self):
        return (self.value&0xff00) >> 8
    
    def setlow(self, value):
        if value < 0x0 or value > 2**(self.size/2):
            print "[ERROR] Cannot write value %d to register. Value too big" % value
            return
    
        self.value = (self.value & 0xFF00) | value 
    
    def sethigh(self, value):
        if value < 0x0 or value > 2**(self.size/2):
            print "[ERROR] Cannot write value %d to register. Value too big" % value
            return
    
        self.value = (self.value & 0x00FF) | (value<<8) 
    
    def get(self):
        return self.value
    
    def set(self, value):
        if value < 0x0 or value > 2**self.size:
            print "[ERROR] Cannot write value %d. Value too big" % value
        self.value = value


class instr():
    def __init__(self, text, oplen, function):
        self.text = text
        self.oplen = oplen
        self.function = function



class emulator():
    
    NAME_OFFSET_START = 0x134
    NAME_OFFSET_END = 0x143
    CARTRIDGETYPE_OFFSET = 0x147
    CART_TYPE_ROMONLY = 0
    
    def __init__(self, filename):
        self.mem = bytearray(65536)
        
        self.running = False
        
        # copy cartridge to memory
        self.mem[0x0:0x8000] = self.loadrom(filename)
        
        self.instrdict = {}
        self.initinstrdict()
        
        self.reset()    
        self.start()
        
    def reset(self):
        # registers
        self.af = register(0x01b0, 16)
        self.bc = register(0x0013, 16)
        self.de = register(0x00d8, 16)
        self.hl = register(0x014d, 16)
        self.sp = register(0xfffe, 16)
        self.pc = register(0x100, 16)
        
        self.zero = False
        self.substract = False
        self.halfcarry = False
        self.carry = False
        
        #self.flag = register(0, 16)
        
        # special memory locations on reset
        self.writebyte(0xFF05, 0)
        self.writebyte(0xFF06, 0)
        self.writebyte(0xFF07, 0)
        self.writebyte(0xFF10, 0x80)
        self.writebyte(0xFF11, 0xBF)
        self.writebyte(0xFF12, 0xF3)
        self.writebyte(0xFF14, 0xBF)
        self.writebyte(0xFF16, 0x3F)
        self.writebyte(0xFF17, 0x00)
        self.writebyte(0xFF19, 0xBF)
        self.writebyte(0xFF1A, 0x7A)
        self.writebyte(0xFF1B, 0xFF)
        self.writebyte(0xFF1C, 0x9F)
        self.writebyte(0xFF1E, 0xBF)
        self.writebyte(0xFF20, 0xFF)
        self.writebyte(0xFF21, 0x00)
        self.writebyte(0xFF22, 0x00)
        self.writebyte(0xFF23, 0xBF)
        self.writebyte(0xFF24, 0x77)
        self.writebyte(0xFF25, 0xF3)
        self.writebyte(0xFF26, 0xF1)
        self.writebyte(0xFF40, 0x91)
        self.writebyte(0xFF42, 0x00)
        self.writebyte(0xFF43, 0x00)
        self.writebyte(0xFF45, 0x00)
        self.writebyte(0xFF47, 0xFC)
        self.writebyte(0xFF48, 0xFF)
        self.writebyte(0xFF49, 0xFF)
        self.writebyte(0xFF4A, 0x00)
        self.writebyte(0xFF4B, 0x00)
        self.writebyte(0xFFFF, 0x00)
    
    
    def readbyte(self, pos):
        if pos < 0x0 or pos > 0xffff:
            print "[ERROR] Cannot access memory location at " + hex(pos)
            return 0
        
        return self.mem[pos]
    
    def read2bytes(self, pos):
        if pos < 0x0 or pos > 0xffff:
            print "[ERROR] Cannot access memory location at " + hex(pos)
            return 0
        
        op1 = self.mem[pos+1]
        op2 = self.mem[pos]
        
        
        return (op1<<8) | op2

    def writebyte(self, pos, value):
        if pos < 0x0 or pos > 0xffff:
            print "[ERROR] Cannot access memory location at " + hex(pos)
            return
        
        if value < 0x0 or value > 0xff:
            print "[ERROR] Cannot write value %d at %s. Value too big" % (value, hex(pos))
            return 
        
        self.mem[pos] = value
    
        
    def loadrom(self, filename):
        print "Loading ROM ",
        
        fh = open(filename, 'rb')
        romba = bytearray(fh.read())
        
        # print name
        print romba[emulator.NAME_OFFSET_START:emulator.NAME_OFFSET_END]
        
        # print cartridge type
        if romba[emulator.CARTRIDGETYPE_OFFSET] == emulator.CART_TYPE_ROMONLY:
            # it's rom only so perfect for us
            print "ROM only cartridge"
        else:
            print "[ERROR] Cartridge Type not ROM only. Cannot emulate"
            return bytearray(1)
        
        return romba



    def start(self):
        self.running = True
        while self.running == True:
            self.cpunext()
            
        print "Emulation finished"

    def cpunext(self):
        instruction = self.readbyte(self.pc.get())
        print "=============================\ncurrent instruction " + hex(instruction)
        
        # Get instruction length
        try:
            instrlength = self.instrdict[instruction].oplen
        except:
            print "Undefined instruction: " + hex(instruction)
            self.running = False
            return
        
        # Operand retrival, can be 0-2 bytes long, depending on operand
        operand = 0
        
        if instrlength == 1:
            operand = self.readbyte(self.pc.get() + 1 )
        elif instrlength == 2:
            operand = self.read2bytes(self.pc.get() + 1) 
        
        print "instruction: " + self.instrdict[instruction].text
        print "operand: " + hex(operand)
        
        # inc pc
        self.pc.set(self.pc.get()+instrlength+1)
        
        # execute instruction
        self.instrdict[instruction].function(self, operand)
                
        print "-------------"
        print "CURRENT REGISTERS"
        print "AF: 0x" + format(self.af.get(), '04x') + "  BC: 0x" + format(self.bc.get(), '04x')
        print "DE: 0x" + format(self.de.get(), '04x') + "  HL: 0x" + format(self.hl.get(), '04x')
        print "SP: 0x" + format(self.sp.get(), '04x') + "  PC: 0x" + format(self.pc.get(), '04x')
        print "-------------"
        
    def initinstrdict(self):
        self.instrdict[0x0]  = instr("nop",0,instrimpl.nop)
        self.instrdict[0xc3] = instr("jp nn", 2,instrimpl.jpnn)
        self.instrdict[0xaf] = instr("xor a", 0,instrimpl.xora)
        self.instrdict[0x21] = instr("ld hl,nn", 2,instrimpl.ldhlnn) 
                
        # ld nn,n
        self.instrdict[0x06] = instr("ld B,n", 1,instrimpl.ldbn)
        self.instrdict[0x0e] = instr("ld C,n", 1,instrimpl.ldcn)
        self.instrdict[0x16] = instr("ld D,n", 1,instrimpl.lddn)
        self.instrdict[0x1e] = instr("ld E,n", 1,instrimpl.lden)
        self.instrdict[0x26] = instr("ld H,n", 1,instrimpl.ldhn)
        self.instrdict[0x2e] = instr("ld L,n", 1,instrimpl.ldln)
        
        # ld (hld),a
        self.instrdict[0x32] = instr("ld (hld),a", 0,instrimpl.ldhlda)
        
        # dec n
        self.instrdict[0x3d] = instr("dec a", 0,instrimpl.deca)
        self.instrdict[0x05] = instr("dec b", 0,instrimpl.decb)
        self.instrdict[0x0d] = instr("dec c", 0,instrimpl.decc)
        self.instrdict[0x15] = instr("dec d", 0,instrimpl.decd)
        self.instrdict[0x1d] = instr("dec e", 0,instrimpl.dece)
        self.instrdict[0x25] = instr("dec h", 0,instrimpl.dech)
        self.instrdict[0x2d] = instr("dec l", 0,instrimpl.decl)
        self.instrdict[0x35] = instr("dec (hl)", 0,instrimpl.dechl)
        
        # jr cc,n
        #self.instrdict[0x20] = instr("jr nz,n", 0,instrimpl.jrnzn)
        #self.instrdict[0x28] = instr("jr z,n",  0,instrimpl.jrzn)
        #self.instrdict[0x30] = instr("jr nc,n", 0,instrimpl.jrncn)
        #self.instrdict[0x38] = instr("jr c,n",  0,instrimpl.jrcn)
        
        
        
class instrimpl():
    @staticmethod
    def nop(emu, op):
        pass
    
    @staticmethod
    def jpnn(emu, op):
        emu.pc.set(op)
    
    @staticmethod
    def xora(emu, op):
        emu.af.sethigh(emu.af.gethigh() ^ emu.af.gethigh())
        
        if emu.af.gethigh() == 0:
            emu.zero = True
        else:
            emu.zero = False
        emu.carry = False
        emu.halfcarry = False
        emu.substract = False
    
    @staticmethod
    def ldhlnn(emu, op):
        emu.hl.set(op)
    
    @staticmethod
    def ldbn(emu, op):
        emu.bc.sethigh(op)
    
    @staticmethod
    def ldcn(emu, op):
        emu.bc.setlow(op)
        
    @staticmethod
    def lddn(emu, op):
        emu.de.sethigh(op)
        
    @staticmethod
    def lden(emu, op):
        emu.de.setlow(op)
        
    @staticmethod
    def ldhn(emu, op):
        emu.hl.sethigh(op)
        
    @staticmethod
    def ldln(emu, op):
        emu.hl.setlow(op)
        
    @staticmethod
    def ldhlda(emu, op):
        emu.writebyte(emu.hl.get(), emu.af.gethigh())
        emu.hl.set(emu.hl.get()-1)
        
        
    @staticmethod 
    def dec(emu, value):
        result = (value - 1) % 256
        if result == 0:
            emu.zero = True
        else:
            emu.zero = False
        
        emu.substract = True
        if (value & 0x0f) == 0x0f:
            emu.halfcarry = True
        else:
            emu.halfcarry = False
            
        return result
    
    @staticmethod
    def deca(emu, op):
        emu.af.sethigh(instrimpl.dec(emu, emu.af.gethigh()))
        
    
    @staticmethod
    def decb(emu, op):
        emu.bc.sethigh(instrimpl.dec(emu, emu.bc.gethigh()))
        
    @staticmethod
    def decc(emu, op):
        emu.bc.setlow(instrimpl.dec(emu, emu.bc.getlow()))
        
    @staticmethod
    def decd(emu, op):
        emu.de.sethigh(instrimpl.dec(emu, emu.de.gethigh()))
        
    @staticmethod
    def dece(emu, op):
        emu.de.setlow(instrimpl.dec(emu, emu.de.getlow()))
        
    @staticmethod
    def dech(emu, op):
        emu.hl.sethigh(instrimpl.dec(emu, emu.hl.gethigh()))
        
    @staticmethod
    def decl(emu, op):
        emu.hl.setlow(instrimpl.dec(emu, emu.hl.getlow())) 
        
    @staticmethod
    def dechl(emu, op):
        # are you sure?
        emu.writebyte(instrimpl.dec(emu, emu.readbyte(emu.hl.get())))
        
        
        
        
        
        
        
        
        
        
        
        

emu = emulator("tetris.gb")


