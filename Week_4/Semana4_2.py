 # Solicitar datos del usuario
nombre = input("Ingrese su nombre: ")
apellido = input("Ingrese su apellido: ")
edad = int(input("Ingrese su edad: "))

# Clasificar según la edad con ifs
if edad < 2:
    categoria = "bebé"
elif edad < 10:
    categoria = "niño"
elif edad < 12:
    categoria = "preadolescente"
elif edad < 18:
    categoria = "adolescente"
elif edad <= 25:
    categoria = "adulto joven"
elif edad < 65:
    categoria = "adulto"
else:
    categoria = "adulto mayor"
# Mostrar resultado de clasificacion
print(f"{nombre} {apellido}. Basado en su ({edad} años), usted es un {categoria}.")