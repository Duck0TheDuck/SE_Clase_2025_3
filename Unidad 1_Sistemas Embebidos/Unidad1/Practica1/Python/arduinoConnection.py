import serial
from Misc.miscUtils import buscarPuertoArduino

puerto_arduino = buscarPuertoArduino()
baud_rate = 9600
matriz = []

def recibirSeñalesArduino(puerto_arduino=puerto_arduino, baud_rate=baud_rate, matriz=matriz, debug=False):
    try:
        ser = serial.Serial(puerto_arduino, baud_rate, timeout=1)
        print("Conexion establecida")
        while True:
            # Read and decode the incoming data
            line = ser.readline().decode("utf-8", errors="ignore").strip().split("-")
            
            if line:
                if debug:
                    print(f"Valores recibidos: {line}")

                try:
                    parsed_line = []
                    for item in line:
                        if item.isdigit():  
                            parsed_line.append(int(item))
                        else:  # Keep as string for non-numeric values
                            parsed_line.append(item)
                    
                    matriz.append(parsed_line)

                except Exception as e:
                    print(f"Error al procesar datos: {e}")

    except serial.SerialException as e:
        print(f"Error en la conexion serial: {e}")
        return matriz
    except KeyboardInterrupt:
        print("\nConexion terminada")
        return matriz
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto serial cerrado")
            return matriz
