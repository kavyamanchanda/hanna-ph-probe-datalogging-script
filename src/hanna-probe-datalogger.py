import serial  # Importing the serial library for serial communication
import csv  # Importing the csv library for CSV file operations
import time  # Importing the time library for time-related operations

# Function to send a command to the device and receive its response
def send_command(ser, command):
    ser.write(command.encode())  # Sending the command to the device
    response = ser.readline().decode().strip()  # Reading and decoding the response
    return response

# Function to record pH data into a CSV file
def record_pH_data(filename, num_samples, time_interval):
    try:
        # Establishing serial connection with the device
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.flushInput()  # Flushing input buffer
            print("Connection established")  # Printing status message

            # Opening CSV file for writing
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Time', 'pH Value', 'Temperature', 'Meter Status']  # Defining field names for CSV file
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Creating CSV writer object
                writer.writeheader()  # Writing header row to CSV file

                samples_taken = 0  # Variable to track the number of samples taken
                # Loop to continuously record pH data until specified number of samples is reached
                while samples_taken < num_samples:
                    try:
                        response = send_command(ser, 'RAS\r')  # Sending RAS command to get pH data
                        print("Received response:", repr(response))  # Debugging statement to print received response
                        if response.startswith('<STX>'):  # Checking if response starts with STX
                            # Parsing the response to extract meter mode, meter status, pH value, temperature, etc.
                            data = response.split()[1:]  # Splitting response to extract data fields
                            meter_mode = data[0]  # Extracting meter mode
                            meter_status = data[1]  # Extracting meter status
                            pH_value = data[2]  # Extracting pH value
                            temperature = data[3]  # Extracting temperature
                            current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Getting current time
                            # Writing pH data along with timestamp to CSV file
                            writer.writerow({'Time': current_time, 'pH Value': pH_value, 'Temperature': temperature, 'Meter Status': meter_status})
                            # Incrementing samples taken count
                            samples_taken += 1
                            print(f"Recorded pH value: {pH_value}")  # Printing recorded pH value
                            print("Data value received:", repr(response))  # Print the entire response received for debugging
                        else:
                            print("Error receiving pH data")  # Printing error message if response format is unexpected
                    except KeyboardInterrupt:
                        print("Recording stopped")  # Handling keyboard interrupt (Ctrl+C) to stop recording
                        break
                    time.sleep(time_interval)  # Waiting for specified time interval between samples
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")  # Handling serial port opening failure

# Entry point of the script
if __name__ == "__main__":
    filename = input("Enter the name for the CSV file (e.g., pH_data.csv): ")  # Getting filename for CSV file from user
    num_samples = int(input("Enter the number of samples to be taken: "))  # Getting number of samples to be taken from user
    time_interval = float(input("Enter the time interval between samples (in seconds): "))  # Getting time interval between samples from user
    
    # Call function to record pH data with provided parameters
    record_pH_data(filename, num_samples, time_interval)
