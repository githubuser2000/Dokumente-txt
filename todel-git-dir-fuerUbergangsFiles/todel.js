const zstd = require('zstd-codec');

const originalString = 'Hello, world!';

// Komprimieren
const compressedData = zstd.compress(originalString);

// Dekomprimieren
const decompressedString = zstd.decompress(compressedData);

console.log(decompressedString); // 'Hello, world!'

