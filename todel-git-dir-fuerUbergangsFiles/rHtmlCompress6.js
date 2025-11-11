const fs = require('fs');
const { ZSTDCompress } = require('simple-zstd');

const table = [
  ['Name', 'Age', 'Gender'],
  ['John Doe', '30', 'Male'],
  ['Jane Smith', '25', 'Female'],
  ['Bob Johnson', '42', 'Male'],
];

const outputStream = fs.createWriteStream('compressed2.zst');

const compressStream = ZSTDCompress(3);

table.forEach((row) => {
  row.forEach((cell) => {
    compressStream.write(cell + '\n');
  });
});

compressStream.on('end', () => {
  console.log('Compression complete!');
  outputStream.end();
});

compressStream.pipe(outputStream);
