import subprocess
import os
import argparse
import signal
import time
import sys
import logging

# Set up logging
def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )

def execute_payload(payload_path, log_path):
    # Check if the payload exists before execution
    if not os.path.isfile(payload_path):
        logging.error("Error: Payload file '" + payload_path + "' does not exist.")
        return None
    
    try:
        # Open the payload script in the background using subprocess
        process = subprocess.Popen(
            ["nohup", payload_path],
            stdout=open(log_path, "a"),
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp  # This detaches the process from the parent
        )

        logging.info("Payload launched with PID: " + str(process.pid))
        return process

    except Exception as e:
        logging.error("Failed to execute payload: " + str(e))
        return None

def check_process_status(pid):
    """Checks if a process with the given PID is running."""
    try:
        os.kill(pid, 0)  # Sending signal 0 checks if the process exists
        return True
    except OSError:
        return False

def retry_payload(payload_path, log_path, max_retries=3, retry_delay=10):
    """Retry logic to launch payload."""
    attempt = 0
    while attempt < max_retries:
        process = execute_payload(payload_path, log_path)
        if process:
            logging.info("Payload executed successfully on attempt " + str(attempt + 1))
            return process
        else:
            attempt += 1
            logging.warning("Retrying in " + str(retry_delay) + " seconds...")
            time.sleep(retry_delay)
    logging.error("Failed to execute payload after " + str(max_retries) + " attempts.")
    return None

def execute_payload_with_timeout(payload_path, log_path, timeout=60):
    """Executes the payload and ensures it finishes within a timeout."""
    process = execute_payload(payload_path, log_path)
    if not process:
        return

    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(5)
        if not check_process_status(process.pid):
            logging.info("Process " + str(process.pid) + " finished within the timeout.")
            return
    
    if check_process_status(process.pid):
        logging.warning("Process " + str(process.pid) + " exceeded timeout. Terminating...")
        os.kill(process.pid, signal.SIGTERM)  # Graceful termination
        time.sleep(2)
        if check_process_status(process.pid):
            logging.error("Process " + str(process.pid) + " did not terminate gracefully, forcing kill.")
            os.kill(process.pid, signal.SIGKILL)

def signal_handler(sig, frame):
    logging.info("Interrupt received, stopping the process...")
    sys.exit(0)

def main():
    # Set up argparse to take the payload path and log file path as arguments
    parser = argparse.ArgumentParser(description="Python Wrapper to execute payload in the background.")
    parser.add_argument("--payload", type=str, required=True, help="The path to the payload script.")
    parser.add_argument("--log", type=str, required=True, help="The path to the log file.")
    parser.add_argument("--timeout", type=int, default=60, help="Maximum time in seconds for the payload to run.")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries in case the payload fails.")
    parser.add_argument("--retry_delay", type=int, default=10, help="Delay in seconds between retries.")
    
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log)

    # Handle system signals (e.g., Ctrl+C or kill signals)
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle kill signal

    # Retry launching the payload with timeout
    process = retry_payload(args.payload, args.log, max_retries=args.retries, retry_delay=args.retry_delay)

    # If the process starts successfully, monitor it with a timeout
    if process:
        logging.info("Monitoring process " + str(process.pid) + " with a timeout of " + str(args.timeout) + " seconds.")
        execute_payload_with_timeout(args.payload, args.log, timeout=args.timeout)

if __name__ == "__main__":
    main()
