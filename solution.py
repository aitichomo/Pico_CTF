import os
import mmap

def memory_map(filename, access=mmap.ACCESS_READ):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDONLY)
    return mmap.mmap(fd, size, access=access)

class Mystery(object):
    PNG_CRC_LEN = 4
    def __init__(self, file_name):
        self.map = memory_map(file_name)
        self.buffer = self.map[self.map.find(b"IEND") + len(b"IEND") + self.PNG_CRC_LEN:]
        self.offset = 0

    def read_byte(self):
        b = self.buffer[self.offset]
        self.offset += 1
        return b

    def __del__(self):
        self.map.close()

FLAG_LEN = 26

flag = [0] * FLAG_LEN
m1_stream = Mystery("mystery.png")
m2_stream = Mystery("mystery2.png")
m3_stream = Mystery("mystery3.png")

flag[1] = m3_stream.read_byte()
flag[0] = m2_stream.read_byte() - 0x15
flag[2] = m3_stream.read_byte()
flag[5] = m3_stream.read_byte()
flag[4] = m1_stream.read_byte()
for i in range(6, 10):
    flag[i] = m1_stream.read_byte()
flag[3] = m2_stream.read_byte() - (10 - 6)
for i in range(10, 15):
    flag[i] = m3_stream.read_byte()
for i in range(15, 26):
    flag[i] = m1_stream.read_byte()

print ("".join(chr(x) for x in flag))
