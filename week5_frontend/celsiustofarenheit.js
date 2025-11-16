const celsius = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
const farenheit = celsius.map(celsius => (celsius * 9/5) + 32);
console.log(farenheit);