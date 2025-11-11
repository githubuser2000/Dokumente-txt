var my_lzma = new LZMA("../src/lzma_worker.js");
/// To compress:
///NOTE: mode can be 1-9 (1 is fast and pretty good; 9 is slower and probably much better).
///NOTE: compress() can take a string or an array of bytes.
///      (A Node.js Buffer or a Uint8Array instance counts as an array of bytes.)
my_lzma.compress(string || byte_array, mode, on_finish(result, error) {}, on_progress(percent) {});

/// To decompress:
///NOTE: By default, the result will be returned as a string if it decodes as valid UTF-8 text;
///      otherwise, it will return a Uint8Array instance.
my_lzma.decompress(byte_array, on_finish(result, error) {}, on_progress(percent) {});
