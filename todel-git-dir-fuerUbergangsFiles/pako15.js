const fs = require('fs');
const pako = require('pako');
const { JSDOM } = require('jsdom');
//const { saveAs } = require('FileSaver');
const json3 = require('json3');

const html = fs.readFileSync('/home/alex/middle.html', 'utf8');

const dom = new JSDOM(html);
const document = dom.window.document;

const tableElement = document.getElementsByTagName('table')[0];
const tableData1 = [];

const trElements = tableElement.getElementsByTagName('tr');
for (let i = 0; i < trElements.length; i++) {
  const trElement = trElements[i];
  const rowData = [];

  const tdElements = trElement.getElementsByTagName('td');

  for (let j = 0; j < tdElements.length; j++) {
    const tdElement = tdElements[j];

    //const cellValue = Uint8Array.from(tdElement.textContent, c => c.charCodeAt(0));
    const cellValue = tdElement.textContent
    rowData.push(cellValue);
  }

  tableData1.push(rowData);
}

console.log(tableData1);

const compressedCells = [];

function transpose(matrix) {
  const transposed = [];
  for (let j = 0; j < matrix[0].length; j++) {
    const newRow = [];
    for (let i = 0; i < matrix.length; i++) {
      newRow.push(matrix[i][j]);
    }
    transposed.push(newRow);
  }
  return transposed;
}

tableData = transpose(tableData1);

for (let row = 0; row < tableData.length; row++) {
  //for (let col = 0; col < tableData[row].length; col++) {
/*    const uintArray = tableData[row].map(str => {
      const buffer = new Uint8Array(str.length);
     console.log(str);
      for (let i = 0; i < str.length; i++) {
        buffer[i] = str.charCodeAt(i);
      }
      return buffer;
    });*/
    const cellsValues1 = json3.stringify(tableData[row])
    /*if (row == 101) {
        console.log(tableData[row]);
        console.log("aaa");
        console.log(cellsValues1);
    }*/
    //const cellsValues = Uint8Array.from(cellsValues1, c => c.charCodeAt(0));
    const cellsValues = new TextEncoder().encode(cellsValues1);
    compressedCells.push(pako.deflate(cellsValues));
  //}
}

const numRows = tableData.length;
const numCols = tableData[0].length;
const rowIndex = 9;
const colIndex = 9;
const compressedCellIndex = (rowIndex * numCols) + colIndex;
//const decompressedCellData = pako.inflate-zlib(compressedCells[compressedCellIndex], { to: 'string' });
//const decompressedCellValue = decompressedCellData[0];

//console.log(decompressedCellValue);
//console.log((pako.inflate(compressedCells[10])));
console.log(json3.parse(pako.inflate(compressedCells[100], { to: 'string' }))[5]);
console.log((pako.inflate(compressedCells[101], { to: 'string' })))
//console.log(json3.parse(pako.inflate(compressedCells[210], { to: 'string' }))[8]);
//console.log(JSON.parse(pako.inflate(compressedCells[333], { to: 'string' })));
/*console.log(pako.inflate-zlib(compressedCells[1000], { to: 'string' }));
console.log(pako.inflate-zlib(compressedCells[5000], { to: 'string' }));
console.log(pako.inflate-zlib(compressedCells[20000], { to: 'string' }));*/
/*const base64Data = Buffer.from(compressedCells).toString('base64');
console.log(base64Data);
const jsonData = JSON.stringify({ data: base64Data });
fs.writeFileSync('data.json', jsonData);*/
// Zum Speichern der Datei kann man z.B. das FileSaver.js library verwenden
// Hier ein Beispiel:
//const blob = new Blob([jsonData], {type: "application/json"});
//saveAs(blob, "compressedCells.json");
const compressedCells2 = [];

// ...

for (let row = 0; row < compressedCells.length; row++) {
    //const compressedCell = pako.deflate-zlib(tableData[row][col]);
    const base64Data = Buffer.from(compressedCells[row]).toString('base64');
    compressedCells2.push(base64Data);
}

// ...

const dataToSave = {
  compressedCells: compressedCells2
};

fs.writeFileSync('data.json', JSON.stringify(dataToSave));
console.log("Tabellen-Breite:");
console.log(compressedCells.length.toString());
