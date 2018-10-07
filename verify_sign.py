#!/usr/bin/env python
import os, sys, getopt
from Crypto.Hash import SHA, SHA256, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS

public_key = 'sign.pub'
BLOCK_SIZE = 16 * 32

def verify_signature(hash, filename, signature_file):
    h, key = None, None

    if not os.path.isfile(public_key):
        print 'public_key has not existed yet'
        return None

    key = RSA.importKey(open(public_key).read())
    
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
    
    #load signature
    signature = ''
    with open(signature_file) as sigFile: 
        signature = sigFile.read()

    verifier = PKCS1_PSS.new(key)
    return verifier.verify(h, signature)

def usage():
    print '''./sign.py -h <hash_mode> <receive_file> <signature_file>
./verify_sign.py -h SHA256 HenMotMai.text HenMotMai.signature'''

if __name__ == '__main__':
    mode = None
    try:
        optlist, args = getopt.getopt(sys.argv[1:], '-h:')
    except getopt.error:
        usage()
        exit(1)

    if len(optlist) != 1 or len(args) != 2:
        usage()
        exit(2)

    opt_dict = dict((o, a) for o, a in optlist)
    mode = opt_dict['-h']

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

    if verify_signature(mode, args[0], args[1]):
       print '{} is authenticate'.format(args[0])
    else:
        print '{} is unauthenticate'.format(args[0])