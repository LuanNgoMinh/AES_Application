#!/usr/bin/env python
import os, sys, getopt
from Crypto.Hash import SHA256, MD5, SHA

BLOCK_SIZE = 16 * 32 #512 bytes

def generateChecksum(hash, filename):
    h = None
    if hash == MD5:
        h = MD5.new()
    elif hash == SHA256:
        h = SHA256.new()
    elif hash == SHA:
        h = SHA.new()
    else:
        # None support
        return None

    with open(filename) as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if len(block) == 0:
                break
            h.update(block)
            
    return h.hexdigest()
    
def verifyChecksum(hash, checksum, filename):
    file_checksum = generateChecksum(hash, filename)
    return file_checksum == checksum

def usage():
    print '''Generate checksum: ./checksum.py -h <hash mode> <filename>
Compare file checksum: ./checksum.py -h <hash mode> -c <checksum> <filename>
Example:
    ./checksum.py -h SHA256 sunflower.jpg
    ./checksum.py -h SHA256 -c 08ad5b6cf4f282bc3044ea437c239ebae398daa17dd366141ba6c883bccabd7b sunflower.jpg
    '''

if __name__ == '__main__':
    mode, checksum, filename = None, '', ''

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'h:c:')
    except getopt.error:
        usage()
        exit(1)
    
    if len(args) == 0:
        usage()
        exit(2)

    dict_opt = dict((o, a) for o, a in optlist)

    try:
        mode = dict_opt['-h']
    except:
        usage()
        exit(2)

    mode = mode.upper()
    if mode == "SHA256":
        mode = SHA256
    elif mode == "SHA":
        mode = SHA
    elif mode == "MD5":
        mode = MD5
    else:
        print 'Mode unsupported'
        exit(2)

    try:
        checksum = dict_opt['-c']
        if verifyChecksum(mode, checksum, args[0]):
            print 'ok'
        else:
            print 'fail'
    except:
        print generateChecksum(mode, args[0])
