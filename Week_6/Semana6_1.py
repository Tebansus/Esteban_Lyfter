#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define function 1 that calls 2
def print_1():
    print("Test Number 1")
    print_2()
# Define function 2
def print_2():
    print("Test Number 2")
# Define main that calls func 1
def main():
    print_1()
if __name__ == "__main__":
    main()

