import serial
import time

# Define command prefixes
COMMAND_PREFIX = {
    "KF1": "KF1", 
    "KF2": "KF2", 
    "KF3": "KF3", 
    "OFF": "OFF", 
    "CHR": "CHR", 
    "RAS": "RAS", 
    "PAR": "PAR", 
    "MDR": "MDR", 
    "GLP": "GLP", 
    "NSL": "NSL", 
    "LODP": "LODP", 
    "LODPALL": "LODPALL"
}

# Define command descriptions
COMMAND_DESCRIPTIONS = {
    "KF1": "Presses functional key 1", 
    "KF2": "Presses functional key 2", 
    "KF3": "Presses functional key 3", 
    "OFF": "Presses OFF key", 
    "CHR": "Changes instrument range according to parameter value", 
    "RAS": "Causes the instrument to send a complete set of readings", 
    "PAR": "Requests the setup parameters setting", 
    "MDR": "Requests the instrument model name and firmware code", 
    "GLP": "Requests the calibration data record", 
    "NSL": "Requests the number of logged samples", 
    "LODP": "Requests pH record logged data", 
    "LODPALL": "Requests all pH Log on demand"
}

def send_command(ser, command):
    """
    Sends a command over the serial port.

    Args:
        ser (Serial): The serial port object.
        command (str): The command to be sent.
    """
    # Encode the command to ASCII and send it over serial
    ser.write(command.encode('ascii'))
    # Optional: Wait for a short time for the command to be processed
    time.sleep(0.1)

def receive_response(ser):
    """
    Receives and prints the response from the serial port.

    Args:
        ser (Serial): The serial port object.
    """
    # Read response from serial and decode it
    response = ser.readline().decode('ascii').strip()
    print("Response:", response)

def main():
    # Define the serial port and baud rate
    serial_port = '/dev/ttyUSB0'  # Change this to your serial port
    baud_rate = 9600  # Change this to match your device's baud rate

    # Create a serial object
    ser = serial.Serial(serial_port, baud_rate)

    # Open the serial port
    if not ser.is_open:
        ser.open()

    try:
        # Loop through each command
        for command, prefix in COMMAND_PREFIX.items():
            description = COMMAND_DESCRIPTIONS[command]
            full_command = f"{prefix} {command}\r\n"
            print(f"Sending command: {full_command.strip()} - {description}")
            send_command(ser, full_command)
            receive_response(ser)
            print()  # Add an empty line for readability

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Exiting...")

    finally:
        # Close the serial port
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
