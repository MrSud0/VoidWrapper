# VoidWrapper

VoidWrapper is a flexible Python-based tool designed to wrap any script or executable and run it as a background process. Inspired by **Jujutsu Kaisen** and its theme of domain expansion, VoidWrapper ensures that your scripts execute silently, infinitely, and without blocking other tasks.

## Features
- Run any script or executable as a background process.
- Customizable logging of script output.
- Retry mechanism to ensure your script runs reliably.
- Timeout control to prevent runaway processes.
- Robust signal handling to gracefully stop or terminate background tasks.
- Configurable retry delays and maximum retry attempts.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/VoidWrapper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd VoidWrapper
   ```
3. Install any necessary dependencies (if any).

## Usage

VoidWrapper can execute any script or executable in the background. You can configure the payload, log file, and additional options like retries and timeouts via command-line arguments.

### Example
To run a payload script `payload.sh` as a background process and log the output to `payload.log`, use the following command:

```bash
python3 voidwrapper.py --payload /path/to/payload.sh --log /path/to/payload.log --timeout 120 --retries 3 --retry_delay 10
```

### Command-line Arguments
- `--payload`: (Required) The path to the script or executable you want to run.
- `--log`: (Required) The path to the log file where output and errors will be captured.
- `--timeout`: (Optional) Maximum time (in seconds) the payload is allowed to run. If exceeded, the process will be terminated. Default is 60 seconds.
- `--retries`: (Optional) The number of times to retry executing the payload if it fails. Default is 3 retries.
- `--retry_delay`: (Optional) Time (in seconds) to wait between retries. Default is 10 seconds.

### Sample Commands

1. **Basic Usage**:
   ```bash
   python3 voidwrapper.py --payload /tmp/myscript.sh --log /tmp/myscript.log
   ```

2. **With Timeout and Retries**:
   ```bash
   python3 voidwrapper.py --payload /tmp/myscript.sh --log /tmp/myscript.log --timeout 120 --retries 5 --retry_delay 15
   ```

## How It Works

VoidWrapper launches any specified script or executable using Python's `subprocess` module, detaching it from the parent process and running it in the background using `nohup`. This ensures that your scripts run silently, even after Ansible or terminal sessions are closed.

The tool also features:
- **Timeout Handling**: If a script exceeds the defined timeout, it will be forcefully terminated.
- **Retries**: If a script fails, VoidWrapper will retry it according to the configured retry attempts and delay.
- **Logging**: Output and errors are redirected to the log file specified via the `--log` argument.

## Signals Handling
VoidWrapper gracefully handles interruptions like `SIGINT` or `SIGTERM`, ensuring the tool shuts down properly and prevents orphaned processes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or find bugs.

## Acknowledgments
VoidWrapper was inspired by the anime **Jujutsu Kaisen** and its "Infinite Void" domain expansion, symbolizing an infinite background process that runs silently, with immense power behind the scenes.
