# Research Project in Lightweight Cryptography

This repository containes source code for the research project in lightweight cryptography.

+ `Student Name`: Harpreet Singh
+ `Student ID`: B00158316
+ `Course`: MACS H6014

## Structure of the repository

The repository contains the following files:

1. `ascon.py` - Taken from the original [repository](https://github.com/meichlseder/pyascon/tree/5ee786cdc8a74d9c0f7b3c81f99f5dcb5490ca00) which implements Ascon v1.2 in Python 3. This implementation was submitted to the NIST LWC competition. The following functions that implement `Authenticated Encryption` were used from the file as part of the research project:

    - ascon_encrypt(key, nonce, associateddata, plaintext, variant)
    - ascon_decrypt(key, nonce, associateddata, ciphertext, variant)

2. `aes.py` - Implements AES-128 in Python 3. `CBC mode` is used for encryption and decryption followed by `HMAC-SHA256` for authentication. This implementation was taken from this [repository](https://github.com/boppreh/aes). The following functions were used from the file as part of the research project:
    - aes_encrypt(key, plaintext)
    - aes_decrypt(key, ciphertext)

3. `benchmark.py` - This file contains the code for benchmarking the performance of `Authenticated Encryption` performed by ASCON-128, ASCON-128a and AES-128. It uses `cProfile` to measure execution times and the results are stored in the results directory based on which environment the code is executed on. We executed the benchmarking on two environments:
    - Raspberry Pi VM (Debian 11, (4GB RAM, 4 virtual Processors) - Image taken from [here](https://downloads.raspberrypi.com/rpd_x86/images/rpd_x86-2022-07-04/2022-07-01-raspios-bullseye-i386.iso). The VM was created using VirtualBox.
    - MacBook Pro (15-inch, 2015) (2.2 GHz Quad-Core Intel Core i7, 16 GB 1600 MHz DDR3)

The execution results are stored json files and subsequently used for plotting the graphs.


## How to run the code

1. Install the required dependencies using the following command:
    
    ```bash
    pip3 install -r requirements.txt --user
    ```
2. Run the benchmarking code using the following command:
    
    ```bash
    python3 benchmark.py
    ```    