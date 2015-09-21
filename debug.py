'''
Created on Sep 21, 2015

@author: mft
'''

def dump(bram, start, end):
    rowcount=0
    rowstr = ""
    counter = 0
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
            rowstr = ""
            rowcount = 0
        
        if counter == 0x134:
            print "WIR SIND DA " + byte
            
    if rowstr != "":
        print rowstr