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
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:  # Establishing serial connection with the device
        ser.flushInput()  # Flushing input buffer

        # Printing status message
        print("Connection established")

        # Opening CSV file for writing
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Time', 'pH Value']  # Defining field names for CSV file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Creating CSV writer object
            writer.writeheader()  # Writing header row to CSV file

            samples_taken = 0  # Variable to track the number of samples taken
            # Loop to continuously record pH data until specified number of samples is reached
            while samples_taken < num_samples:
                try:
                    # Sending command to device to get pH data
                    response = send_command(ser, 'RAS\r')
                    # Checking if response starts with the expected start-of-text character
                    if response.startswith('<STX>'):
                        # Extracting pH value from response
                        pH_reading = response.split()[1]
                        # Getting current time
                        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        # Writing pH data along with timestamp to CSV file
                        writer.writerow({'Time': current_time, 'pH Value': pH_reading})
                        # Printing recorded pH value
                        print(f"Recorded pH value: {pH_reading}")
                        samples_taken += 1  # Incrementing samples taken count
                    else:
                        # Printing error message if response format is unexpected
                        print("Error receiving pH data")
                except KeyboardInterrupt:
                    # Handling keyboard interrupt (Ctrl+C) to stop recording
                    print("Recording stopped")
                    break
                time.sleep(time_interval)  # Waiting for specified time interval between samples

if __name__ == "__main__":
    # Getting filename for CSV file from user
    filename = input("Enter the name for the CSV file (e.g., pH_data.csv): ")
    # Getting number of samples to be taken from user
    num_samples = int(input("Enter the number of samples to be taken: "))
    # Getting time interval between samples from user
    time_interval = float(input("Enter the time interval between samples (in seconds): "))
    # Calling function to record pH data with provided parameters
    record_pH_data(filename, num_samples, time_interval)
