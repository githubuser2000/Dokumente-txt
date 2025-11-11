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
    const compressedCell = ZSTDCompress(Buffer.from($.html()), { level: 3 });
    compressedTable[`${i},${j}`] = compressedCell;
  }
}

const compressedTableString = JSON.stringify(compressedTable);

ZSTDDecompress()
  .end(Buffer.from(compressedTableString, 'utf-8'))
  .pipe(fs.createWriteStream('table.html.zst'))
  .on('error', (err) => {
    console.error('Error writing compressed table:', err);
  })
  .on('finish', () => {
    console.log('Compressed table saved to table.html.zst');
  });

// read compressed table file and decompress
fs.createReadStream('table.html.zst')
  .pipe(ZSTDDecompress())
  .on('error', (err) => {
    console.error('Error decompressing table:', err);
  })
  .on('data', (data) => {
    const decompressedTable = JSON.parse(data.toString());
    for (const cellKey in decompressedTable) {
      const [i, j] = cellKey.split(',');
      const decompressedCell = ZSTDDecompress(decompressedTable[cellKey]);
      const $ = cheerio.load(decompressedCell.toString());
      console.log(`Cell[${i}][${j}]: ${$('td').text()}`);
    }
  });
