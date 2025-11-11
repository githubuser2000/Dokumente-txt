const fs = require('fs');
const { promisify } = require('util');
const pako = require('pako');

const readFile = promisify(fs.readFile);

(async function() {
  try {
    // Lese die HTML-Datei
    const html = await readFile('/home/alex/middle.html', 'utf8');
    // Erstelle ein temporäres Element, um das HTML zu parsen
    const tempElement = new DOMParser().parseFromString(html, 'text/html');
    // Greife auf alle table-Elemente im Dokument zu
    const tableElement =  tempElement.getElementsByTagName('table')[0];
    // Erstelle ein leeres 2D-Array, um die Tabellenzelleninhalte zu speichern
    const tableData = [];

    // Greife auf alle <tr>-Elemente in der Tabelle zu
    const trElements = tableElement.getElementsByTagName('tr');
    for (let i = 0; i < trElements.length; i++) {
      const trElement = trElements[i];
      const rowData = [];

      // Greife auf alle <td>-Elemente in der aktuellen <tr>-Zeile zu
      const tdElements = trElement.getElementsByTagName('td');

      // Iteriere durch alle <td>-Elemente in der aktuellen <tr>-Zeile
      for (let j = 0; j < tdElements.length; j++) {
        const tdElement = tdElements[j];

        // Konvertiere den Textinhalt des aktuellen <td>-Elements zu einem Uint8Array
        const cellValue = new TextEncoder().encode(tdElement.textContent);
        rowData.push(cellValue);
      }

      // Füge die aktuelle Zeile zur 2D-Matrix hinzu
      tableData.push(rowData);
    }

    // Gib das 2D-Array mit den Tabellenzelleninhalten aus
    console.log(tableData);

    // Komprimiere die Zelleninhalte
    const compressedCells = [];

    for (let row = 0; row < tableData.length; row++) {
      for (let col = 0; col < tableData[row].length; col++) {
        compressedCells.push(pako.deflate(tableData[row][col]));
        //if (row == 9 && col == 9)
        //console.log(tableData[row][col]);
      }
    }

    // Dekomprimiere eine Zelle
    const numRows = tableData.length;
    const numCols = tableData[0].length;
    const rowIndex = 9;
    const colIndex = 9;
    const compressedCellIndex = (rowIndex * numCols) + colIndex;
    const decompressedCellData = pako.inflate(compressedCells[compressedCellIndex], { to: 'string' });
    const decompressedCellValue = new TextDecoder().decode(decompressedCellData);

    // Gib den dekomprimierten Zellenwert aus
    console.log(decompressedCellValue);
    console.log(new TextDecoder().decode(pako.inflate(compressedCells[100], { to: 'string' })));
    console.log(new TextDecoder().decode(pako.inflate(compressedCells[1000], { to: 'string' })));
    console.log(new TextDecoder().decode(pako.inflate(compressedCells[5000], { to: 'string' })));
  }})
