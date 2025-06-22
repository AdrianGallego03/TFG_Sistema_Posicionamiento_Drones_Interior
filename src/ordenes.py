"""
Programa para mover el dron a través de una ruta predefinida.
Se almacena la ruta realizada para comprobar que la ruta se ha seguido correctamente.
"""

import time
import os
from datetime import datetime

def read_variations(file_path):
    """
    Lee cada línea completa del archivo y la almacena como una lista de valores.
    Se espera que el fichero tenga encabezado y columnas:
    opt_m_x, opt_m_y, opt_qua, yaw, alt, battery_V
    """
    variations = []
    with open(file_path, 'r') as file:
        
        # Omitir encabezado
        next(file)  
        
        for line in file:
        
            values = list(map(float, line.strip().split(',')))
            variations.append(values)
    
    return variations


def move_drone(target_x, target_y, target_qua, target_yaw, target_alt,
               tolerance=0.5, yaw_tolerance=2, alt_tolerance=0.1, max_duration=20000, log_file=None):
    """
    Mueve el dron de forma controlada hasta alcanzar los valores objetivos.
    Al finalizar, se registran en el log los valores finales de los sensores junto
    con un booleano que indica si se alcanzó el punto objetivo (True) o no (False).
    
    Durante el bucle de control se actualizan los comandos RC:
        RC1 (roll) y RC2 (pitch) se usan para corregir posición en X e Y,
        RC4 se usa para corregir el yaw.
    
    
    Args:
        target_x: desplazamiento deseado en el eje X 
        target_y: desplazamiento deseado en el eje Y 
        target_qua: calidad asociada
        target_yaw: orientación objetivo (en grados, de 0 a 360)
        target_alt: altitud objetivo

        tolerance: error permitido en X e Y (unidades del sensor de flujo)
        yaw_tolerance: error permitido en yaw (en grados)
        alt_tolerance: error permitido en altitud (en metros)
        max_duration: tiempo máximo (ms) para completar el movimiento del segmento
      
    Returns:
        objetivo_alcanzado: booleano que indica si se alcanzó el objetivo (True) o no (False)
          
    
    """
    
    #Debug: imprimir destino
    print(f"Moviendo a destino - Var X: {target_x}, Var Y: {target_y}, Yaw: {target_yaw}, Alt: {target_alt}")
    

    # Registrar valores iniciales de los sensores de flujo óptico
    init_flow_x = cs.opt_m_x
    init_flow_y = cs.opt_m_y

    start_time = time.time() * 1000  # Tiempo en milisegundos
    objetivo_alcanzado = False

    # Bucle de control
    while True:
        current_time = time.time() * 1000
        if current_time - start_time > max_duration:
            print("Tiempo máximo superado. Se aborta el segmento.")
            break

        # Calcular la variación acumulada (desplazamientos relativos)
        current_dx = cs.opt_m_x - init_flow_x
        current_dy = cs.opt_m_y - init_flow_y

        error_x = target_x - current_dx
        error_y = target_y - current_dy

        #Control de Altitud
        current_alt = cs.sonarrange  # Obtener la altitud actual
        error_alt = abs(target_alt - current_alt)  # Comparar con la deseada
    
        #Control de YAW 
        current_yaw = cs.yaw  # Se asume que cs.yaw entrega el valor actual en grados
        error_yaw = target_yaw - current_yaw
        # Normalizar error_yaw al intervalo [-180, 180]
        if error_yaw > 180:
            error_yaw -= 360
        elif error_yaw < -180:
            error_yaw += 360

        # Debug: imprimir progreso
        # print(f"Flow - X: {current_dx}, Y: {current_dy} | Error X: {error_x}, Error Y: {error_y} | Yaw Actual: {current_yaw}, Error Yaw: {error_yaw} | Altitud Actual: {current_alt}, Error Altitud: {error_alt}")

        # Verificar si se han alcanzado las tolerancias en posición y yaw
        if abs(error_x) < tolerance and abs(error_y) < tolerance and abs(error_yaw) < yaw_tolerance and abs(error_alt) < alt_tolerance:
            objetivo_alcanzado = True
            print("Posición y yaw objetivo alcanzados.")
        
            # Registrar los datos finales para este segmento
            final_opt_m_x = cs.opt_m_x
            final_opt_m_y = cs.opt_m_y
            final_opt_qua = cs.opt_qua  
            final_yaw = cs.yaw
            final_alt = cs.sonnarrange 
            final_battery = cs.battery_voltage 

            if log_file is not None:
            # Se escribe en el archivo de ruta.
                log_file.write(f"{final_opt_m_x}, {final_opt_m_y}, {final_opt_qua}, {final_yaw}, {final_alt}, {final_battery}, {objetivo_alcanzado}\n")
            
            break

        # Control proporcional para la altitud:
        Kp_alt = 50  # Constante proporcional para la altitud (ajustable según necesidad)
        delta_alt = int(Kp_alt * error_alt)
        cmd_rc3 = 1500 + delta_alt
        
        # Limitar el comando RC3 a un rango seguro 
        cmd_rc3 = max(1300, min(1550, cmd_rc3))
        Script.SendRC(3, cmd_rc3, True)  # Enviar comando a RC3 para controlar la altitud
        
        # Control proporcional para el yaw:
        Kp_yaw = 5  # Constante proporcional para el yaw
        delta_yaw = int(Kp_yaw * error_yaw)
        cmd_rc4 = 1500 + delta_yaw
        # Limitar el comando de yaw a un rango 
        cmd_rc4 = max(1450, min(1550, cmd_rc4))
        Script.SendRC(4, cmd_rc4, True)
        
        
        # Control proporcional para la posición:
        Kp_xy = 50  # Constante proporcional para X e Y
        # Nota: se asigna error_y a RC1 (roll) y error_x a RC2 (pitch) según la convención
        delta_rc1 = int(Kp_xy * error_y)
        delta_rc2 = int(Kp_xy * error_x)
        cmd_rc1 = 1500 + delta_rc1
        cmd_rc2 = 1500 + delta_rc2

        Script.SendRC(1, cmd_rc1, True)  # RC1 – Roll (inclinación lateral)
        Script.SendRC(2, cmd_rc2, True)  # RC2 – Pitch (inclinación frontal)

        # Registrar los datos finales para este segmento
        final_opt_m_x = cs.opt_m_x
        final_opt_m_y = cs.opt_m_y
        final_opt_qua = cs.opt_qua 
        final_yaw = cs.yaw
        final_alt = cs.sonarrange
        final_battery = cs.battery_voltage 

        if log_file is not None:
        # Se escribe en el log: se guardan los valores medidos y el booleano de éxito.
            log_file.write(f"{final_opt_m_x}, {final_opt_m_y}, {target_qua}, {final_yaw}, {final_alt}, {final_battery}, {objetivo_alcanzado}\n")
        Script.Sleep(100)  
        
    # Fin del bucle: detener movimiento
    Script.SendRC(1, 1500, True)
    Script.SendRC(2, 1500, True)
    Script.SendRC(4, 1500, True)

    return objetivo_alcanzado



def main():
    """
    Prueba para mover el dron a través de una ruta predefinida, armándolo, elevándolo, y desarmándolo al final.
    """
    
    # Esperar a que el dron esté conectado
    while cs.mode == "INITIALISING":
        time.sleep(1)
    print("Conexión y modo operativo establecido.")
    
    Script.ChangeMode("AUTO")  
    # Obtener la ruta del directorio actual del script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(current_dir, "..\\Rutas", "prueba subida y movimiento eje y.txt")

    # Leer los datos de la ruta guardada
    route_data = read_variations(ruta_entrada)

    # Crear un nuevo archivo para guardar la nueva ruta con el flag de objetivo alcanzado
    nueva_ruta_dir = os.path.join(current_dir, "..\\Rutas\\Rutas_Recreadas")
    if not os.path.exists(nueva_ruta_dir):
        os.makedirs(nueva_ruta_dir)
        # Generar el nombre del archivo con la fecha actual
    
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: Año-Mes-Día_Hora-Minuto-Segundo
    file_name = f"ruta_{current_date}.txt"
    
    nueva_ruta_file = os.path.join(nueva_ruta_dir, file_name)
    log = open(nueva_ruta_file, "w")
    # Escribir encabezado en el nuevo fichero
    log.write("opt_m_x, opt_m_y, opt_qua, yaw, alt, battery_V, objetivo_alcanzado\n")

    # Armar el dron (por ejemplo, enviando comandos a RC3 y RC4 para el armado)
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)  # Throttle al mínimo
    Script.SendRC(4, 2000, True)  # Comando para armar (según configuración)
    Script.Sleep(2000)
    print("Motores encendidos.")

    # Recorrer cada punto de la ruta leída y ejecutarlo
    for point in route_data:
        target_x, target_y, target_qua, target_yaw, target_alt, battery = point
        # Llamar a move_drone pasando además el log para que se guarden los datos
        move_drone(target_x, target_y, target_qua, target_yaw, target_alt, 
                   tolerance=0.3, yaw_tolerance=100, alt_tolerance=0.2, max_duration=30000, log_file=log)

    # Una vez completada la ejecución de la ruta, estabilizar y desarmar
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), True)  # Throttle al mínimo
    Script.Sleep(2000)
    print("Ruta completada. Procediendo a desarmar.")

    # Comandos de desarme
    estado_actual = cs.mode
    print(f"Estado actual antes de desarmar: {estado_actual}")
    if cs.armed:
        print("Dron armado; desarmando motores...")
        Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)
        Script.SendRC(4, 1000, True)  # Reducir yaw para desarmar
        Script.Sleep(5000)
    else:
        print("Dron no está armado.")
    
    # Apagar motores como medida extra de seguridad
    print("Enviando comandos finales para desarmar motores.")
    Script.SendRC(4, 1000, True)
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)
    Script.Sleep(5000)

    log.close()

main()