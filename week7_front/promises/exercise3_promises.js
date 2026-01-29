words = ["very", "dogs", "cute", "are"];
const promises = [
    new Promise(resolve => setTimeout(() => resolve(words[1]), 1000)),
    new Promise(resolve => setTimeout(() => resolve(words[3]), 2000)),
    new Promise(resolve => setTimeout(() => resolve(words[0]), 3000)),
    new Promise(resolve => setTimeout(() => resolve(words[2]), 4000))
];
Promise.all(promises)
    .then(results => {
        const sentence = results.join(" ") + ".";
        console.log(sentence); // Output: "dogs are very cute."
    })
    .catch(error => {
        console.error(error);
    });
