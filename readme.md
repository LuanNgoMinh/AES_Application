# CRYPTO APPLICATION

`git: https://github.com/LuanNgoMinh/crypto_Application`

## ENCRYPT - DECRYPT
### Suppported Mode
* ECB 
* CBC 
* CFB 
* OFB 
* CTR

### Content
Encrypt file with AES Mode and IV

#### Command
``` shell
python encrypt.py -m <AES_Mode> -i <Initialization_Vector> <plan_text_file> <cipher_text_file>
```

#### Example
```shell
python encrypt.py -m CFB -i "meo con xinh xan" HenMotMai.text HenMotMai.cipher
```

### Decrypt file
Decrypt file with AES Mode
#### Command
``` shell
python decrypt.py -m <AES_Mode> <cipher_text_file> <plain_text_file>
```

#### Example
```shell
python decrypt.py -m CFB HenMotMai.cipher HenMotMai.data
```
### Testing
Auto encrypt and decrypt file. After that, compare sha256 checksum origin file and decrypt_file <br>
Encrypt and decrypt file storage at test_space dir in same folder with test file

#### Command
```shell
sudo chmod +x test
./test <file_1> <file_2> <file_3> ...
```

#### Example:
``` shell
./test sunflower.jpg HenMotMai.text testcase1
```

#### Output
```shell
... some log ...
=> CFB true: origin_file_name
... some log ...
=> CTR true: origin_file_name
... some log ...
=> OFB false: origin_file_name
```

## CHECKSUM
Generate checksum from a file. Verify file from check sum
### Hash mode support
* SHA
* SHA256
* MD5
### Generate checksum
#### Command
```shell
./checksum.py -h <hash mode> <filename>
```

#### Example
```shell
./checksum.py -h SHA256 sunflower.jpg
```

### Compare file with checksum
#### Command
```shell
./checksum.py -h <hash mode> -c <checksum> <filename>
```

#### Example
```shell
    ./checksum.py -h SHA256 -c 08ad5b6cf4f282bc3044ea437c239ebae398daa17dd366141ba6c883bccabd7b sunflower.jpg
```

## DIGITAL SIGNATURE

### Sign a file
#### Command
```shell
./sign.py -h <hash_mode> <file_need_signing> <signature_file>
```
#### Example
```shell
./sign.py -h MD5 HenMotMai.text HenMotMai.signature
```

### Verify signature
#### Command
```shell
./sign.py -h <hash_mode> <receive_file> <signature_file>
```

#### Example
```shell
./verify_sign.py -h SHA256 HenMotMai.text HenMotMai.signature
```