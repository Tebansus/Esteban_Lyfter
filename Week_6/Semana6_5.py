#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Function to use .isupper and .islower to determine cases
def count_cases(string_to_count): 
    result = [0,0]
    for char in string_to_count:
        if char.isupper():
            result[0] += 1
        elif char.islower():
            result[1] += 1
    return result

def main():
    # Define the string and pass it to the counting function 
    test_string = "I love Nación Sushi"
    counts = count_cases(test_string)
    print(f"There’s {counts[0]} upper cases and {counts[1]} lower cases")

if __name__ == "__main__":
    main()

