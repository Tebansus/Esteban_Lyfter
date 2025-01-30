#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define function for sum
def list_sum(list_1):
    return sum(list_1)

# Main function where list is defined and passed to sum function
def main():
    list_main = [4, 6, 2, 29]
    sum_of_list = list_sum(list_main)
    print(sum_of_list)
if __name__ == "__main__":
    main()

