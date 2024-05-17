import struct
import sys

MEM = None
REG = None
IP  = 0

INSTR_SIZE = 12
EXPONENT   = 0x10001

TEST_EQUAL          = 0x789ABCDE
SET_IP              = 0x6789ABCD
SET_IP_IF_NOT_EQUAL = 0xDEF01234
SET_IP_IF_EQUAL     = 0x56789ABC
ADD                 = 0x456789AB
XOR                 = 0x3456789A
SET_REG_VAL         = 0x23456789
SET_REG_REG         = 0x12345678
SUB                 = 0xEF012345
SET_STATUS          = 0xBCDEF012
EXIT                = 0xABCDEF01
SHIFT_LEFT          = 0x89ABCDEF
SHIFT_RIGHT         = 0x9ABCDEF0
EXP_MOD             = 0xCDEF0123

def load(filename):
    global MEM
    f = open(filename, "rb")
    MEM = f.read()
    f.close()


def decode(addr):
    return struct.unpack("<LLL", MEM[addr:addr+INSTR_SIZE])


def run():
    global IP
    IP = 0
    while IP <= len(MEM)-INSTR_SIZE:
        instr, arg1, arg2 = decode(IP)
        if instr == TEST_EQUAL:
            print("%04x : test     reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2))
        if instr == SET_IP:
            print("%04x : set      ip, %d" % (IP // INSTR_SIZE, arg1))     
        if instr == SET_IP_IF_EQUAL:
            print("%04x : setifeq  ip, %d" % (IP // INSTR_SIZE, arg1))
        if instr == SET_IP_IF_NOT_EQUAL:
            print("%04x : setifneq ip, %d" % (IP // INSTR_SIZE, arg1))
        if instr == ADD:
            print("%04x : add      reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2))                 
        if instr == XOR:
            print("%04x : xor      reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2))                                
        if instr == SET_REG_VAL:
            print("%04x : mov      reg[%d], %d" % (IP // INSTR_SIZE, arg1, arg2))         
        if instr == SET_REG_REG:
            print("%04x : mov      reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2)) 
        if instr == SUB:
            print("%04x : sub      reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2))          
        if instr == SET_STATUS:
            print("%04x : set      status, reg[%d]" % (IP // INSTR_SIZE, arg1))   
        if instr == EXIT:
            print("%04x : exit     status" % (IP // INSTR_SIZE))         
        if instr == SHIFT_LEFT:
            print("%04x : shl      reg[%d], %d" % (IP // INSTR_SIZE, arg1, arg2))   
        if instr == SHIFT_RIGHT:
            print("%04x : shr      reg[%d], %d" % (IP // INSTR_SIZE, arg1, arg2))   
        if instr == EXP_MOD:
            print("%04x : expmod   reg[%d], reg[%d]" % (IP // INSTR_SIZE, arg1, arg2))
  
        IP += INSTR_SIZE

        
def main():
    load("vmcode")
    run()
    
if __name__ == "__main__":
    main()
    