bytes    = (0xC8, 0xF7, 0x1D, 0x14, 0x96, 0x97, 0x41, 0xF9, 0x77, 0xFD)
number   = 0
bitcount = 0
output   = ''
for byte in bytes:
    # add data on to the end
    number = number + (byte << bitcount)
    # increase the counter
    bitcount = bitcount + 1
    # output the first 7 bits
    output = output + '%c' % (number % 128)
    # then throw them away
    number = number >> 7
    # every 7th letter you have an extra one in the buffer
    if bitcount == 7:
        output = output + '%c' % (number)
        bitcount = 0
        number = 0
print output
