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
mem = bytearray(65536)

def readbyte(pos):
    if pos < 0x0 or pos > 0xffff:
        print "[ERROR] Cannot access memory location at " + hex(pos)
        return 0
    
    return mem[pos]

def writebyte(pos, value):
    if pos < 0x0 or pos > 0xffff:
        print "[ERROR] Cannot access memory location at " + hex(pos)
        return
    
    if value < 0x0 or value > 0xff:
        print "[ERROR] Cannot write value %d. Value too big" % (value)
        return 
    
    mem[pos] = value


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
         

# registers
af = register(0xAAFF, 16)
de = register(0xAAFF, 16)
hl = register(0xAAFF, 16)
sp = register(0xAAFF, 16)
pc = register(0xAAFF, 16)
flag = register(0xAAFF, 16)


print hex(af.get())
af.setlow(0xcc)
af.sethigh(0xbb)
print hex(af.get())



print "Loading ROM ",

filename = "tetris.gb"
fh = open(filename, 'rb')
romba = bytearray(fh.read())
#romba = fh.read()

NAME_OFFSET_START = 0x134
NAME_OFFSET_END = 0x143
CARTRIDGETYPE_OFFSET = 0x147
CART_TYPE_ROMONLY = 0

# print name
print romba[NAME_OFFSET_START:NAME_OFFSET_END]

# print cartridge type
if romba[CARTRIDGETYPE_OFFSET] == CART_TYPE_ROMONLY:
    # it's rom only so perfect for us
    print "ROM only cartridge"
else:
    print "Cartridge Type not ROM only. Cannot emulate"

# copy cartridge in memory
mem[0x0:0x8000] = romba


