"""
Prueba para comprobar los valores mínimos y máximos de los canales RC.
Además se comprueba los que los valores de cs se actualizan y que se capturan correctamente.
"""
print("valor rc1", Script.GetParam("RC1_MIN"),Script.GetParam("RC1_MAX") )
print("valor rc2", Script.GetParam("RC2_MIN"),Script.GetParam("RC2_MAX") )
print("valor rc3", Script.GetParam("RC3_MIN"),Script.GetParam("RC3_MAX"))
print("valor rc4", Script.GetParam("RC4_MIN"),Script.GetParam("RC4_MAX") )
i = 30
while i > 0:
    
    print("Valores del cs", cs.opt_m_x, cs.opt_m_y, cs.opt_qua, cs.yaw, cs.sonarrange, cs.battery_voltage)
    Script.Sleep(1000)
    i -= 1
