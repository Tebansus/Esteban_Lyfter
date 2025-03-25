# Bubblesort algorithm that sorts a list from left to right, by bubbling the largest elements to the right.
def bubble_sort(list):
    for i in range(len(list)-1):
        for j in range(len(list)-1-i):
            # Instead of doing the swap in multiple lines, we can do it in one line with tuple unpacking.
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]


def main():
    my_test_list = [18, -11, 68, 6, 32, 53, -2]
    bubble_sort(my_test_list)

    print(my_test_list)

if __name__ == "__main__":
    main()