#!/usr/bin/env python
import os, sys, getopt
from Crypto.Hash import SHA, SHA256, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto import Random

private_key = 'sign.pem'
public_key = 'sign.pub'
BLOCK_SIZE = 16 * 32

def sign(hash, filename, signature_file):
    h, key = None, None
    
    # Check private key has existed yet
    if not os.path.isfile(private_key):
        #generate rsa key
        key = RSA.generate(1024, Random.new().read)
        with open(private_key, 'wb') as prvKeyFile:
            prvKeyFile.write(key.exportKey())
        with open(public_key, 'wb') as pubKeyFile:
            pubKeyFile.write(key.publickey().exportKey())
    else:
        key = RSA.importKey(open(private_key, 'rb').read())
   
    if hash == MD5:
        h = MD5.new()
    elif hash == SHA256:
        h = SHA256.new()
    elif hash == SHA:
        h = SHA.new()
    else:
        # None support
        return None

    f_in = open(filename)
    while True:
        block = f_in.read(BLOCK_SIZE)
        if len(block) == 0:
            break
        h.update(block)

    signer = PKCS1_PSS.new(key)
    signature = signer.sign(h)
    
    with open(signature_file, 'wb') as f:
        f.write(signature)


def usage():
    print '''./sign.py -h <hash_mode> <file_need_signing> <signature_file>
Example: ./sign.py -h MD5 HenMotMai.text HenMotMai.signature'''

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

    sign(mode, args[0], args[1])
    print '{} file signed, signature export to {}'.format(args[0], args[1])