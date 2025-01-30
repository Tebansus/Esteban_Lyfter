#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define the list
test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Add only the even values
even_list = [x for x in test_list if x%2 == 0]
print(even_list)

