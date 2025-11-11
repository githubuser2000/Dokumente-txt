// Daten in Abschnitte aufteilen
const data = "Dies ist ein Testtext";
const sections = [
  data.slice(0, 6),
  data.slice(6, 12),
  data.slice(12, 16),
  data.slice(16)
];

// Jeden Abschnitt einzeln komprimieren
const compressedSections = sections.map(section => pako.deflate(section));

// Nur einen Abschnitt dekomprimieren
const decompressedSection = pako.inflate(compressedSections[1], { to: "string" });
console.log(decompressedSection); // "ist ein"

