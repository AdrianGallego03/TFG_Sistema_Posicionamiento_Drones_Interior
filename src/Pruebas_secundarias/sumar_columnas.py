"""
Codigo para comprobar la distancia recorrida en cada eje durante una ruta.
"""
import csv
import sys
import math

def sumar_desplazamiento_rotado(nombre_archivo):
    """
    Suma los desplazamientos en los ejes X e Y de un archivo, teniendo en cuenta la rotación del dron.
    Args:
        nombre_archivo (str): Ruta al archivo con los datos del dron.

    """
    suma_delta_x = 0.0
    suma_delta_y = 0.0

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=',')
        # Saltamos la cabecera
        cabecera = next(lector)
        
        for fila in lector:
            yaw_inicial = 0.0  # Inicializar yaw para la primera fila
            if not fila:
                continue  # Saltar filas vacías
            try:
                # Convertir los valores necesarios a float:
                opt_m_x = float(fila[0].strip())
                opt_m_y = float(fila[1].strip())
                # Se ignora 'opt_qua' que está en fila[2]
                # El ángulo 'yaw' se encuentra en la cuarta columna (fila[3])
                yaw = float(fila[3].strip())
                
                yaw = math.radians(yaw)  # Convertir a radianes
                yaw_diff = yaw - yaw_inicial  # Calcular la diferencia respecto al yaw inicial
                yaw_inicial = yaw  # Actualizar yaw inicial para la siguiente iteración
            except ValueError:
                print("Error al procesar la fila:", fila)
                continue
            
            # Calcular las componentes x e y teniendo en cuenta la rotación del dron:
            delta_x = opt_m_x * math.cos(yaw_diff) - opt_m_y * math.sin(yaw_diff)
            delta_y = opt_m_x * math.sin(yaw_diff) + opt_m_y * math.cos(yaw_diff)
            
            suma_delta_x += delta_x
            suma_delta_y += delta_y

    print("Suma de delta_x:", suma_delta_x)
    print("Suma de delta_y:", suma_delta_y)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python sumar_desplazamiento_rotado.py <archivo.txt>")
        sys.exit(1)

    nombre_archivo = sys.argv[1]
    sumar_desplazamiento_rotado(nombre_archivo)