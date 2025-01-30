#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Define function to iterate through the list and save the primes, calling the prime_formula to check
def prime_number(number_list):
    prime_number_list = []
    for number in number_list:
        if prime_formula(number) and number != 1:
            prime_number_list.append(number)
    return prime_number_list
# Prime formula 6n-1 where n has to be a natural whole number, so check if N is. 
def prime_formula(number_to_test):
    if ((number_to_test-1)/6) % 1 == 0 or ((number_to_test+1)/6) % 1 == 0 or number_to_test == 2 or number_to_test == 3:
        return True
    else:
        return False
        
def main():
    # Define tst list and print results
    list_to_cut = [1, 4, 6, 7, 13, 9, 67]
    prime_result = prime_number(list_to_cut)
    print(prime_result)

if __name__ == "__main__":
    main()

