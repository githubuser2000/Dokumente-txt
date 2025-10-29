#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <ssdeep.h>

// =====================================
// Hilfsfunktionen
// =====================================

// Tokenize text into words (whitespace split)
int tokenize(const char* text, char tokens[][128], int max_tokens) {
    int count = 0;
    const char* start = text;
    while (*start && count < max_tokens) {
        while (*start == ' ') start++;
        if (!*start) break;
        const char* end = start;
        while (*end != ' ' && *end != '\0') end++;
        int len = end - start;
        if (len >= 128) len = 127;
        strncpy(tokens[count], start, len);
        tokens[count][len] = '\0';
        count++;
        start = end;
    }
    return count;
}

// Simple hash for SimHash: djb2
uint32_t hash_word(const char *str) {
    uint32_t hash = 5381;
    int c;
    while ((c = *str++))
        hash = ((hash << 5) + hash) + c;
    return hash;
}

// Compute SimHash
uint64_t compute_simhash(char tokens[][128], int len) {
    int bits[64] = {0};
    for (int i=0; i<len; i++) {
        uint64_t h = hash_word(tokens[i]);
        for (int j=0; j<64; j++) {
            if (h & ((uint64_t)1 << j))
                bits[j] += 1;
            else
                bits[j] -= 1;
        }
    }
    uint64_t simhash = 0;
    for (int j=0; j<64; j++) {
        if (bits[j] > 0)
            simhash |= ((uint64_t)1 << j);
    }
    return simhash;
}

// Hamming distance for SimHash
int hamming_distance(uint64_t a, uint64_t b) {
    uint64_t x = a ^ b;
    int dist = 0;
    while (x) { dist += x & 1; x >>= 1; }
    return dist;
}

// =====================================
// MinHash (naiv)
// =====================================

#define NUM_HASH 128

uint32_t minhash(char tokens[][128], int len) {
    uint32_t minhash_val = UINT32_MAX;
    for (int i=0;i<len;i++) {
        uint32_t h = hash_word(tokens[i]);
        if (h < minhash_val) minhash_val = h;
    }
    return minhash_val;
}

// Jaccard similarity approximation via MinHash (naiv, für Demo)
double minhash_similarity(uint32_t mhA, uint32_t mhB) {
    return mhA == mhB ? 1.0 : 0.0;  // sehr naive Approximation
}

// =====================================
// Main
// =====================================
int main() {

    const char* textA = "fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin";
    const char* textB = "fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin";

    // ---------------------------
    // 1. Fuzzy Hashing: ssdeep
    // ---------------------------
    char ssdeepA[BUFSIZ];
    char ssdeepB[BUFSIZ];
    if (ssdeep_hash_buf(textA, strlen(textA), ssdeepA, BUFSIZ) != 0) {
        printf("ssdeep hash A failed\n");
    }
    if (ssdeep_hash_buf(textB, strlen(textB), ssdeepB, BUFSIZ) != 0) {
        printf("ssdeep hash B failed\n");
    }
    int ssdeep_similarity = ssdeep_compare(ssdeepA, ssdeepB);
    printf("ssdeep A: %s\n", ssdeepA);
    printf("ssdeep B: %s\n", ssdeepB);
    printf("ssdeep similarity: %d %%\n\n", ssdeep_similarity);

    // ---------------------------
    // 2. SimHash
    // ---------------------------
    char tokensA[1024][128];
    char tokensB[1024][128];
    int lenA = tokenize(textA, tokensA, 1024);
    int lenB = tokenize(textB, tokensB, 1024);

    uint64_t simhashA = compute_simhash(tokensA, lenA);
    uint64_t simhashB = compute_simhash(tokensB, lenB);
    int hamming = hamming_distance(simhashA, simhashB);

    printf("SimHash A: %llu\n", simhashA);
    printf("SimHash B: %llu\n", simhashB);
    printf("SimHash Hamming distance: %d\n\n", hamming);

    // ---------------------------
    // 3. MinHash
    // ---------------------------
    uint32_t minhashA = minhash(tokensA, lenA);
    uint32_t minhashB = minhash(tokensB, lenB);
    double mh_sim = minhash_similarity(minhashA, minhashB);
    printf("MinHash A: %u\n", minhashA);
    printf("MinHash B: %u\n", minhashB);
    printf("MinHash similarity (naiv): %.2f\n\n", mh_sim);

    return 0;
}

