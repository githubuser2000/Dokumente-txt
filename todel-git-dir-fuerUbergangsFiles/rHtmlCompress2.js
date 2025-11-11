const fs = require('fs');
const {ZSTDCompress, ZSTDDecompress} = require('simple-zstd');

// ZSTDCompress(compressionLevel, streamOptions)
// ZSTDDecompress(streamOptions)

const filesToCompress = ['example1.txt', 'example2.txt', 'example3.txt'];

filesToCompress.forEach((filename) => {
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
