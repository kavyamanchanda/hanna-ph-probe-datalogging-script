import serial  # Importing the serial library for serial communication
import csv     # Importing the csv library for CSV file operations
import time    # Importing the time library for time-related operations

# List to check for over range or under range reading status
bad_reading_status = ['RO','RU','OR','UR','OU','UO','UU','OO']

# Function to send a command to the device and receive its response
def send_command(ser, command):
    ser.write(command.encode('utf-8'))  # Sending the command to the device
    response = ser.readline().decode()  # Reading and decoding the response
    return response

# Function to record pH data into a CSV file
def record_pH_data(filename, num_samples, time_interval):
    try:
        # Establishing serial connection with the device
        with serial.Serial(port='/dev/tty.usbserial-FT7BPE6T', baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=1,xonxoff=0, rtscts=0) as ser: #sending command 8,N,1, no flow control
            ser.reset_input_buffer()  # Flushing input buffer
            print("Connection established")  # Printing status message

            # Opening CSV file for writing
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile) # Create a CSV file writer object
                writer.writerow(['Time'.ljust(20),'pH Value'.ljust(15),'Temperature (C)'.ljust(15),'mV Value'.ljust(10)])

                samples_taken = 0  # Variable to track the number of samples taken
                
                # Different slicing positions based on Meter Mode
                field_positions00 = {
        'meter_mode': slice(0, 2),
        'meter_status': slice(2, 4),
        'reading_status': slice(4, 6),
        'pH_value': slice(6, 17),
        'temperature': slice(24, 33),
        'mV_value' : slice(17,24)
    }
                field_positions01 = {
        'meter_mode': slice(0, 2),
        'meter_status': slice(2, 4),
        'reading_status': slice(4, 6),
        'pH_value': slice(6, 17),
        'temperature': slice(24, 33),
        'mV_value' : slice(17,24)
    }
                field_positions02 = {
        'meter_mode': slice(0, 2),
        'meter_status': slice(2, 4),
        'reading_status': slice(4, 6),
        'pH_value': slice(6, 17),
        'temperature': slice(24, 33),
        'mV_value' : slice(17,24)
    }
                # Meter Mode 03 means mV range, hence no pH value
                field_positions03 = {
        'meter_mode': slice(0, 2),
        'meter_status': slice(2, 4),
        'reading_status': slice(4, 6),
        'pH_value': 0,
        'temperature': slice(17, 27),
        'mV_value' : slice(6,17)
    }
                # Loop to continuously record pH data until specified number of samples is reached
                while samples_taken < num_samples:
                    try:
                        response = send_command(ser,'\x10RAS\r')  # Sending KF1 command to get pH data '\x16KF1\r'
                        #print("Received response:", repr(response))  # Debugging statement to print received response
                        if response.startswith('\x02') and len(response) > 3:  # Checking if response starts with STX or x02, and avoiding invalid responses
                            # Parsing the response to extract meter mode, meter status, pH value, temperature, and mV value.
                            data = response[1:]  # Splitting response to extract data fields
                            
                            meter_mode = data[0:2]  # Extracting meter mode
                            if meter_mode == '00':
                                extracted_data = {key: data[pos] for key, pos in field_positions00.items()}
                            if meter_mode == '01':
                                extracted_data = {key: data[pos] for key, pos in field_positions01.items()}
                            if meter_mode == '02':
                                extracted_data = {key: data[pos] for key, pos in field_positions02.items()}
                            if meter_mode == '03':
                                extracted_data = {key: data[pos] for key, pos in field_positions03.items()}
                                extracted_data.update({'pH_value': 'NaN'})
                            print("Data received: ",extracted_data)

                            current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Getting current time

                            # Writing pH data along with timestamp to CSV file
                            writer.writerow([current_time.ljust(20),extracted_data['pH_value'].ljust(15),extracted_data['temperature'].ljust(15),  extracted_data['mV_value'].ljust(10)])
                            # Incrementing samples taken count
                            samples_taken += 1

                            for i in bad_reading_status:
                                if i == extracted_data['reading_status']:
                                    writer.writerow("Bad Reading status, over range(O) or under range(U)")
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
