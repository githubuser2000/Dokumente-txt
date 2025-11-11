import { decompress } from "@oneidentity/zstd-js/wasm/decompress";

async function loadAndDecompressData() {
  const response = await fetch('compressed.zst');
  const compressedData = await response.arrayBuffer();
  const decompressedData = await decompress(compressedData);
  console.log(decompressedData);
}

loadAndDecompressData();
