const fs = require('fs');
const { ZSTDCompress, ZSTDDecompress } = require('simple-zstd');
const cheerio = require('cheerio');

const tableData = [
  [
    ['Zelle 1', 'Zelle 2'],
    ['Zelle 3', 'Zelle 4']
  ],
  [
    ['Zelle 5', 'Zelle 6'],
    ['Zelle 7', 'Zelle 8']
  ],
  [
    ['Zelle 9', 'Zelle 10'],
    ['Zelle 11', 'Zelle 12']
  ],
  [
    ['Zelle 13', 'Zelle 14'],
    ['Zelle 15', 'Zelle 16']
  ]
];

const compressedTable = {};

for (let i = 0; i < tableData.length; i++) {
  for (let j = 0; j < tableData[i].length; j++) {
    const $ = cheerio.load('<td></td>');
    $('td').text(tableData[i][j]);
    const compressedCell = ZSTDCompress(3).read($.html());
    compressedTable[`${i},${j}`] = compressedCell;
     console.log(`${i},${j}: ${compressedCell}`);
  }
}

const compressedTableString = JSON.stringify(compressedTable);

fs.writeFileSync('table.html.zst', ZSTDCompress(3).read(compressedTableString).toString());

const compressedTableStringFromFile = ZSTDDecompress().end(fs.readFileSync('table.html.zst')).toString();

const compressedTableFromFile = JSON.parse(compressedTableStringFromFile);

for (const key in compressedTableFromFile) {
  const decompressedCell = cheerio.load(ZSTDDecompress().end(compressedTableFromFile[key]).toString());
  console.log(`${key}: ${decompressedCell('td').text()}`);
}
