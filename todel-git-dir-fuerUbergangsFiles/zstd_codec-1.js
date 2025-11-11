const { compress } = require('zstd_codec');

// Daten, die komprimiert werden sollen
const chunks = ['Hello', 'World', 'This', 'is', 'a', 'test'];

// Komprimierung
const compressedChunks = chunks.map(chunk => compress(chunk));

console.log(compressedChunks);
