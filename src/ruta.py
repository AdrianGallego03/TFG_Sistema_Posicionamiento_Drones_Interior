"""
Script para recoger datos del dron y guardarlos en un archivo de texto.
"""
import time
import os
from datetime import datetime

def main(file_name):
    """
    Función principal que recoge datos del dron y los guarda en un archivo de texto.
    Args:
        file_name: Nombre del archivo donde se guardarán los datos.
    """
    
    # Obtener la ruta del directorio actual del script 
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ruta completa al archivo
    file_path = os.path.join(current_dir, "..\\Rutas", file_name)

    # Comprobar que el dron está armado antes de empezar a recoger datos
    # Descomentar las siguientes líneas si se quiere esperar a que el dron esté armado, 
    # o si se va a realizar una ruta volando
    #
    # while True:
    #        armed = cs.armed  
    #        if armed == True:
    #            break
    #        print("El dron no esta armado")
    #        Script.Sleep(1000)
    
    with open(file_path, 'w') as file:
        file.write('opt_m_x, opt_m_y, opt_qua, yaw, alt, battery_V\n')  # Encabezado del archivo
        
        print("opt_m_x, opt_m_y, opt_qua, yaw, alt, battery_V\n")
            
        # Desconmentar la siguiente línea si se quiere realizar una ruta completa con el dron volando
        # while cs.armed:
        
        # Comentar las siguientes líneas si se quiere realizar una ruta completa con el dron volando
        i = 20
        while i > 0:
            
            # Obtener la variable 'opt_m_x' del estado
            opt_m_x = cs.opt_m_x
            # Obtener la variable 'opt_m_y' del estado
            opt_m_y = cs.opt_m_y
            # Obtener la variable 'opt_qua' del estado
            opt_qua = cs.opt_qua
            # Obtener la variable 'yaw' del estado
            yaw = cs.yaw
            # Obtener la variable 'alt' del estado
            alt = cs.sonarrange
            # Obtener la variable 'batery_voltage' del estado
            battery = cs.battery_voltage

            print(f'{opt_m_x}, {opt_m_y}, {opt_qua}, {yaw}, {alt}, {battery}')
            
            # Escribir los datos en el archivo
            file.write(f'{opt_m_x}, {opt_m_y}, {opt_qua}, {yaw}, {alt}, {battery}\n')
            
            # Esperar un intervalo de tiempo antes de la siguiente lectura (p.ej., 1 segundo)
            time.sleep(0.5)
            i -= 1
            


# Generar el nombre del archivo con la fecha actual
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: Año-Mes-Día_Hora-Minuto-Segundo
file_name = f"ruta_{current_date}.txt"

main(file_name)
