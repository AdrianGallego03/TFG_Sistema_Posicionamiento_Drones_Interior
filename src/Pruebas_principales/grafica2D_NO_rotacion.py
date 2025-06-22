"""
Programa para graficar la trayectoria de un dron en 2D sin aplicar rotación.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import os

def main(file_name):
    """
    Función principal que grafica la trayectoria del dron en 2D sin aplicar rotación.
    Args:
        file_name: Nombre del archivo que contiene los datos de la trayectoria del dron.
    """
    
    # Obtener la ruta del archivo de datos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..\\..\\Rutas", file_name) 
    
    # Comprobar cabecera del archivo
    with open(file_path, "r") as f:
        header = f.readline().strip().split(",")
    if len(header) < 3:
        print("Error: El archivo debe tener al menos 3 columnas.")
        sys.exit(1)
    columnas_requeridas = ["opt_m_x", "opt_m_y", "opt_qua"]
    for i, col in enumerate(columnas_requeridas):
        if header[i].strip() != col:
            print(f"Error: Fallo en el tipo de columnas.")
            sys.exit(1)
            
    # Leer el archivo de datos
    datos = np.genfromtxt(file_path, delimiter=',', skip_header=1)

    # Inicializar las listas para almacenar las coordenadas y los colores
    x_coords = [0]
    y_coords = [0]
    colors = ['red']  # Inicializar con un color para el punto de inicio

    # Normalizar la calidad para que esté entre 0 y 1
    max_quality = max(datos[:, 2])
    min_quality = min(datos[:, 2])
    norm_quality = (datos[:, 2] - min_quality) / (max_quality - min_quality)

    # Recorrer las filas del archivo de datos
    for i in range(len(datos)):
        opt_m_x = -datos[i, 0]
        opt_m_y = datos[i, 1]
        qua = norm_quality[i]  # Usar la calidad normalizada
        
        # Calcular las nuevas coordenadas sumando los deltas calculados a las coordenadas anteriores
        x_coords.append(x_coords[-1] + opt_m_x)
        y_coords.append(y_coords[-1] + opt_m_y)

        # Asignar color basado en la calidad normalizada utilizando un mapa de colores
        colors.append(cm.coolwarm(1.0-qua))

    # Crear la figura 2D
    fig, ax = plt.subplots()

    # Plotear las coordenadas con colores
    sc = ax.scatter(x_coords, y_coords, c=colors, marker='o')

    # Etiquetar los puntos con su índice
    for i in range(len(x_coords)):
        if i == 0 or i == len(x_coords)-1:
            ax.text(x_coords[i], y_coords[i], str(i), fontsize=12, ha='center', va='bottom')

    # Añadir flechas para mostrar la dirección del recorrido
    for i in range(len(x_coords) - 1):
        ax.annotate('', xy=(x_coords[i + 1], y_coords[i + 1]), xytext=(x_coords[i], y_coords[i]),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))

    # Configurar el punto (0,0) en el centro de la gráfica
    ax.set_xlim([min(x_coords)-1, max(x_coords)+1])
    ax.set_ylim([min(y_coords)-1, max(y_coords)+1])

    # Etiquetas y título
    ax.set_xlabel('opt_m_x (m)')
    ax.set_ylabel('opt_m_y (m)')
    plt.title('Trayectoria del dron en 2D sin rotacion aplicada')

    # Mostrar la gráfica
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Debe introducir el nombre del archivo de ruta.")
        sys.exit(1)
    file_name = sys.argv[1]
    main(file_name)
