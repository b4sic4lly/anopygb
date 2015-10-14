'''
Created on Sep 21, 2015

@author: mft
'''

def dump(bram, start, end):
    rowcount=0
    rowstr = ""
    counter = 1
    
    print "MEM:" + format(counter-1, '04x') + " ",
    
    for byte in bram[start:end]:
        newbyte = format(byte, '02x') 
        print newbyte + " ",
        if byte >= 32 and byte <=126:
            rowstr+= chr(byte)
        else:
            rowstr +="."
        
        rowcount+=1
        if rowcount >= 16:
            print rowstr
            print "MEM:" + format(counter, '04x') + " ",
            rowstr = ""
            rowcount = 0
        
        counter+=1
        
        
            
    if rowstr != "":
        print rowstr
        
        
def dumpinstruction(emu, instruction, operand):
    # print current instruction
    
    
    instrlength = emu.instrdict[instruction].oplen
    
    debugstring = "PC %04x " % (emu.pc.get()-(instrlength+1))
    
    if instrlength>0:
        debugstring += emu.instrdict[instruction].text % operand
    else:
        debugstring += emu.instrdict[instruction].text
    
    #print len(debugstring)
    
    
    if len(debugstring) <= 15:
        debugstring += "\t"
    
    if len(debugstring) <= 23:
        debugstring += "\t"
    
    debugstring += "AF: 0x" + format(emu.af.get(), '04x') + "\tBC: 0x" + format(emu.bc.get(), '04x') + " "
    debugstring += "DE: 0x" + format(emu.de.get(), '04x') + "\tHL: 0x" + format(emu.hl.get(), '04x') + " "
    debugstring += "SP: 0x" + format(emu.sp.get(), '04x') + "\tPC: 0x" + format(emu.pc.get(), '04x') + " "
         
    print debugstring