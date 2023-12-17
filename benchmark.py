import cProfile
import ascon
import aes

def generate_binary_data(length):
    return bytes(bytearray([i % 256 for i in range(length)]))


def encrypt_with_aes(key, iv, data):
    return aes.AES(key).encrypt_ctr(data, iv)


def decrypt_with_aes(key, iv, data):
    return aes.AES(key).decrypt_ctr(data, iv)


def encrypt_with_ascon(key, nonce, associateddata, plaintext, variant="Ascon-128"):
    return ascon.ascon_encrypt(key, nonce, associateddata, plaintext, variant)


def decrypt_with_ascon(key, nonce, associateddata, ciphertext, variant="Ascon-128"):
    return ascon.ascon_decrypt(key, nonce, associateddata, ciphertext, variant)


def benchmark_aes(plaintext_size):
    key = generate_binary_data(16)
    iv = generate_binary_data(16)
    data = generate_binary_data(plaintext_size)

    profiler = cProfile.Profile()
    profiler.enable()
    aes_encrypted = encrypt_with_aes(key, iv, data)
    aes_decrypted = decrypt_with_aes(key, iv, aes_encrypted)
    profiler.disable()
    profiler.print_stats()

    assert aes_decrypted == data

def benchmark_ascon(plaintext_size):
    key = generate_binary_data(16)
    nonce = generate_binary_data(16)
    associateddata = generate_binary_data(32)
    plaintext = generate_binary_data(plaintext_size)

    profiler = cProfile.Profile()
    profiler.enable()
    ascon_encrypted = encrypt_with_ascon(key, nonce, associateddata, plaintext)
    ascon_decrypted = decrypt_with_ascon(key, nonce, associateddata, ascon_encrypted)
    profiler.disable()
    profiler.print_stats()
    
    assert ascon_decrypted == plaintext    

if __name__ == "__main__":
    benchmark_ascon(1024 * 1024) 
    benchmark_aes(1024 * 1024)