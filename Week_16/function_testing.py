import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sympy import isprime
from Week_6.Semana6_3 import list_sum
from Week_6.Semana6_4 import inverting_string
from Week_6.Semana6_5 import count_cases
from Week_6.Semana6_6 import hyphenated_word_order
from Week_6.Semana6_7 import prime_number

import random
import pytest

#############################################################
##############Test Suite for list_sum function###############
#############################################################
def test_list_sum_interger_with_sum_output():    
    array_test = [random.randint(1, 1000) for i in range(15)]
    assert list_sum(array_test) == sum(array_test)

def test_list_sum_float_with_sum_output():
    array_test = [random.uniform(1, 1000) for i in range(15)]
    assert list_sum(array_test) == sum(array_test)

def test_list_sum_invalid_values():
    with pytest.raises(TypeError):
        list_sum("test")
    with pytest.raises(TypeError):
        list_sum(123)
    with pytest.raises(TypeError):
        list_sum(122.34)

#############################################################
#########Test Suite for inverting_string function############
#############################################################
def test_inverting_string_really_long_string():
    long_string = "test" * 10000  # 10,000 characters long
    assert inverting_string(long_string) == long_string[::-1]
def test_inverting_string_empty_string():
    empty_string = ""
    assert inverting_string(empty_string) == ""
def test_inverting_string_invalid_values():
    with pytest.raises(TypeError):
        inverting_string(123)
    with pytest.raises(TypeError):
        inverting_string(122.34)
#############################################################
#########Test Suite for count_cases function#################
#############################################################
def test_count_cases_small_string():
    small_string = "Testing_String"
    assert count_cases(small_string) == [2, 11]

def test_count_cases_long_string():
    long_string = "L"* 10000 + "s"* 10000 + "T"* 50000 + "t"* 10000
    assert count_cases(long_string) == [60000, 20000]
    
def test_count_cases_not_string():
    with pytest.raises(TypeError):
        count_cases(123)
    with pytest.raises(TypeError):
        count_cases(122.34)
    with pytest.raises(TypeError):
        count_cases(None)
#############################################################
######Test Suite for hyphenated_word_order function##########
#############################################################       
def test_hyphenated_word_order_long_list():
    long_list = ["word" + str(i) for i in range(100000)]
    assert hyphenated_word_order("-".join(long_list)) == "-".join(sorted(long_list))
def test_hyphenated_word_order_empty_string_list():
    empty_list = []
    assert hyphenated_word_order("-".join(empty_list)) == "-".join(sorted(empty_list))
def test_hyphenated_word_order_invalid_values():
    with pytest.raises(AttributeError):
        hyphenated_word_order(123)
    with pytest.raises(AttributeError):
        hyphenated_word_order(122.34)
    with pytest.raises(AttributeError):
        hyphenated_word_order(None)
#############################################################
######Test Suite for prime_number function###################
############################################################# 
def test_prime_number_long_list_large_numers():
    long_list = [random.randint(1, 1000000) for i in range(100000)]
    prime_numbers = prime_number(long_list)
    # Check if the returned numbers are prime. Note: this will fail because the prime_formula in exercise 6_7 is incorrect.
    # The original formula only checks for 6n-1 and 6n+1, 2 and 3, which is not sufficient to determine if a number is prime.  
    for num in prime_numbers:
        assert isprime(num), f"{num} is not a prime number"
def test_prime_invalid_values():
    with pytest.raises(TypeError):
        prime_number("test")
    with pytest.raises(TypeError):
        prime_number(123)
    with pytest.raises(TypeError):
        prime_number(122.34)
def test_prime_small_numbers_small_list():
    small_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    prime_numbers = prime_number(small_list)
    assert prime_numbers == [2, 3, 5, 7]

# main function to run all tests
def main():
    # Exercise 3: list_sum function testing
    test_list_sum_interger_with_sum_output()
    test_list_sum_float_with_sum_output()
    test_list_sum_invalid_values()    
    print("All tests passed for list_sum function.")

    #Exercise 4: inverting_string function testing with pytest
    test_inverting_string_really_long_string()
    test_inverting_string_empty_string()
    test_inverting_string_invalid_values()
    print("All tests passed for inverting_string function.")
    # Exercise 5: count_cases function testing
    test_count_cases_small_string()
    test_count_cases_long_string()
    test_count_cases_not_string()
    print("All tests passed for count_cases function.")
    # Exercise 6: hyphenated_word_order function testing
    test_hyphenated_word_order_long_list()
    test_hyphenated_word_order_empty_string_list()
    test_hyphenated_word_order_invalid_values()
    print("All tests passed for hyphenated_word_order function.")
    # Exercise 7: prime_number function testing
    test_prime_invalid_values()
    test_prime_small_numbers_small_list()
    print("All easy tests passed for prime_number function. The long list test is expected to fail.")    
    test_prime_number_long_list_large_numers()
   
    
    
if __name__ == "__main__":
    main()
