'''
Created on Sep 21, 2015

@author: mft
'''


print "Starting AnoPyGB..."
print "Loading ROM ",

filename = "tetris.gb"
fh = open(filename, 'rb')
#romba = bytearray(fh.read())
romba = fh.read()

NAME_OFFSET_START = 0x134
NAME_OFFSET_END = 0x143

# print name
print romba[NAME_OFFSET_START:NAME_OFFSET_END]


