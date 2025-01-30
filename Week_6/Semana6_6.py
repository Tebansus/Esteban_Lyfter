#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Function to split the words, order them and put them back together with -
def hyphenated_word_order(list_to_order):
    words = list_to_order.split("-")
    sorted_words = sorted(words)
    joined_ordered_words = "-".join(sorted_words)
    return joined_ordered_words
def main():
    # Test string and ordered word printing
    string_to_test = "python-variable-funcion-computadora-monitor"
    result = hyphenated_word_order(string_to_test)
    print(result)
if __name__ == "__main__":
    main()

