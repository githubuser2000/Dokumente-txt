// Importieren der LZMA-JS-Bibliothek
const LZMA = require('lzma');
// KEINE ZENTRALE DATENHALDE
// Beispiel-Daten
const data = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' },
];

// Komprimierung in Chunks
const compressedChunks = [];
const uncompressedChunks = [];

const CHUNK_SIZE = 1; // Größe eines Chunks in Anzahl der Objekte

for (let i = 0; i < data.length; i += CHUNK_SIZE) {
  const chunk = JSON.stringify(data.slice(i, i + CHUNK_SIZE), 1);
  const compressedChunk = LZMA.compress(chunk, 9);
  compressedChunks.push(compressedChunk);
  uncompressedChunks.push(chunk);
}

// Ausgabe der komprimierten Daten
console.log('Komprimierte Chunks:');
console.log(compressedChunks);

// Dekomprimierung eines Chunks
const chunkIndexToDecompress = 1; // Index des Chunks, der dekomprimiert werden soll
const compressedChunkToDecompress = compressedChunks[chunkIndexToDecompress];
const decompressedChunk = LZMA.decompress(compressedChunkToDecompress);

// Vergleich der ursprünglichen Daten mit den dekomprimierten Daten
console.log('Ursprünglicher Chunk:');
console.log(uncompressedChunks[chunkIndexToDecompress]);

console.log('Dekomprimierter Chunk:');
console.log(decompressedChunk);
console.log('KEINE ZENTRALE DATENHALDE');
