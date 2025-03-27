#############################################################
#################First Analysis##############################
#############################################################


#For bubble sort, the best case scenario is when the list is already sorted. In this case, the complexity is O(n).
# However, the worst case scenario is when the list is sorted in reverse order. In this case, the complexity is O(n^2).
# Because Big O notation is used to describe the worst case scenario, the complexity of bubble sort is O(n^2).
def bubble_sort(list):
    for i in range(len(list)-1):
        for j in range(len(list)-1-i):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]

#############################################################
#################Second Analysis#############################
#############################################################

#The complexity of the function is O(n) because the function iterates through the list once to calculate the sum of the elements.
# Even in the worst case scenario, the complexity of the function remains O(n) because it still iterates through the list once.
def print_numbers_times_2(numbers_list):
	for number in numbers_list:
		print(number * 2)

#############################################################
#################Third Analysis##############################
#############################################################


# The complexity of the function is O(n^2) because it contains a nested loop.
# The outer loop iterates through the list once, and the inner loop iterates through the list again for each element in the outer loop.
def check_if_lists_have_an_equal(list_a, list_b):
	for element_a in list_a:
		for element_b in list_b:
			if element_a == element_b:
				return True
				
	return False

#############################################################
#################Fourth Analysis#############################
#############################################################


# For the function to find the maximum element in a list, the complexity is O(10) because it iterates through the list once, but a maximum of 10 times.
# In the best case scenario, the complexity is O(1) because the function returns immediately if the list is empty.
# Normally however, if N <10, the complexity is O(N), but if N > 10, the complexity is O(10), which would best be described as O(min(N, 10)).
# So, in the worst scenario, the complexity is O(10), because it can be O(1), O(2), O(3)...up until O(10), which is the worst case scenario.
def print_10_or_less_elements(list_to_print):
	list_len = len(list_to_print)
	for index in range(min(list_len, 10)):
		print(list_to_print[index])

#############################################################
#################Fifth Analysis##############################
#############################################################


# The complexity of the function is O(n^3) because it contains three nested for loops. In the best case scenario, the complexity is O(1) because the function returns immediately if the list is empty.
# However, in the worst case scenario, the complexity is O(n^3) because the function iterates through the list three times. 
# So, because Big O notation is used to describe the worst case scenario, the complexity of the function is O(n^3).
# However, this assumes all lists are roughly the same size or similar enough when talking about sizes apporaching mathematical limits of infinity. If the lists are of different sizes and not approaching infinity, the complexity is better described as O(n*m*p) where n, m, and p are the sizes of the three lists.
def generate_list_trios(list_a, list_b, list_c):
	result_list = []
	for element_a in list_a:
		for element_b in list_b:
			for element_c in list_c:
				result_list.append(f'{element_a} {element_b} {element_c}')
				
	return result_list