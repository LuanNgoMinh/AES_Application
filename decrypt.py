#!/usr/bin/env python
# -*- coding: utf-8 -*-
# decrypt.py –m <mode> <tên file input> <tên file output>
import os, getopt, sys, struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Counter

#Key for aes encryption
secret_key = 'conmeoconxinhxan'

def decrypt(mode, encrypt_filename, output):
    # Generate key from secret key
    key = SHA256.new(secret_key).digest()

    with open(encrypt_filename, "rb") as encrypt_file:
        with open(output, "wb") as decrypt_file:
            # Read 16 bytes because use iv 16 bytes
            iv = encrypt_file.read(16)
            aes = None

            if mode == AES.MODE_CTR:
                ctr = Counter.new(128, initial_value=long(iv.encode("hex"), 16))
                aes = AES.new(key, mode, counter=ctr)
            else:
                aes = AES.new(key, mode, iv)

            next_block = ''
            while True:
                block, next_block = next_block, aes.decrypt(encrypt_file.read(AES.block_size))
                if len(next_block) == 0: 
                    padding_length = ord(block[-1])
                    block = block[:-padding_length]
                    decrypt_file.write(block)
                    break
                    
                decrypt_file.write(block)
                
            decrypt_file.close()
            encrypt_file.close()
    pass


def usage():
    print \
    '''Usage:\n\n\tpython encrypt.py or ./encrypt.py -m <mode> <input file name> <output file name>
\n\t-mode: mode to encryption: ECB, CBC, CFB, OFB, CTR, OPENPGP
\nExample: ./decrypt.py -m CFB meomeo.text meomeo.decrypted
    '''


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print usage()
        exit(1)

    mode = None

    #get options list
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:')
    except optlist.error:
        print "Get options error"
        exit(2)

    #check options list
    if len(optlist) != 1:
        print 'Options lists error'
        usage()
        exit(1)

    if len(args) != 2:
        print 'File name error'
        usage()
        exit(1)

    #check input file has existed yet
    if not os.path.isfile(args[0]):
        print '"{}" file has not existed yet'.format(args[0])
        exit(3)

    dict_opt = dict((o, a) for o, a in optlist)
    mode = dict_opt['-m']

    #check mode valid
    mode = mode.upper()
    if mode == 'ECB':
        mode = AES.MODE_ECB
    elif mode == 'CBC':
        mode = AES.MODE_CBC
    elif mode == 'CFB':
        mode = AES.MODE_CFB
    elif mode == 'OFB':
        mode = AES.MODE_OFB
    elif mode == 'CTR':
        mode = AES.MODE_CTR
    else:
        print '"{}" mode is in valid'.format(mode)

    print 'Decrypt {} with {} mode'.format(args[0], dict_opt['-m'])
    decrypt(mode, args[0], args[1])
    pass
