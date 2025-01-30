#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Example lists
list_a = ['first_name', 'last_name', 'role']
list_b = ['Alek', 'Castillo', 'Software Engineer']
dict_to_use = {}
# Iterate through both lists and assign the key pair values
for i in range(len(list_a)):
    dict_to_use[list_a[i]] = list_b[i]
# Print example
print(dict_to_use)

