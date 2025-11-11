const fs = require('fs');
const { ZSTDCompress } = require('simple-zstd');
const { Transform } = require('stream');

const filesToCompress = ['example1.txt', 'example2.txt', 'example3.txt'];
const jsonDataFilePath = 'json-data-file.json';
const outputStream = fs.createWriteStream('compressed.zst.json');
const compressStream = ZSTDCompress(3);
const binaryToJsonStream = new Transform({
  transform(chunk, encoding, callback) {
    const jsonObject = { data: chunk.toString('base64') };
    const jsonString = JSON.stringify(jsonObject);
    this.push(jsonString);
    callback();
  },
});



filesToCompress.forEach((filename) => {
  fs.createReadStream(filename)
    .pipe(compressStream)
    .on('error', (err) => {
      console.error(`Error processing ${filename}:`, err);
    })
    .pipe(binaryToJsonStream)
    .pipe(outputStream, { end: false });
});

compressStream.on('end', () => {
  console.log('Compression complete!');
  outputStream.end();
});
