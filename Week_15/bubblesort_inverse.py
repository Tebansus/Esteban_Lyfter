# Inverse bubble sort algorithm that sorts a list from right to left, by bubbling the smallest elements to the left.
def bubble_sort(list):
    for i in range(len(list)-1):
        # the main change is here, we start from the right and go to the left by adjusting the parameters in the range function.
        for j in range(len(list)-1, i, -1):
            # Also change the comparison operator to < and the swap to swap left instead of right.
            if list[j] < list[j-1]:
                list[j], list[j-1] = list[j-1], list[j]


def main():
    my_test_list = [18, -11, 68, 6, 32, 53, -2]
    bubble_sort(my_test_list)

    print(my_test_list)

if __name__ == "__main__":
    main()