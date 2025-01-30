#!/usr/bin/env python
# coding: utf-8

# In[1]:


testglobalvar = 5

def testfunc():
    test_func_var = 7


def main():
    # The global var is printed, as expected
    print(testglobalvar)
    # The function var isn't printed because main function has no access to it
    print(test_func_var)

if __name__ == "__main__":
    main()

