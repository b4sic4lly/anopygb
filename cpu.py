'''
Created on Sep 22, 2015

@author: mft
'''

class instrimpl():
    
    @staticmethod
    def cp(emu, value):
        result = emu.af.gethigh() - value
        if result == 0:
            emu.zero = True
        else:
            emu.zero = False
        
        emu.substract = True
        
        if (value & 0x0f) > (emu.af.gethigh() & 0x0f):
            emu.halfcarry = True
        else:
            emu.halfcarry = False
        
        # carry
        if emu.af.gethigh() < value:
            emu.carry = True
        else:
            emu.carry = False
            
    
    @staticmethod
    def cpa(emu, op):
        instrimpl.cp(emu, emu.af.gethigh())
    
    @staticmethod
    def cpb(emu, op):
        instrimpl.cp(emu, emu.bc.gethigh())
    
    @staticmethod
    def cpc(emu, op):
        instrimpl.cp(emu, emu.bc.getlow())
    
    @staticmethod
    def cpd(emu, op):
        instrimpl.cp(emu, emu.de.gethigh())
    
    @staticmethod
    def cpe(emu, op):
        instrimpl.cp(emu, emu.de.getlow())
    
    @staticmethod
    def cph(emu, op):
        instrimpl.cp(emu, emu.hl.gethigh())
    
    @staticmethod
    def cpl(emu, op):
        instrimpl.cp(emu, emu.hl.getlow())
    
    @staticmethod
    def cphl(emu, op):
        instrimpl.cp(emu, emu.readbyte(emu.hl.get()))
        
    @staticmethod
    def cpn(emu, op):
        instrimpl.cp(emu, op)
    
    @staticmethod
    def ldhlb(emu, op):
        emu.writebyte(emu.hl.get(), emu.bc.gethigh())
    
    @staticmethod
    def ldhlc(emu, op):
        emu.writebyte(emu.hl.get(), emu.bc.getlow())
    
    @staticmethod
    def ldhld(emu, op):
        emu.writebyte(emu.hl.get(), emu.de.gethigh())
    
    @staticmethod
    def ldhle(emu, op):
        emu.writebyte(emu.hl.get(), emu.de.getlow())
    
    @staticmethod
    def ldhlh(emu, op):
        emu.writebyte(emu.hl.get(), emu.hl.gethigh())
    
    @staticmethod
    def ldhll(emu, op):
        emu.writebyte(emu.hl.get(), emu.hl.getlow())
    
    @staticmethod
    def ldhln(emu, op):
        emu.writebyte(emu.hl.get(), op)
        
    
    
    
    
    @staticmethod
    def ldhan(emu, op):
        emu.af.sethigh(emu.readbyte(0xff00+op))
    
    @staticmethod
    def ldhna(emu, op):
        emu.writebyte(0xff00+op, emu.af.gethigh())
    
    
    @staticmethod
    def tosignedint(byte):
        if byte > 127:
            return (256-byte) * (-1)
        else:
            return byte
    
    @staticmethod
    def stub(emu, op):
        print "This instruction is not implemented"
        emu.running = False
    
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
        
    @staticmethod
    def jrnzn(emu, op):
        if emu.zero == False:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrzn(emu, op):
        if emu.zero == True:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrncn(emu, op):
        if emu.carry == False:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrcn(emu, op):
        if emu.carry == True:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))      
    
    @staticmethod
    def ldaa(emu, op):
        emu.af.sethigh(emu.af.gethigh())    
    
    @staticmethod
    def ldab(emu, op):
        emu.af.sethigh(emu.bc.gethigh())    
    
    @staticmethod
    def ldac(emu, op):
        emu.af.sethigh(emu.bc.getlow())    
    
    @staticmethod
    def ldad(emu, op):
        emu.af.sethigh(emu.de.gethigh())    
    
    @staticmethod
    def ldae(emu, op):
        emu.af.sethigh(emu.de.getlow())    
    
    @staticmethod
    def ldah(emu, op):
        emu.af.sethigh(emu.hl.gethigh())    
    
    @staticmethod
    def ldal(emu, op):
        emu.af.sethigh(emu.hl.getlow())    
    
    @staticmethod
    def ldabc(emu, op):
        emu.af.sethigh(emu.readbyte(emu.bc.get()))    
    
    @staticmethod
    def ldade(emu, op):
        emu.af.sethigh(emu.readbyte(emu.de.get()))    
    
    @staticmethod
    def ldahl(emu, op):
        emu.af.sethigh(emu.hl.get())    
    
    @staticmethod
    def ldann(emu, op):
        emu.af.sethigh(emu.readbyte(op))    
    
    @staticmethod
    def ldan(emu, op):
        emu.af.sethigh(op)    
    
    @staticmethod
    def di(emu, op):
        # TODO: this is not correct they are disabled after the next instruction 
        emu.interruptmasterenable = False
    
    @staticmethod
    def ei(emu, op):
        # TODO: this is not correct they are enabled after the next instruction
        emu.interruptmasterenable = True
    