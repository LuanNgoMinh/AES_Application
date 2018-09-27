#!/usr/bin/env python
# -*- coding: utf-8 -*-
# decrypt.py –m <mode> <tên file input> <tên file output>
import sys, struct
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

            while True:
                block = encrypt_file.read(AES.block_size)
                if len(block) == 0:
                    break

                decrypted = aes.decrypt(block)
                decrypt_file.write(decrypted)
                # decrypt_file.truncate(size)
                
            decrypt_file.close()
            encrypt_file.close()
    pass


if __name__ == '__main__':
    mode = AES.MODE_ECB
    decrypt(mode, "HenMotMai.text.encrypted", "HenMotMai.text.decrypt")
    # decrypt(mode, "meo.jpg", "meo.decrypt.jpg")
    pass
