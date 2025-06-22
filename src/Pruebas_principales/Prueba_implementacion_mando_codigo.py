
"""
Prueba para comprobar que el dron puede recibir ordenes de armado del mando y mensajes de radio contro via comandos.      
"""
    
def comprobar_armado(segundos=15):
    """Función para comprobar si el dron está armado y mostrar el estado cada segundo durante 15 segundos.
    Args:
        segundos (int): Número de segundos durante los cuales se comprobará el estado del dron. Por defecto es 15.
    Returns:
        None
    """
    
    i = 0
    while i < segundos:
        if cs.armed:
            print('El dron esta armado')
        else:
            print('El dron no esta armado')
        Script.Sleep(1000)
        i += 1

# comprobar el modo de vuelo del dron
estado_actual = cs.mode
print(f"Estado actual: {estado_actual}")
Script.Sleep(3000)

# Cambiar el modo de vuelo del dron a POST_HOLD 
print('Cambiando a modo PH')
Script.ChangeMode('POST_HOLD')
Script.Sleep(1000)

# Comprobar si el dron ha cambiado de estado
estado_actual = cs.mode
print(f"Estado actual: {estado_actual}")

# Comprobar si el dron está armado 
comprobar_armado()

# Si el dron esta armado, enviar mensajes RC de prueba para comprobar al conexion mando/script dron
if cs.armed:
    
    # Acelerar motores
    Script.SendRC(3, int(1550), True)  
    Script.Sleep(3000) 
    Script.SendRC(3, int(1500), True)
    Script.Sleep(3000)
    Script.SendRC(3, int(1450), True)
    Script.Sleep(3000)
    
    
    # Desarmar motores
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)  
    Script.SendRC(4, int(1000), True)  
    Script.Sleep(5000)  
    
    if not cs.armed:
        print('Motores apagados')
    else:
        print('Fallo al apagar los motores')
    