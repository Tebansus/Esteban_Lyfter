const fs = require('fs');
results = {};
let filesRead = 0;
const totalFiles = 2;
function checkAndLog () {
    filesRead++;
    if (filesRead === totalFiles) {
        const words = new Set(results['file1.txt'].split(/\s+/));
        const words2 = results['file2.txt'].split(/\s+/);
        const common = words2.filter(word => words.has(word) && word !== '');
        console.log("Common words:", [...new Set(common)]);
    }


}

fs.readFile('file1.txt', 'utf8', (err, data) => {    
    results['file1.txt'] = data;
    checkAndLog();
});
fs.readFile('file2.txt', 'utf8', (err, data) => {
    results['file2.txt'] = data;
    checkAndLog();
});

