'''
Created on Sep 22, 2015

@author: mft
'''

class instrimpl():
    
    @staticmethod
    def cp(emu, value):
        result = emu.af.gethigh() - value
        if result == 0:
            emu.setZero(True)
        else:
            emu.setZero(False)
        
        emu.substract = True
        
        if (value & 0x0f) > (emu.af.gethigh() & 0x0f):
            emu.setHalfcarry(True)
        else:
            emu.setHalfcarry(False)
        
        # carry
        if emu.af.gethigh() < value:
            emu.carry = True
        else:
            emu.setCarry(False)
            
    
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
    def ldba(emu, op):
        emu.bc.sethigh(emu.af.gethigh())
    
    @staticmethod
    def ldca(emu, op):
        emu.bc.setlow(emu.af.gethigh())
        
    @staticmethod
    def ldda(emu, op):
        emu.de.sethigh(emu.af.gethigh())
    
    @staticmethod
    def ldea(emu, op):
        emu.de.setlow(emu.af.gethigh())
        
    @staticmethod
    def ldha(emu, op):
        emu.hl.sethigh(emu.af.gethigh())
        
    @staticmethod
    def ldla(emu, op):
        emu.de.setlow(emu.af.gethigh())
        
    @staticmethod
    def ldbca(emu, op):
        emu.writebyte(emu.bc.get(), emu.af.gethigh())
    
    @staticmethod
    def lddea(emu, op):
        emu.writebyte(emu.de.get(), emu.af.gethigh())
        
    @staticmethod
    def ldhla(emu, op):
        emu.writebyte(emu.hl.get(), emu.af.gethigh())
        
    @staticmethod
    def ldnna(emu, op):
        emu.writebyte(op, emu.af.gethigh())
        
    
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
    def tounsignedint(byte):
        if byte < 0:
            return byte + 256
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
            emu.setZero(True)
        else:
            emu.setZero(False)
        emu.setCarry(False)
        emu.setHalfcarry(False)
        emu.setSubstract(False)
    
    @staticmethod
    def ldhlnn(emu, op):
        emu.hl.set(op)
    
    @staticmethod
    def ldbcnn(emu, op):
        emu.bc.set(op)
        
    @staticmethod
    def lddenn(emu, op):
        emu.de.set(op)
        
    @staticmethod
    def ldspnn(emu, op):
        emu.sp.set(op)
    
    
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
            emu.setZero(True)
        else:
            emu.setZero(False)
        
        emu.substract = True
        if (value & 0x0f) == 0x0f:
            emu.setHalfcarry(True)
        else:
            emu.setHalfcarry(False)
            
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
    def decmhl(emu, op):
        # are you sure?
        emu.writebyte(instrimpl.dec(emu, emu.readbyte(emu.hl.get())))
    
    @staticmethod
    def decbc(emu, op):
        emu.bc.set(instrimpl.dec(emu, emu.bc.get())) 
    
    @staticmethod
    def decde(emu, op):
        emu.de.set(instrimpl.dec(emu, emu.de.get()))
        
    @staticmethod
    def dechl(emu, op):
        emu.hl.set(instrimpl.dec(emu, emu.hl.get()))
        
    @staticmethod
    def decsp(emu, op):
        emu.sp.set(instrimpl.dec(emu, emu.sp.get()))
    
    
    @staticmethod
    def jrnzn(emu, op):
        if emu.getZero() == False:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrzn(emu, op):
        if emu.getZero() == True:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrncn(emu, op):
        if emu.getCarry() == False:
            emu.pc.set(emu.pc.get() + instrimpl.tosignedint(op))
            
    @staticmethod
    def jrcn(emu, op):
        if emu.getCarry() == True:
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
    def ldiahl(emu, op):
        emu.af.sethigh(emu.readbyte(emu.hl.get()))
        emu.hl.set(emu.hl.get()+1)   
        
    @staticmethod
    def ldahl(emu, op):
        emu.af.sethigh(emu.readbyte(emu.hl.get()))
        
    
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
        
    @staticmethod
    def ldff00ca(emu, op):
        emu.writebyte(0xff00+emu.bc.getlow(), emu.af.gethigh())
        
    @staticmethod
    def inca(emu, op):
        emu.af.sethigh(instrimpl.inc(emu, emu.af.gethigh()))
    
    @staticmethod
    def incb(emu, op):
        emu.bc.sethigh(instrimpl.inc(emu, emu.bc.gethigh()))
        
    @staticmethod
    def incc(emu, op):
        emu.bc.setlow(instrimpl.inc(emu, emu.bc.getlow()))
        
    @staticmethod
    def incd(emu, op):
        emu.de.sethigh(instrimpl.inc(emu, emu.de.gethigh()))
        
    @staticmethod
    def ince(emu, op):
        emu.de.setlow(instrimpl.inc(emu, emu.de.getlow()))
        
    @staticmethod
    def inch(emu, op):
        emu.hl.sethigh(instrimpl.inc(emu, emu.hl.gethigh()))
        
    @staticmethod
    def incl(emu, op):
        emu.hl.sethigh(instrimpl.inc(emu, emu.hl.gethigh()))
        
    @staticmethod
    def inchl(emu, op):
        emu.writebyte(emu.hl.get(), instrimpl.inc(emu, emu.readbyte(emu.hl.get())) )
    
    @staticmethod 
    def inc(emu, value):
        result = (value + 1) % 256
        if result == 0:
            emu.setZero(True)
        else:
            emu.setZero(False)
        
        emu.setSubstract(False)
        
        if (value & 0x0f) == 0x0f:
            emu.setHalfcarry(True)
        else:
            emu.setHalfcarry(False)
            
        return result    
        
    @staticmethod
    def call(emu, op):
        emu.push2bytestack(emu.pc.get())
        emu.pc.set(op)
            
    @staticmethod
    def orwitha(emu, value):
        result = emu.af.gethigh() | value
        if result == 0:
            emu.setZero(True)
        else:
            emu.setZero(False)
            
        emu.setSubstract(False)
        emu.setHalfcarry(False)
        emu.setCarry(False)
        
        return result
    
    @staticmethod
    def ora(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.af.gethigh()))
    
    @staticmethod
    def orb(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.bc.gethigh()))
    
    @staticmethod
    def orc(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.bc.getlow()))
    
    @staticmethod
    def ord(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.de.gethigh()))
    
    @staticmethod
    def ore(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.de.getlow()))
    
    @staticmethod
    def orh(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.hl.gethigh()))
    
    @staticmethod
    def orl(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.hl.getlow()))
    
    @staticmethod
    def orhl(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, emu.readbyte(emu.hl.get())))
    
    @staticmethod
    def orn(emu, op):
        emu.af.sethigh(instrimpl.orwitha(emu, op))
    
    @staticmethod
    def ret(emu, op):
        emu.pc.set(emu.pop2bytestack())
        
    @staticmethod
    def pushaf(emu, op):
        emu.push2bytestack(emu.af.get())
    
    @staticmethod
    def pushbc(emu, op):
        emu.push2bytestack(emu.bc.get())
        
    @staticmethod
    def pushde(emu, op):
        emu.push2bytestack(emu.de.get())
        
    @staticmethod
    def pushhl(emu, op):
        emu.push2bytestack(emu.hl.get())
            
    @staticmethod
    def andwitha(emu, value):
        result = emu.af.gethigh() & value
        if result == 0:
            emu.setZero(True)
        else:
            emu.setZero(False)
    
        emu.setSubstract(False)
        emu.setHalfcarry(True)
        emu.setCarry(False)
        
        return result
    
    @staticmethod
    def anda(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.af.gethigh()))
    
    @staticmethod
    def andb(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.bc.gethigh()))
        
    @staticmethod
    def andc(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.bc.getlow()))
        
    @staticmethod
    def andd(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.de.gethigh()))
        
    @staticmethod
    def ande(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.de.getlow()))
        
    @staticmethod
    def andh(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.hl.gethigh()))
        
    @staticmethod
    def andl(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.hl.getlow()))
        
    @staticmethod
    def andhl(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, emu.readbyte(emu.hl.get())))
        
    @staticmethod
    def andn(emu, op):
        emu.af.sethigh(instrimpl.andwitha(emu, op))
            
    @staticmethod
    def retnz(emu, op):
        if emu.getZero() == False:
            emu.pc.set(emu.pop2bytestack())
    
    @staticmethod
    def retz(emu, op):
        if emu.getZero() == True:
            emu.pc.set(emu.pop2bytestack())
    
    @staticmethod
    def retnc(emu, op):
        if emu.getCarry() == False:
            emu.pc.set(emu.pop2bytestack())
    
    @staticmethod
    def retc(emu, op):
        if emu.getCarry() == True:
            emu.pc.set(emu.pop2bytestack())
    
    @staticmethod
    def popaf(emu, op):
        emu.af.set(emu.pop2bytestack())
    
    @staticmethod
    def popbc(emu, op):
        emu.bc.set(emu.pop2bytestack())
        
    @staticmethod
    def popde(emu, op):
        emu.de.set(emu.pop2bytestack())
        
    @staticmethod
    def pophl(emu, op):
        emu.hl.set(emu.pop2bytestack())
    
    @staticmethod
    def reti(emu, op):
        emu.returnfrominterrupt()
        
    @staticmethod
    def cplcomplement(emu, op):
        emu.af.sethigh(instrimpl.tounsignedint(~emu.af.gethigh()))
    
    @staticmethod
    def rrca(emu, op):
        emu.setCarry((emu.af.gethigh() >> 0) & 1)
        emu.setSubstract(False)
        emu.setHalfcarry(False)
        if emu.af.gethigh() >> 1 == 0:
            emu.setZero(True)
        else:
            emu.setZero(False)
        emu.af.sethigh(emu.af.gethigh() >> 1)
    

    
        
        
        
        
        
        
        
        
        
    