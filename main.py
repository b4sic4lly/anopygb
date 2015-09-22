'''
Created on Sep 21, 2015

@author: mft
'''

from debug import *
from cpu import instrimpl 

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
    def __init__(self, text, oplen, function, ticks):
        self.text = text
        self.oplen = oplen
        self.function = function
        self.ticks = ticks



class emulator():
    
    NAME_OFFSET_START = 0x134
    NAME_OFFSET_END = 0x143
    CARTRIDGETYPE_OFFSET = 0x147
    CART_TYPE_ROMONLY = 0
    
    INT_VBLANK = (1 << 0)
    INT_LCDSTAT = (1 << 1)
    INT_TIMER = (1 << 2)
    INT_SERIAL = (1 << 3)
    INT_JOYPAD = (1 << 4)
    
    GPU_HBLANK = 0
    GPU_VBLANK = 1
    GPU_OAM = 2
    GPU_VRAM = 3
    
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
        
        self.interruptmasterenable = True
        
        
        self.ticks = 0
        self.gputicks = 0
        self.lastticks = 0
        
        self.gpumode = 0
        
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
    
    def pushstack(self, byte):
        if byte < 0x0 or byte > 0xff:
            print "[ERROR] Cannot push byte %d. Value too big" % byte
            return
        
        self.sp.set(self.sp.get() - 2)
        self.writebyte(self.sp.get(), byte)
    
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
                
        #raw_input("[Press key to start emulation]")
        while self.running == True:
            self.cpunext()
            self.gpunext()
            self.intnext()
            
        print "Emulation finished"
    
    
    def intnext(self):
        if self.interruptmasterenable == True and self.getInterruptEnable() != 0 and self.getInterruptFlags() != 0:
            inttype = self.getInterruptEnable() & self.getInterruptFlags()
            print "INTNEXT: inttype: %d" % inttype
            if inttype == self.INT_VBLANK:
                print "INTERRUPT VBLANK START"
                self.setInterruptFlags(self.getInterruptEnable() & ~self.INT_VBLANK)
                # TODO: you have to draw here
                
                self.interruptmasterenable = False;
                self.pushstack(self.pc.get())
                self.pc.set(0x40);
                
                self.ticks += 12;


    def getInterruptEnable(self):
        return self.readbyte(0xffff)
    
    def setInterruptEnable(self, value):
        self.writebyte(0xffff, value)
    
    def getInterruptFlags(self):
        return self.readbyte(0xff0f)

    def setInterruptFlags(self, value):
        self.writebyte(0xff0f, value)
        
    def addGpuLine(self, value):
        self.writebyte(0xff44, self.readbyte(0xff44) + value)
        
    def setGpuLine(self, value):
        self.writebyte(0xff44, value)
        
    def getGpuLine(self):
        return self.readbyte(0xff44)

    def fireinterrupt(self, inttype):
        #print "enable&inttype %d" % (inttype & self.getInterruptEnable())
        if (self.getInterruptEnable() & inttype) != 0:
            self.setInterruptEnable(self.getInterruptEnable() | inttype)

    def gpunext(self):
        self.gputicks += self.ticks - self.lastticks
        self.lastticks = self.ticks

        #print self.gpuline

        #print "CURRENT GPUMODE: %d" % self.gpumode

        if self.gpumode == self.GPU_HBLANK:

            if self.gputicks >= 204:
                # hblank ACTION
                self.addGpuLine(1)
                            
                if self.getGpuLine() == 143:
                    # fire vblank interrupt
                    self.fireinterrupt(self.INT_VBLANK)
                    self.gpumode = self.GPU_VBLANK
                                
                self.gputicks -= 204
                
        elif self.gpumode == self.GPU_VBLANK:
            if self.gputicks >= 456:
                self.addGpuLine(1)
                
                if self.getGpuLine() > 153:
                    self.setGpuLine(0)
                    
                    # TODO: this has to be MODE OAM
                    self.gpumode = self.GPU_HBLANK
                
                self.gputicks -= 456
                
        else:
            print "[ERROR] GPU-Mode No. %d not possible" % self.gpumode 

    def cpunext(self):
        instruction = self.readbyte(self.pc.get())
        
        #if self.pc.get() == 0x02b2:
        #    print "BREAKPOINT "
        #    self.running = False
        #    return
        
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
        
        dumpinstruction(self, instruction, operand)
        
        # inc pc
        self.pc.set(self.pc.get()+instrlength+1)
        
        self.ticks += self.instrdict[instruction].ticks
        
        # execute instruction
        self.instrdict[instruction].function(self, operand)
        
        
        
        '''
        print "=============================\ncurrent instruction " + hex(instruction)
        print "instruction: " + self.instrdict[instruction].text
        print "operand: " + hex(operand)
          
        print "-------------"
        print "CURRENT REGISTERS"
        print "AF: 0x" + format(self.af.get(), '04x') + "  BC: 0x" + format(self.bc.get(), '04x')
        print "DE: 0x" + format(self.de.get(), '04x') + "  HL: 0x" + format(self.hl.get(), '04x')
        print "SP: 0x" + format(self.sp.get(), '04x') + "  PC: 0x" + format(self.pc.get(), '04x')
        print "-------------"
        '''
        
    def initinstrdict(self):
        self.instrdict[0x0]  = instr("nop",0,instrimpl.nop, 4)
        self.instrdict[0xc3] = instr("jp %d", 2,instrimpl.jpnn, 12)
        self.instrdict[0xaf] = instr("xor a", 0,instrimpl.xora, 4)
        self.instrdict[0x21] = instr("ld hl,%d", 2,instrimpl.ldhlnn, 12) 
                
        # ld nn,n
        self.instrdict[0x06] = instr("ld B,%d", 1,instrimpl.ldbn, 8)
        self.instrdict[0x0e] = instr("ld C,%d", 1,instrimpl.ldcn, 8)
        self.instrdict[0x16] = instr("ld D,%d", 1,instrimpl.lddn, 8)
        self.instrdict[0x1e] = instr("ld E,%d", 1,instrimpl.lden, 8)
        self.instrdict[0x26] = instr("ld H,%d", 1,instrimpl.ldhn, 8)
        self.instrdict[0x2e] = instr("ld L,%d", 1,instrimpl.ldln, 8)
        
        # ld (hld),a
        self.instrdict[0x32] = instr("ld (hld),a", 0,instrimpl.ldhlda, 8)
        
        # dec n
        self.instrdict[0x3d] = instr("dec a", 0,instrimpl.deca, 4)
        self.instrdict[0x05] = instr("dec b", 0,instrimpl.decb, 4)
        self.instrdict[0x0d] = instr("dec c", 0,instrimpl.decc, 4)
        self.instrdict[0x15] = instr("dec d", 0,instrimpl.decd, 4)
        self.instrdict[0x1d] = instr("dec e", 0,instrimpl.dece, 4)
        self.instrdict[0x25] = instr("dec h", 0,instrimpl.dech, 4)
        self.instrdict[0x2d] = instr("dec l", 0,instrimpl.decl, 4)
        self.instrdict[0x35] = instr("dec (hl)", 0,instrimpl.dechl, 12)
        
        # jr cc,n
        self.instrdict[0x20] = instr("jr nz,%02x", 1,instrimpl.jrnzn, 8)
        self.instrdict[0x28] = instr("jr z,%02x",  1,instrimpl.jrzn, 8)
        self.instrdict[0x30] = instr("jr nc,%02x", 1,instrimpl.jrncn, 8)
        self.instrdict[0x38] = instr("jr c,%02x",  1,instrimpl.jrcn, 8)
        
        #ld a,n
        self.instrdict[0x7f] = instr("ld A,A", 0,instrimpl.ldaa, 4)
        self.instrdict[0x78] = instr("ld A,b", 0,instrimpl.ldab, 4)
        self.instrdict[0x79] = instr("ld A,c", 0,instrimpl.ldac, 4)
        self.instrdict[0x7a] = instr("ld A,d", 0,instrimpl.ldad, 4)
        self.instrdict[0x7b] = instr("ld A,e", 0,instrimpl.ldae, 4)
        self.instrdict[0x7c] = instr("ld A,h", 0,instrimpl.ldah, 4)
        self.instrdict[0x7d] = instr("ld A,l", 0,instrimpl.ldal, 4)
        self.instrdict[0x0a] = instr("ld A,(bc)", 0,instrimpl.ldabc, 8)
        self.instrdict[0x1a] = instr("ld A,(de)", 0,instrimpl.ldade, 8)
        self.instrdict[0x7e] = instr("ld A,(hl)", 0,instrimpl.ldahl, 8)
        self.instrdict[0xfa] = instr("ld A,(%d)", 2,instrimpl.ldann, 16)
        self.instrdict[0x3e] = instr("ld A,%d", 1,instrimpl.ldan, 8)
        
        # interrupts di, ei
        self.instrdict[0xf3] = instr("di", 0,instrimpl.di, 4)
        self.instrdict[0xfb] = instr("ei", 0,instrimpl.ei, 4)
        
        # ldhna
        self.instrdict[0xe0] = instr("ld ($FF00+%d),a", 1, instrimpl.ldhna, 12)
        self.instrdict[0xf0] = instr("ld a,($FF00+%02x)", 1, instrimpl.ldhan, 12)
        
        # cp n
        self.instrdict[0xbf] = instr("cp a", 0, instrimpl.cpa, 4)
        self.instrdict[0xb8] = instr("cp b", 0, instrimpl.cpb, 4)
        self.instrdict[0xb9] = instr("cp c", 0, instrimpl.cpc, 4)
        self.instrdict[0xba] = instr("cp d", 0, instrimpl.cpd, 4)
        self.instrdict[0xbb] = instr("cp e", 0, instrimpl.cpe, 4)
        self.instrdict[0xbc] = instr("cp h", 0, instrimpl.cph, 4)
        self.instrdict[0xbd] = instr("cp l", 0, instrimpl.cpl, 4)
        self.instrdict[0xbe] = instr("cp (hl)", 0, instrimpl.cphl, 8)
        self.instrdict[0xfe] = instr("cp %02x", 1, instrimpl.cpn, 8)
                
        print "Loaded %d of 244 instructions" % len(self.instrdict)
        

    
    
    
    
    
    
    
    
    
    
    

        
        
emu = emulator("tetris.gb")


