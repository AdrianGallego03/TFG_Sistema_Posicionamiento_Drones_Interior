"""
Script para comparar los datos de altura del sensor barométrico y el sensor ToF del dron.
"""
from datetime import datetime
import os 
import time

# Generar el nombre del archivo con la fecha actual
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: Año-Mes-Día_Hora-Minuto-Segundo
filename_ALT = f"ruta_{current_date}_ALT.txt"
filename_SONAR = f"ruta_{current_date}_SONAR.txt"

# Obtener la ruta del directorio actual del script 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo 

file_path_ALT = os.path.join(current_dir, "..\\Rutas",filename_ALT) 
file_path_SONAR = os.path.join(current_dir, "..\\Rutas",filename_SONAR)

#while True:
#        armed = cs.armed  # Capturamos el modo actual
#        if armed == True:
#            break
#        print("El dron no esta armado")
#        Script.Sleep(1000)

with open(file_path_ALT, 'w') as file, open(file_path_SONAR, 'w') as file_sonar:

    #Almacenar los datos del barometro en en archivo ALT y los datos del sensor ToF en el archivo SONAR
    file.write('opt_m_x, opt_m_y, opt_qua, yaw, alt\n') 
    file_sonar.write('opt_m_x, opt_m_y, opt_qua, yaw, sonarrange\n')
    
    # Si se quiere realizar una ruta competa con el dron volando, descomentar la siguiente línea:
    #while cs.armed:
    
    # Y comentar las dos siguientes líneas:
    i = 30 # Número de lecturas a realizar (30 segundos de datos)
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
        alt = cs.alt
        #Obtener la variable 'sonarrange' del estado
        sonarrange = cs.sonarrange

        # Debug
        print(f' ALT: {alt}, SONAR: {sonarrange}')
        
        # Escribir los datos en el archivo
        file.write(f'{opt_m_x}, {opt_m_y}, {opt_qua}, {yaw}, {alt}\n')
        file_sonar.write(f'{opt_m_x}, {opt_m_y}, {opt_qua}, {yaw}, {sonarrange}\n')
        
        # Esperar un segundo para tomar la siguiente lectura
        time.sleep(1)
        i -= 1
