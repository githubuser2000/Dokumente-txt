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

for (let i = 0; i < tableData.length; i++) {
  const filename = `table_${i+1}.html`;
  const tableHtml = createTableHtml(tableData[i]);
  //const compressedHtml = zstd.ZSTDCompress(JSON.stringify(tableHtml)).toString('base64');
  const compressedHtml = zstd.ZSTDCompress(tableHtml).toString('base64');
  
  fs.writeFileSync(filename, compressedHtml);
  
  console.log(`Compressed table ${i+1} and saved to ${filename}`);
}

function createTableHtml(tableData) {
  const $ = cheerio.load('<table></table>');
  const $table = $('table');
  for (let i = 0; i < tableData.length; i++) {
    const $row = $('<tr></tr>');
    for (let j = 0; j < tableData[i].length; j++) {
      const $cell = $('<td></td>');
      $cell.text(tableData[i][j]);
      $row.append($cell);
    }
    $table.append($row);
  }
  return $.html();
}
