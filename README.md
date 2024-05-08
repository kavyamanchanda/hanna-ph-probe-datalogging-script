# Hanna pH Probe Data Logging Script

## Overview
This Python script is designed to interface with a Hanna pH probe device over a serial connection (COM port or `/dev/ttyUSB0`). It allows you to record pH data from the device and store it in a CSV file along with corresponding timestamps.

## Functionality
The script performs the following functions:
- Connects to the Hanna pH probe device over a serial connection.
- Sends a command to the device to retrieve pH data, including pH value, temperature, and meter status.
- Parses the response from the device and stores the pH data in a CSV file.
- Records pH data at regular intervals for a specified number of samples.

## Requirements
- Python 3.x
- PySerial library (`pip install pyserial`)

## Usage
1. Connect the Hanna pH probe device to your computer via USB.
2. Ensure that the device is powered on and ready for communication.
3. Install Python 3.x if not already installed.
4. Install the PySerial library by running `pip install pyserial` in your terminal or command prompt.
5. Download the `hanna-probe-datalogger.py` script to your computer.

### Running the Script
1. Open a terminal or command prompt.
2. Navigate to the directory where the script (`hanna-probe-datalogger.py`) is located.
3. Run the script by executing the following command:
   ```
   python hanna-probe-datalogger.py
   ```
4. Follow the prompts to provide the following information:
   - Filename for the CSV file to store pH data.
   - Number of samples to be taken.
   - Time interval between samples (in seconds).

### Example
```
$ python hanna-probe-datalogger.py
Enter the name for the CSV file (e.g., pH_data.csv): data.csv
Enter the number of samples to be taken: 10
Enter the time interval between samples (in seconds): 5
Connection established
Recorded pH value: 7.01
Data value received: '<STX>00 0x01 7.01 25.00 0x10 <ETX>'
Recorded pH value: 7.02
Data value received: '<STX>00 0x01 7.02 25.00 0x10 <ETX>'
...
```

## Troubleshooting
- If you encounter any issues, ensure that the device is properly connected and powered on.
- Check that the correct COM port (Windows) or `/dev/ttyUSB0` (Linux) is selected in the script.
- Verify that the communication settings (baud rate, parity, stop bits) match those specified in the device manual.
- If the script fails to connect to the device, check for any errors reported in the terminal or command prompt.

## License
This script is provided under the [GPL V3](LICENSE).
