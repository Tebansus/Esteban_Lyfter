# Solicitar N cantidad de  Notas
cantidad_de_notas = int(input("Digite el número de notas que va a ingresar: "))
# Listas donde guardar los resultados y contador para promedio  total
notas_aprobadas = []
notas_desaprobadas = []
notas_totales = 0
# Ejecutar la cantidad de veces definida por N
for i in range(cantidad_de_notas):
    # Pedir la nota
    nota_temporal = int(input("Digite la nota: "))
    # Asignar a la lista correspondiente
    if nota_temporal >= 70:
        notas_aprobadas.append(nota_temporal)
    else:
        notas_desaprobadas.append(nota_temporal)
    # Suma de todas las notas para el promedio
    notas_totales = notas_totales + nota_temporal
# Imprimir estadisticas. 
print(f"El promedio de notas totales fue de: {notas_totales/cantidad_de_notas}")
print(f"La cantidad de notas aprobadas fue: {len(notas_aprobadas)}")
print(f"La cantidad de notas desaprobadas fue: {len(notas_desaprobadas)}")
print(f"El promedio de las aprobadas fue:  {sum(notas_aprobadas)/len(notas_aprobadas)}")
print(f"El promedio de las desaprobadas fue:  {sum(notas_desaprobadas)/len(notas_desaprobadas)}")