import pytest
import random

 
# Test with a small list of random numbers
def test_bubble_sort_small_sorted_list_output():
    array_to_sort = [random.randint(1, 1000) for i in range(15)]
    assert bubble_sort(array_to_sort) == sorted(array_to_sort)

# Test with a large list of random numbers
def test_bubble_sort_big_sorted_list_output():
    array_to_sort = [random.randint(1, 1000) for i in range(1000)]
    assert bubble_sort(array_to_sort) == sorted(array_to_sort)
# test with empty list
def test_bubble_sort_empty_sorted_list_output():
    array_to_sort = []
    assert bubble_sort(array_to_sort) == []
# Test with a list containing non-list elements to see if it raises a TypeError
def test_bubble_sort_non_list_element_sorted_list_output():
    with pytest.raises(TypeError):
        bubble_sort("test")
    with pytest.raises(TypeError):
        bubble_sort(123)
    with pytest.raises(TypeError):
        bubble_sort(122.34)
#Bubble sort function from other exercise
def bubble_sort(arr):
    
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
# Main function to run the tests
def main():

    test_bubble_sort_small_sorted_list_output()
    test_bubble_sort_big_sorted_list_output()
    test_bubble_sort_empty_sorted_list_output()
    test_bubble_sort_non_list_element_sorted_list_output()
    print("All tests passed!")
 

if __name__ == "__main__":
    main()