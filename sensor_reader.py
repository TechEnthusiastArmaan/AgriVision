import serial
import time

arduino_port = "COM5"  # Replace with your port
baud_rate = 9600
num_entries = 2  # Set the number of entries you want to read

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
    time.sleep(2)

    for _ in range(num_entries):
        line = ser.readline().decode("utf-8").strip()
        if line:
            try:
                temp, hum, soil, air = map(float, line.split(","))
                print(f"Temperature: {temp}°C | Humidity: {hum}% | Soil Moisture: {soil} | Air Quality: {air}")
            except ValueError:
                print("Waiting for valid data...")

except serial.SerialException:
    print("Could not connect to Arduino. Check port and cable.")
