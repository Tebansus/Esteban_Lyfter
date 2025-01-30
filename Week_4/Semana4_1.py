# String + String
print("hola" + " mundo")
# Resultado: String concatenado "hola mundo"

# String + int
print("hola" + 8)
# Resultado: TypeError: can only concatenate str (not "int") to str

# int + string
print(8 + "hola")
# Resultado: TypeError: unsupported operand type(s) for +: 'int' and 'str'


# list + list
print([1, 2, 3] + [1, 2, 3])
# Resultado: Lista concatenada [1, 2, 3, 1, 2, 3]

# String + list
print("hola" + [1, 2, 3])
# Resultado: TypeError: can only concatenate str (not "list") to str

# float + int
print(7.23 + 2)
# Resultado: Suma de ambos valores 9.23

# bool + bool

print(True + False)  # Resultado: 1 ya que es 1 + 0 en operacion aritmentica
print(True + True)   # Resultado: 2 ya que es 1 + 1 en operacion aritmentica
print(False + False) # Resultado: 0 ya que es 0 + 0 en operacion aritmentica