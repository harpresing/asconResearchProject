import ascon
import aes
import random
import cProfile
import json
import pstats
import time
import matplotlib.pyplot as plt
import platform

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

def benchmark_ascon(key, data, variant="Ascon-128"):
    nonce = generate_binary_data(16)
    associateddata = generate_binary_data(0)

    profiler = cProfile.Profile()
    profiler.enable()

    ascon_encrypted = encrypt_with_ascon(key, nonce, associateddata, data, variant)
    ascon_decrypted = decrypt_with_ascon(key, nonce, associateddata, ascon_encrypted, variant)

    profiler.disable()
    stats = pstats.Stats(profiler)
    execution_time = stats.total_tt
    
    assert ascon_decrypted == data

    return execution_time

def log(msg):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - {msg}")

def read_data_as_bytes(size):
    size_in_bytes = int(size * 1024 * 1024)
    # Image size is 2.7 MB
    if size == 2.7:
            image_path = 'resources/IMG_1844.jpeg'
            with open(image_path, 'rb') as file:
                binary_data = file.read()
                data = binary_data
    # Video size is 3 MB            
    elif size == 3.0:
        video_path = 'resources/IMG_1937.MOV'
        chunk_size = 1024
        with open(video_path, 'rb') as file:
            binary_data = b''
            while chunk := file.read(chunk_size):
                binary_data += chunk
                data = binary_data
    else:
        data = generate_binary_data(size_in_bytes)
    return data


def measure_performance(algorithm, sizes):
    perf_metrics = []

    for size in sizes:
        log(f"Measuring performance for {algorithm} with {size} MB data")

        key = generate_binary_data(16)
        data = read_data_as_bytes(size)        

        if algorithm == "AES-128":
            execution_time = benchmark_aes(key, data)
        elif algorithm == "ASCON-128": 
            execution_time = benchmark_ascon(key, data)
        else:
            execution_time = benchmark_ascon(key, data, "Ascon-128a")    
        

        perf_metrics.append({
            "size": f"{size}MB",
            "executionTimeInSeconds": execution_time
        })
        log(f"Execution time for {algorithm} with {size} MB data: {execution_time} seconds")

    return {"algorithm": algorithm, "perfMetrics": perf_metrics}

def update_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_bar_chart(json_data, system_info, input_type):
    # Extract data for plotting
    algorithms = [entry["algorithm"] for entry in json_data]
    sizes = [metric["size"] for metric in json_data[0]["perfMetrics"]]
    execution_times_ascon_128 = [metric["executionTimeInSeconds"] for metric in json_data[0]["perfMetrics"]]
    execution_times_ascon_128a = [metric["executionTimeInSeconds"] for metric in json_data[1]["perfMetrics"]]
    execution_times_aes = [metric["executionTimeInSeconds"] for metric in json_data[2]["perfMetrics"]]
    
    
    # Plotting
    bar_width = 0.2
    index = range(len(sizes))

    fig, ax = plt.subplots()
    bar1 = ax.bar(index, execution_times_aes, bar_width, label='AES-128')
    bar2 = ax.bar([i + bar_width for i in index], execution_times_ascon_128, bar_width, label='ASCON-128')
    bar3 = ax.bar([i + bar_width * 2 for i in index], execution_times_ascon_128a, bar_width, label='ASCON-128a')


    # Add labels, title, and legend
    ax.set_xlabel('Size (MB)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Authenticated Encryption Comparison on ' + system_info)
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(sizes)
    ax.legend()

    # Show the plot
    # plt.show()
    plt.savefig(f'results/{platform.system()}/perfResult-{input_type}-{system_info}.png')
    plt.close()


def execute_perf_test(algorithms, data_sizes, input_type):
    performance_data = []

    for algorithm in algorithms:
        performance_data.append(measure_performance(algorithm, data_sizes))

    # Update the JSON file with performance metrics
    system_info = f"{platform.system()}-{platform.release()}"    
    update_json_file(f'results/{platform.system()}/perfResult-{input_type}-{system_info}.json', performance_data)

    # Generate and display the bar chart
    generate_bar_chart(performance_data, system_info, input_type)


if __name__ == "__main__":
    algorithms = ["ASCON-128", "ASCON-128a", "AES-128"]
    data_sizes = [0.1, 0.4, 0.8, 1.2]  # in MB
    execute_perf_test(algorithms, data_sizes, "text")

    image_sizes = [2.7]
    execute_perf_test(algorithms, image_sizes, "image")

    video_size = [3.0]
    execute_perf_test(algorithms, video_size, "video")
    
