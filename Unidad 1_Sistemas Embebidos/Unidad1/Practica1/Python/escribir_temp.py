import serial
import csv
from datetime import datetime
import serial.tools.list_ports
import time

VID = 0x1a86
PID = 0x7523

def buscarPuertoArduino(vid=VID, pid=PID):
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        if puerto.vid == vid and puerto.pid == pid:
            return puerto.device
    return None

def main():
    puerto = buscarPuertoArduino()
    if not puerto:
        print("No Arduino found")
        return

    try:
        ser = serial.Serial(puerto, 9600, timeout=1)
        time.sleep(10)  # Allow time for serial connection to initialize

        with open('sensor_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Temperature', 'Humidity'])
            
            while True:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        data = line.split(',')
                        if len(data) == 3:  # Ensure correct data format
                            writer.writerow(data)
                            file.flush()
                except Exception as e:
                    print(f"Error reading data: {e}")
                    break

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")

if __name__ == "__main__":
    main()