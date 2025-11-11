const fs = require('fs');
const {ZSTDCompress, ZSTDDecompress} = require('simple-zstd');

// ZSTDCompress(compressionLevel, streamOptions)
// ZSTDDecompress(streamOptions)

fs.createReadStream('example.txt')
  .pipe(ZSTDCompress(3))
  .pipe(ZSTDDecompress())
  .pipe(fs.createWriteStream('example_copy.txt'))
  .on('error', (err) => {
    //..
  })
  .on('finish', () => {
    console.log('Copy Complete!');
  })

  // -> Copy Complete
