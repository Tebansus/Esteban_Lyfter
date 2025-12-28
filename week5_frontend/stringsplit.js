const example = "This is a string!"
let word = "";
let separated_words = [];
for (let i = 0; i < example.length; i++) {
    if (example[i] !== " ") {
        word += example[i];
    } else {
        if (word.length > 0) {
            separated_words.push(word);
            word = "";
        }
    }
}
if (word.length > 0) {
    separated_words.push(word);
}
console.log(separated_words);