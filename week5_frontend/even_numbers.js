const test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20];
let even_numbers_list = [];
let even_numbers_list_2 = [];
function even_numbers_for() {
    for (let i =0; i < test_list.length; i++) {
        if (test_list[i] % 2 === 0) {
            even_numbers_list.push(test_list[i]);
        }
    }
    return even_numbers_list;
}

console.log(even_numbers_for());

function even_numbers_filter() {
    even_numbers_list_2 = test_list.filter(number => number % 2 === 0);
    return even_numbers_list_2;
}

console.log(even_numbers_filter());