import random
import time
import logging
from prometheus_client import start_http_server, Gauge, Histogram, Counter, Summary

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Metrics
CPU_USAGE = Gauge('cpu_usage', 'Random CPU usage percentage between 0 and 100')
MEMORY_USAGE = Gauge('memory_usage', 'Random memory usage percentage between 0 and 100')
DISK_IO = Gauge('disk_io', 'Random disk I/O operations per second')
NETWORK_BANDWIDTH = Gauge('network_bandwidth', 'Random network bandwidth usage in Mbps')

REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request',
                         buckets=[0.1, 0.2, 0.5, 1, 2, 5, 10])

ERROR_COUNTER = Counter('error_total', 'Total number of errors')
UPDATE_COUNTER = Counter('update_total', 'Total number of metric updates')

MEMORY_SUMMARY = Summary('memory_summary', 'Summary of memory usage values')

def generate_random_metrics():
    while True:
        try:
            update_metrics()
            log_metrics()
            
            # Simulate occasional high-load conditions
            if random.random() < 0.05:
                simulate_high_load()

            time.sleep(1)

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            ERROR_COUNTER.inc()

def update_metrics():
    CPU_USAGE.set(random.uniform(0, 100))
    memory_usage = random.uniform(0, 100)
    MEMORY_USAGE.set(memory_usage)
    MEMORY_SUMMARY.observe(memory_usage)
    DISK_IO.set(random.uniform(0, 500))
    NETWORK_BANDWIDTH.set(random.uniform(0, 1000))

    with REQUEST_TIME.time():
        process_time = random.uniform(0, 3)
        time.sleep(process_time)

    if random.random() < 0.1:
        ERROR_COUNTER.inc()
        logging.warning("An error occurred during metric generation")

    UPDATE_COUNTER.inc()

def log_metrics():
    logging.info(f"Metrics updated: CPU={CPU_USAGE._value.get():.2f}%, "
                 f"Memory={MEMORY_USAGE._value.get():.2f}%, "
                 f"Disk I/O={DISK_IO._value.get():.2f} ops/s, "
                 f"Network Bandwidth={NETWORK_BANDWIDTH._value.get():.2f} Mbps")

def simulate_high_load():
    condition = random.choice(['cpu_spike', 'memory_leak', 'disk_thrashing'])
    if condition == 'cpu_spike':
        CPU_USAGE.set(random.uniform(90, 100))
        logging.warning("Simulated high CPU usage")
    elif condition == 'memory_leak':
        MEMORY_USAGE.set(random.uniform(90, 100))
        logging.warning("Simulated memory leak")
    else:  # disk_thrashing
        DISK_IO.set(random.uniform(400, 500))
        logging.warning("Simulated disk thrashing")

if __name__ == '__main__':
    try:
        port = 8000
        start_http_server(port)
        logging.info(f"Exporter started on port {port}")
        generate_random_metrics()
    except KeyboardInterrupt:
        logging.info("Exporter stopped by user")
    except Exception as e:
        logging.error(f"Failed to start exporter: {str(e)}")

