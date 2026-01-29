function callback1() {
    console.log("The number is even.");
}
function callback2() {
    console.log("The number is odd.");
}
function checkNumber(num, evenCallback, oddCallback) {
    if (num % 2 === 0) {
        evenCallback();
    } else {
        oddCallback();
    }

}
checkNumber(4, callback1, callback2); // Output: The number is even.
checkNumber(7, callback1, callback2); // Output: The number is odd.