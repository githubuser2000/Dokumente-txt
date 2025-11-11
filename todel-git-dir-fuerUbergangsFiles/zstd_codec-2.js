const zstd = require('zstd-codec');

// Beispiel-Daten
const data = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' },
];

// Komprimieren der Daten in Blöcken
const blockSize = 1024 * 1024; // Blockgröße von 1 MB
const compressedData = [];
let offset = 0;

while (offset < data.length) {
  const block = data.slice(offset, offset + blockSize);
  const compressedBlock = zstd.compress(block);
  compressedData.push(compressedBlock);
  offset += blockSize;
}

// Dekomprimieren eines Teils der Daten
const startOffset = 10 * blockSize; // Offset, ab dem die Daten dekomprimiert werden sollen
const endOffset = 20 * blockSize; // Offset, bis zu dem die Daten dekomprimiert werden sollen

let currentOffset = 0;
let currentBlockIndex = 0;
let currentBlockOffset = 0;

while (currentOffset < endOffset) {
  const compressedBlock = compressedData[currentBlockIndex];
  const block = zstd.decompress(compressedBlock, {
    // Der letzte Block kann kleiner als die Blockgröße sein, deshalb müssen wir die Blockgröße für den letzten Block aktualisieren
    blockSize: currentBlockIndex === compressedData.length - 1 ? endOffset - currentOffset : blockSize
  });

  if (currentOffset + block.length > startOffset) {
    const startIndex = startOffset - currentOffset;
    const endIndex = Math.min(endOffset - currentOffset, startIndex + (endOffset - startOffset));
    const partialBlock = block.slice(startIndex, endIndex);
    console.log(partialBlock); // Ausgabe des dekomprimierten Teils der Daten
  }

  currentBlockIndex++;
  currentBlockOffset = currentOffset + block.length;
  currentOffset += block.length;
}
