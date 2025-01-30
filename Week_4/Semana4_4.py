# Solicita numeros
numeros = input("Digite 3 números separados por coma: ")
# Les quita la coma y los guarda en una lista
lista_numeros = [int(numero.strip()) for numero in numeros.split(",")]
# Determina el maximo de la lista
numero_maximo = max(lista_numeros)
# Imprime el maximo.
print(f"El numero mayor es {numero_maximo}")