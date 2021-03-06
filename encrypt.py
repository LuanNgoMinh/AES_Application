#!/usr/bin/env python
#-*- coding: utf-8 -*-
#usage: encrypt.py –m <mode> –i <IV> <tên file input> <tên file output>
import os, sys, getopt
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
from Crypto.Util import Counter

#Key for aes encryption
secret_key = 'conmeoconxinhxan'
padding = chr(0xAA)

def encrypt(mode, iv, input, output):
    key = SHA256.new(secret_key).digest()
    iv = MD5.new(iv).digest()
    aes = None

    if mode == AES.MODE_CTR:
        ctr = Counter.new(128, initial_value=long(iv.encode("hex"), 16))
        aes = AES.new(key, mode, counter=ctr)
    else:
        aes = AES.new(key, mode, iv)
   
    with open(output, "wb") as encrypt_file:
            with open(input, "rb") as plantext_file:
                encrypt_file.write(iv)

                while True:
                    block = plantext_file.read(AES.block_size)
                    if len(block) == 0:
                        break

                    if len(block) % 16 != 0:
                        padding_length = aes.block_size - (len(block) % aes.block_size)
                        encrypt_file.write(aes.encrypt(block + padding_length * chr(padding_length)))
                        break

                    encrypted = aes.encrypt(block)
                    encrypt_file.write(encrypted)

                plantext_file.close()
                encrypt_file.close()
    
    print "Encrypt success"
    pass


def usage():
    print \
    '''Usage:\n\n\tpython encrypt.py or ./encrypt.py -m <mode> -i <IV> <input file name> <output file name>
\n\t-mode: mode to encryption: ECB, CBC, CFB, OFB, CTR, OPENPGP
\n\t-i: initialization vector, a string randomly
\nExample: ./encrypt.py -m CFB -i meoconxinhxinh meomeo.text meomeo.encrypted
    '''

if __name__ == '__main__':
    if len(sys.argv) != 7:
        usage()
        exit(1)

    mode, iv = None, None
    
    #Getopt
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:i:')
    except getopt.error:
        print 'Get options error'
        exit(2)

    #Check file name options    
    if len(args) != 2:
        print 'File name error'
        usage()
        exit(1)

    #check optlist
    if len(optlist) != 2:
        print 'Optlist error'
        usage()
        exit(1)

    dict_opt = dict((o, a) for o, a in optlist)
    mode = dict_opt['-m']
    iv = dict_opt['-i']

    #check input file has existed yet
    if not os.path.isfile(args[0]):
        print '"{}" file has not existed yet'.format(args[0])
        exit(3)
    
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
        exit(4)

    print 'Encrypt {} with {} mode'.format(args[0], dict_opt['-m'])
    encrypt(mode, iv, args[0], args[1])