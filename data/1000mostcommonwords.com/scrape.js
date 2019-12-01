
let table = document.getElementsByTagName("table")[0];
let rows = table.rows;
let results = [];

for (let i = 0; i < table.rows.length; i++) {
    if (i === 0) continue;

    let row = table.rows[i];
    let [number, translation, english] = row.cells;
    let result = `${number.innerText},${translation.innerText},${english.innerText}`;
    results.splice(0, 0, result);
}

results.forEach(result => console.log(result));
