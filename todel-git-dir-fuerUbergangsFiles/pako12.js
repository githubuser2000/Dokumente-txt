const fs = require('fs');
const pako = require('pako');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('/home/alex/middle.html', 'utf8');

const dom = new JSDOM(html);
const document = dom.window.document;

const tableElement = document.getElementsByTagName('table')[0];
const tableData = [];

const trElements = tableElement.getElementsByTagName('tr');
for (let i = 0; i < trElements.length; i++) {
  const trElement = trElements[i];
  const rowData = [];

  const tdElements = trElement.getElementsByTagName('td');

  for (let j = 0; j < tdElements.length; j++) {
    const tdElement = tdElements[j];

    const cellValue = Uint8Array.from(tdElement.textContent, c => c.charCodeAt(0));
    rowData.push(cellValue);
  }

  tableData.push(rowData);
}

console.log(tableData);

const compressedCells = [];

for (let row = 0; row < tableData.length; row++) {
  for (let col = 0; col < tableData[row].length; col++) {
    compressedCells.push(pako.deflate(tableData[row][col]));
  }
}

const numRows = tableData.length;
const numCols = tableData[0].length;
const rowIndex = 9;
const colIndex = 9;
const compressedCellIndex = (rowIndex * numCols) + colIndex;
const decompressedCellData = pako.inflate(compressedCells[compressedCellIndex], { to: 'string' });
const decompressedCellValue = decompressedCellData[0];

console.log(decompressedCellValue);
console.log(pako.inflate(compressedCells[100], { to: 'string' }));
console.log(pako.inflate(compressedCells[1000], { to: 'string' }));
console.log(pako.inflate(compressedCells[5000], { to: 'string' }));
console.log(pako.inflate(compressedCells[20000], { to: 'string' }));
