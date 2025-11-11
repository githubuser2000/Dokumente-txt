// Importieren der LZ-String Bibliothek
const LZString = require('lz-string');

// Beispiel-Daten in mehrere Chunks aufteilen
const data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed malesuada, dolor at feugiat tincidunt, mi lacus congue ipsum, vel bibendum magna enim a quam.';

const chunk1 = data.substring(0, 30);
const chunk2 = data.substring(30, 60);
const chunk3 = data.substring(60);

// Komprimierung der Chunks und Speicherung in einer zentralen Datenhalde
const compressedData = LZString.compressToBase64(chunk1) + LZString.compressToBase64(chunk2) + LZString.compressToBase64(chunk3);

// Dekomprimierung eines Teils der Daten
const decompressedChunk = LZString.decompressFromBase64(compressedData.substring(0, 100));

console.log(decompressedChunk);
