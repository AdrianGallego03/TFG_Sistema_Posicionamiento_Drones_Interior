"""
Prueba para comprobar el paso de argumentos al script y la entrada del usuario en Mission Planner.
Como se puede comprobar, no se permite pasar argumentos al script ni se permite la entrada de datos por terminal.
"""

def main(file_name):
    print(file_name)
    a = input("Introduzca un número: ")
    print(f"El número introducido es: {a}")
    
if __name__ == "__main__":
    
    print("inicio script")
    if len(sys.argv) != 2:
        print("Debe introducir en nombre del archivo para guardar la ruta del dron.")
        
    file_name = sys.argv[1]
    main(file_name)
else:
    print("No main")
    