"""
Prueba para armar el dron, elevarlo a 1 metro, esperar 10 segundos y descenderlo, para finalmente desarmarlo.
De esta manera se comprueba que el sensor ToF puede ser usado para regular la altitud del dron.
"""

# Armar el dron: 
# Se envían comandos a los canales necesarios para armar.
Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)  
Script.SendRC(4, 2000, True)  
Script.Sleep(3000)  

if not cs.armed:
    print("Error: El dron no se armó correctamente.")
else:
    print("Dron armado. Procediendo a elevar.")

    # Elevar: Se asume que un valor de 1700 en RC3 genera ascenso.
    Script.SendRC(3, 1550, True)
    
    # Esperar hasta alcanzar 1 metro de altitud.
    while cs.sonarrange < 1:
        Script.Sleep(100)
    
    print("Altitud de 1 metro alcanzada.")

    # Esperar 10 segundos en esa posición.
    Script.Sleep(10000)

    # Descender: Se utiliza el valor mínimo en RC3.
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), True)
    while cs.sonarrange > 0.1:
        Script.Sleep(100)
     
    print("Descenso completado.")

    # Desarmar el dron:
    Script.SendRC(4, 1000, True)  # Ajustar yaw (o enviar otro comando) para desarmar
    Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)
    Script.Sleep(3000)

    if not cs.armed:
        print('Motores apagados')
    else:
        print('Fallo al apagar los motores')
