# Hanna pH Probe Data Logging Script

## Overview
This Python script is designed to interface with a Hanna pH probe device over a serial connection (COM port or `/dev/ttyUSB0`). Do change the port depending on the port on your device. This can be checked in MacOS by typing in Terminal: ls /dev/tty.*. 

The script allows you to record pH data, temperature and mV value from the device and store it in a CSV file along with corresponding timestamps.

## Functionality
The script performs the following functions:
- Connects to the Hanna pH probe device over a serial connection.
- Sends a command in the format of <command prefix><command><CR> to the device to retrieve a response with:
      - Meter Mode (2 chars):
         00 - pH range (0.001 resolution)
         01 - pH range (0.01 resolution)
         02 - pH range (0.1 resolution)
         03 - mV range
      - Meter Status (2 chars):
         0x10 - temperature probe is connected
         0x01 - new GLP data available
         0x02 - new SETUP parameter
         0x04 - out of calibration range
         0x08 - the meter is in autoend point mode
      - Reading status (2 chars):
         R - in range
         O - over range
         U - under range
         First character corresponds to the primary reading. Second character corresponds to mV reading.
      - Primary reading (corresponding to the selected range) - 11 ASCII chars, including sign, decimal point and exponent.
      - Secondary reading (only when primary reading is not mV) - 7 ASCII chars, including sign and decimal point.
      - Temperature reading - 7 ASCII chars, with sign and two decimal points, always in degree C.
- Parses this response from the device and stores the pH value, mV value and temperature in a CSV file.
- Records pH data at regular intervals for a specified number of samples, both given as input by the user.

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
