"""
Script para graficar la trayectoria de un dron en 3D a partir de un archivo de datos.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.cm as cm

# Nombres de columnas válidos (en orden)
COLUMNAS_VALIDAS = [
    "opt_m_x", "opt_m_y", "opt_qua", "yaw", "alt", "battery_V", "objetivo_alcanzado"
]

def main(file_name):
    """
    Función principal que grafica la trayectoria del dron en 3D a partir de un archivo de datos.
    Args:
        file_name: Nombre del archivo que contiene los datos de la trayectoria del dron.
    """
    
    # Obtener la ruta del directorio actual del script 
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ruta completa al archivo 
    file_path = os.path.join(current_dir, "..\\Rutas", file_name) 

    # Leer la cabecera y comprobar columnas
    with open(file_path, "r") as f:
        header = f.readline().strip().split(",")
        
    if not (5 <= len(header) <= 7):
        print(f"Error: El archivo debe tener entre 5 y 7 columnas, tiene {len(header)}.")
        # print(f"Cabecera encontrada: {header}")
        sys.exit(1)
        
    for i, col in enumerate(header):
        if col.strip() != COLUMNAS_VALIDAS[i]:
            print(f"Error: Tipo de columnas incorrectas.")
            sys.exit(1)
        
    # Leer el archivo de datos
    datos = np.genfromtxt(file_path, delimiter=',', skip_header=1)

    # Si solo hay una fila, genfromtxt devuelve un vector 1D;
    # Convertir en una matriz 2D de 1xN para que datos[:,2] funcione.
    if datos.ndim == 1:
        datos = datos.reshape(1, -1)
    
    #Si hay columna de objetivo_alcanzado, guardar los datos
    has_obj = (datos.shape[1] == 7)
    if has_obj:
        obj_flags = datos[:, 6].astype(int)

    # Inicializar las listas para almacenar las coordenadas y los colores
    x_coords = [0]
    y_coords = [0]
    z_coords = [0]
    colors = ['red']  # Inicializar con un color para el punto de inicio

    # Normalizar la calidad para que esté entre 0 y 1
    max_quality = max(datos[:, 2])
    min_quality = min(datos[:, 2])
    norm_quality = (datos[:, 2] - min_quality) / (max_quality - min_quality)

    # Ángulo de rotación inicial (asumiendo que es 0)
    previous_yaw_raw = None
    acum_yaw = 0  # Acumulador para el yaw global
    
    # Recorrer las filas del archivo de datos
    for i in range(len(datos)):
        opt_m_x = -datos[i, 0]
        opt_m_y = datos[i, 1]
        qua = norm_quality[i]  # Usar la calidad normalizada
        yaw = datos[i, 3]
        alt = datos[i, 4]
        
        # Convertir yaw a radianes
        current_yaw_raw = math.radians(yaw)
        
        if previous_yaw_raw is None:
        # Para la primera iteración, el ángulo acumulado es el mismo que el raw
            acum_yaw = current_yaw_raw
        else:
            # Calcular la diferencia entre el yaw actual y el anterior
            diff = current_yaw_raw - previous_yaw_raw
            
            # Ajustar la diferencia para que esté en el rango [-pi, pi]
            if diff > math.pi:
                diff -= 2 * math.pi
            elif diff < -math.pi:
                diff += 2 * math.pi
            
            # Acumular la diferencia al yaw global
            acum_yaw += diff

        # Actualizamos el yaw raw previo para la siguiente iteración
        previous_yaw_raw = current_yaw_raw
        
        # Calcular las componentes x e y teniendo en cuenta la rotación del dron
        delta_x = opt_m_x * math.cos(acum_yaw) - opt_m_y * math.sin(acum_yaw)
        delta_y = opt_m_x * math.sin(acum_yaw) + opt_m_y * math.cos(acum_yaw)

        # Calcular las nuevas coordenadas sumando los deltas calculados a las coordenadas anteriores
        x_coords.append(x_coords[-1] + delta_x)
        y_coords.append(y_coords[-1] + delta_y)
        z_coords.append(alt)

        # Elegir color: verde si el objetivo se alcanzó, si no usar coolwarm
        if has_obj and obj_flags[i] == 1:
            colors.append('green')
        else:
            colors.append(cm.coolwarm(1.0 - norm_quality[i]))


    # Crear la figura y el eje 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotear las coordenadas con colores
    ax.scatter(x_coords, y_coords, z_coords, c=colors, marker='o')

    # Etiquetar los puntos con su índice
    for i in range(len(x_coords)):
        if i == 0 or i == len(x_coords)-1:
            ax.text(x_coords[i], y_coords[i], z_coords[i], str(i), fontsize=12, ha='center', va='bottom')

    # Añadir flechas para mostrar la dirección del recorrido
    for i in range(len(x_coords) - 1):
        ax.quiver(x_coords[i], y_coords[i], z_coords[i], 
                  x_coords[i + 1] - x_coords[i], y_coords[i + 1] - y_coords[i], z_coords[i + 1] - z_coords[i], 
                  arrow_length_ratio=0.1)

    # Calcular el rango máximo entre x, y y z
    x_range = max(x_coords) - min(x_coords)
    y_range = max(y_coords) - min(y_coords)
    z_range = max(z_coords) - min(z_coords)
    max_range = max(x_range, y_range, z_range)

    # Redondear hacia arriba al siguiente entero
    max_range_ceiled = math.ceil(max_range)

    # Ajustar los límites de los ejes para que todos tengan el mismo rango
    ax.set_xlim([-max_range_ceiled, max_range_ceiled])
    ax.set_ylim([-max_range_ceiled, max_range_ceiled])
    ax.set_zlim([-max_range_ceiled, max_range_ceiled])

    # Etiquetas y título
    ax.set_xlabel('opt_m_x (m)')
    ax.set_ylabel('opt_m_y (m)')
    ax.set_zlabel('alt (m)')
    plt.title('Trayectoria del dron en 3D')

    # Si existe columna de batería
    # Nueva gráfica: Voltaje vs Tiempo
    if datos.shape[1] > 5: 
        fig2, ax2 = plt.subplots()
         
        battery = datos[:, 5]
        tiempo = np.arange(len(battery))
        ax2.plot(tiempo, battery, marker='o', color='green')
        ax2.set_xlabel('Tiempo (s)')
        ax2.set_ylabel('Voltaje (mV)')
        ax2.set_title('Voltaje vs Tiempo')
    else:
        print("No se encontró columna de batería en los datos.")

    # Mostrar la gráfica
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Debe introducir el nombre del archivo de ruta.")
        sys.exit(1)
    file_name = sys.argv[1]
    main(file_name)
