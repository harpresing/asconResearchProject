import ascon
import aes
import random
import cProfile
import json
import pstats
import time
import matplotlib.pyplot as plt

def generate_binary_data(length):
    return bytes(bytearray([random.randint(0, 255) for _ in range(length)]))

def encrypt_with_aes(key, iv, data):
    return aes.AES(key).encrypt_ctr(data, iv)


def decrypt_with_aes(key, iv, data):
    return aes.AES(key).decrypt_ctr(data, iv)


def encrypt_with_ascon(key, nonce, associateddata, plaintext, variant="Ascon-128"):
    return ascon.ascon_encrypt(key, nonce, associateddata, plaintext, variant)


def decrypt_with_ascon(key, nonce, associateddata, ciphertext, variant="Ascon-128"):
    return ascon.ascon_decrypt(key, nonce, associateddata, ciphertext, variant)


def benchmark_aes(key, data):
    iv = generate_binary_data(16)

    profiler = cProfile.Profile()
    profiler.enable()

    aes_encrypted = encrypt_with_aes(key, iv, data)
    aes_decrypted = decrypt_with_aes(key, iv, aes_encrypted)

    profiler.disable()
    stats = pstats.Stats(profiler)
    execution_time = stats.total_tt

    assert aes_decrypted == data

    return execution_time

def benchmark_ascon(key, data):
    nonce = generate_binary_data(16)
    associateddata = generate_binary_data(32)

    profiler = cProfile.Profile()
    profiler.enable()

    ascon_encrypted = encrypt_with_ascon(key, nonce, associateddata, data)
    ascon_decrypted = decrypt_with_ascon(key, nonce, associateddata, ascon_encrypted)

    profiler.disable()
    stats = pstats.Stats(profiler)
    execution_time = stats.total_tt
    
    assert ascon_decrypted == data

    return execution_time

def log(msg):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - {msg}")      

def measure_performance(algorithm, sizes):
    perf_metrics = []

    for size in sizes:
        log(f"Measuring performance for {algorithm} with {size} MB data")
        
        profiler = cProfile.Profile()
        profiler.enable()

        size_in_bytes = size * 1024 * 1024

        key = generate_binary_data(16)
        data = generate_binary_data(size_in_bytes)

        if algorithm == "AES-128":
            benchmark_aes(key, data)
        else: 
            benchmark_ascon(key, data)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        execution_time = stats.total_tt

        perf_metrics.append({
            "size": f"{size}MB",
            "executionTimeInSeconds": execution_time
        })
        log(f"Execution time for {algorithm} with {size} MB data: {execution_time} seconds")

    return {"algorithm": algorithm, "perfMetrics": perf_metrics}

def update_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_bar_chart(json_data):
    # Extract data for plotting
    algorithms = [entry["algorithm"] for entry in json_data]
    sizes = [metric["size"] for metric in json_data[0]["perfMetrics"]]
    execution_times_aes = [metric["executionTimeInSeconds"] for metric in json_data[0]["perfMetrics"]]
    execution_times_ascon = [metric["executionTimeInSeconds"] for metric in json_data[1]["perfMetrics"]]

    # Plotting
    bar_width = 0.35
    index = range(len(sizes))

    fig, ax = plt.subplots()
    bar1 = ax.bar(index, execution_times_aes, bar_width, label='AES-128')
    bar2 = ax.bar([i + bar_width for i in index], execution_times_ascon, bar_width, label='ASCON-128')

    # Add labels, title, and legend
    ax.set_xlabel('Size (MB)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Algorithm Comparison')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(sizes)
    ax.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    algorithms = ["AES-128", "ASCON-128"]
    data_sizes = [1, 2]  # in MB

    performance_data = []

    for algorithm in algorithms:
        performance_data.append(measure_performance(algorithm, data_sizes))

    # Update the JSON file with performance metrics
    update_json_file('perfResult.json', performance_data)

    # Generate and display the bar chart
    generate_bar_chart(performance_data)