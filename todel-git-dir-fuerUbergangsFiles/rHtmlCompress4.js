const fs = require('fs');
const zstd = require('simple-zstd');
const cheerio = require('cheerio');
const {ZSTDCompress, ZSTDDecompress} = require('simple-zstd');

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

filename = 'zstd4out.file'

tableData.forEach((filename) => {
  fs.createReadStream(filename)
    .pipe(ZSTDCompress(3))
    .pipe(ZSTDDecompress())
    .pipe(fs.createWriteStream(`${filename}_copy.txt`))
    .on('error', (err) => {
      console.error(`Error processing ${filename}:`, err);
    })
    .on('finish', () => {
      console.log(`Copy of ${filename} Complete!`);
    });
});
