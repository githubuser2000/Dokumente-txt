const fs = require('fs');
const { ZSTDCompress } = require('simple-zstd');

const filesToCompress = ['example1.txt', 'example2.txt', 'example3.txt'];
const outputStream = fs.createWriteStream('compressed.zst');

const compressStream = ZSTDCompress(3);

filesToCompress.forEach((filename) => {
  fs.createReadStream(filename)
    .pipe(compressStream)
    .on('error', (err) => {
      console.error(`Error processing ${filename}:`, err);
    })
    .pipe(outputStream, { end: false });
});

compressStream.on('end', () => {
  console.log('Compression complete!');
  outputStream.end();
});
