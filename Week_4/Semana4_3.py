import random
# Generar numero aleatorio de 1 al 10
random_number = random.randint(1, 10)

#Bucle que solo termina si el usuario acierta. 
while True:
    guess = input("Digite un numero del 1 al 10. ")
    # Comparar el numero, si no es igual, sigue preguntando.
    if int(guess) == random_number:
        print(f"Felicidades, el numero {guess} sí es el correcto, gracias por participar.")
        break
    else:
        print("Numero incorrecto, intentelo otra vez. ")