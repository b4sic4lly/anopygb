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
            print "[ERROR] Cannot write value %d. Value too big" % value
    
        self.value = (self.value & 0xFF00) | value 
    
    def sethigh(self, value):
        if value < 0x0 or value > 2**(self.size/2):
            print "[ERROR] Cannot write value %d. Value too big" % value
    
        self.value = (self.value & 0x00FF) | (value<<8) 
    
    def get(self):
        return self.value
    
    def set(self, value):
        if value < 0x0 or value > 2**self.size:
            print "[ERROR] Cannot write value %d. Value too big" % value
        self.value = value


class instr():
    def __init__(self, text, oplen):
        self.text = text
        self.oplen = oplen



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
            print "[ERROR] Cannot write value %d. Value too big" % (value)
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
        
        print "operand: " + hex(operand)
        
        self.pc.set(self.pc.get()+instrlength+1)
        
        #
        # Instruction Switch
        #
        
        if instruction == 0x0:
            #nop
            pass
        elif instruction == 0xc3:
            #jp nn
            self.pc.set(operand)
            print "new pc : " + hex(operand)
        elif instruction == 0xaf:
            # xor n
            self.af.sethigh(self.af.gethigh() ^ self.af.gethigh())
            if self.af.gethigh() == 0:
                self.zero = True
            else:
                self.zero = False
            self.carry = False
            self.halfcarry = False
            self.substract = False
            
        else:
            print "Undefined instruction: " + hex(instruction)
            self.running = False
            return
        
        print "-------------"
        print "CURRENT REGISTERS"
        print "AF: 0x" + format(self.af.get(), '04x') + "  BC: 0x" + format(self.bc.get(), '04x')
        print "DE: 0x" + format(self.de.get(), '04x') + "  HL: 0x" + format(self.hl.get(), '04x')
        print "SP: 0x" + format(self.sp.get(), '04x') + "  PC: 0x" + format(self.pc.get(), '04x')
        print "-------------"
        
    def initinstrdict(self):
        self.instrdict[0x0]  = instr("nop",0)
        self.instrdict[0xc3] = instr("jp nn", 2)
        self.instrdict[0xaf] = instr("xor n", 0) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

emu = emulator("tetris.gb")


