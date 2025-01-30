#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Function to invert string
def inverting_string(string_to_invert):
    return string_to_invert[::-1]


def main():
    # Call function and print reversed string
    print(inverting_string("Hola mundo"))

if __name__ == "__main__":
    main()

