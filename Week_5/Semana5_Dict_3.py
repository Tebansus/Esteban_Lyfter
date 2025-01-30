#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define Keys
list_of_keys = ['access_level', 'age']

# define dictionary
employee = {'name': 'John', 'email': 'john@ecorp.com', 'access_level': 5, 'age': 28}

# Define the process for 
for key in list_of_keys:
    employee.pop(key, None)  # Elimina la clave si existe, ignora si no
# Mostrar el resultado
print(employee)

