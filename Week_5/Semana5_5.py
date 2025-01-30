#!/usr/bin/env python
# coding: utf-8

# In[ ]:


values_by_user = []
# ASk for user values
for i in range(10):
    values_by_user.append(int(input("Digite un numero: ")))
# Find the highest number without using the max function, which was forbidden in the exercise description.
# Instead, compare number by number
highest = values_by_user[0]
for num in values_by_user:
    if num > highest:
        highest = num
print(f"Los numeros fueron: {values_by_user} y el máximo fue {highest}")


# In[ ]:




