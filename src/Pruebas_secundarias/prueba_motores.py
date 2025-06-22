"""
Prueba para probar el control del dron via comandos RC, armando y desarmando los motores.
"""
# Esperar a que el dron esté conectado verificando el modo
while True:
    modo_actual = cs.mode  # Capturamos el modo actual
    if modo_actual != "INITIALISING":
        break
    Script.Sleep(1000)
print('Conexión y modo operativo establecido')

# Desactivar verificaciones previas al armado (prearm checks)
Script.ChangeParam("ARMING_CHECK", 0)


# Verificar modo antes de STABILIZE
estado_actual = cs.mode
print(f"Estado actual antes de STABILIZE: {estado_actual}")

# Armar los motores directamente
Script.ChangeMode('STABILIZE')  # Cambiar a STABILIZE para armar de forma manual


# Verificar si realmente se está en modo STABILIZE antes de armar
estado_actual = cs.mode
print(f"Estado actual antes de armar: {estado_actual}")


# Asegurarse de que los valores enviados sean enteros (Int16)
Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)  # Throttle al mínimo
Script.SendRC(4, int(2000), True)  # Aumentar yaw para armar motores
Script.Sleep(5000)  # Esperar un poco para asegurarse de que los motores se armen


# Verificar modo despues de armar
estado_actual = cs.mode
print(f"Estado actual despues de armar: {estado_actual}")


# Verificar el estado de armado
if cs.armed:
    print('Motores armados')
else:
    print('Fallo al armar los motores')

# Mantener el estado armado por un tiempo para probar
Script.Sleep(5000)

# Asegurarse de estar en modo STABILIZE antes de desarmar
print('Cambiando a modo STABILIZE para desarmar')
Script.ChangeMode('STABILIZE')
Script.Sleep(2000)  # Esperar un poco para asegurarse de que el modo ha cambiado

# Verificar si realmente se está en modo STABILIZE antes de desarmar
estado_actual = cs.mode
print(f"Estado actual antes de desarmar: {estado_actual}")

# Verificar el estado de armado antes de desarmar
if cs.armed:
    print('Dron está armado, procediendo a desarmar')
else:
    print('Dron no está armado, no es necesario desarmar')

# Apagar los motores (desarmar)
print('Enviando comandos para desarmar motores')
Script.SendRC(4, int(1000), True)  # Reducir yaw para desarmar motores
Script.SendRC(3, int(Script.GetParam("RC3_MIN")), False)  # Throttle al mínimo
Script.Sleep(10000)  # Esperar un poco para asegurarse de que los motores se desarmen

# Verificar el estado de desarme
if not cs.armed:
    print('Motores apagados')
else:
    print('Fallo al apagar los motores')

print('Control de motores completado')
