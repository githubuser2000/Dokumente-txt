const ZstdCodec = require('zstd-codec').ZstdCodec;
ZstdCodec.run(zstd => {
    const simple = new zstd.Simple();
    const streaming = new zstd.Streaming();

//const streaming = new ZstdCodec.run().Streaming();
//const compressed = streaming.compress(data); // use default compression_level 3

// chunks: data chunks to compress, must be Iterable of Uint8Array
const size = 10;
const array = new Uint8Array(size);

for (let i = 0; i < size; i++) {
  array[i] = Math.floor(Math.random() * 256);
}
const chunks = array;
//const size_hint = 10; //chunks.map((ar) => ar.length).reduce((p, c) => p + c);
const compressed = streaming.compressChunks(chunks); // use default compression_level 3
//const data = streaming.decompress(data); // can omit size_hint

//const size_hint = 2 * 1024 * 1024; // 2MiB
//const data = streaming.decompressChunks(compressed, size_hint);
});
