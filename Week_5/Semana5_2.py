#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define the string
string_to_use = 'Pizza con piña'

# iterate on reserse order using range, for this, we start at the last character with len(my_string) - 1, then we move to the first (last in this case) element and the final -1 indicates the stepping, for it to go backwards.
for i in range(len(string_to_use) - 1, -1, -1):
    print(string_to_use[i])

