#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ssdeep.h>  // ssdeep C-Bibliothek: https://ssdeep-project.github.io/ssdeep/
#include <tlsh.h>    // TLSH C-Bibliothek: https://github.com/trendmicro/tlsh

// Helper function: tokenize text into words (naiv, whitespace split)
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

// Naive Jaccard similarity
double jaccard_similarity(char tokensA[][128], int lenA, char tokensB[][128], int lenB) {
    int intersection = 0;
    for (int i = 0; i < lenA; i++) {
        for (int j = 0; j < lenB; j++) {
            if (strcmp(tokensA[i], tokensB[j]) == 0) {
                intersection++;
                break;
            }
        }
    }
    int union_count = lenA + lenB - intersection;
    return (double)intersection / union_count;
}

// Entry point
int main() {
    const char* textA = "fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin";
    const char* textB = "fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin";

    // =========================
    // 1. Fuzzy Hashing: ssdeep
    // =========================
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
    printf("ssdeep similarity: %d %%\n", ssdeep_similarity);

    // =========================
    // 2. TLSH
    // =========================
    TLSH_CTX *tlshA = TLSH_CTX_new();
    TLSH_CTX *tlshB = TLSH_CTX_new();
    TLSH_CTX_update(tlshA, (const unsigned char*)textA, strlen(textA));
    TLSH_CTX_update(tlshB, (const unsigned char*)textB, strlen(textB));
    unsigned char digestA[TLSH_DIGEST_LENGTH];
    unsigned char digestB[TLSH_DIGEST_LENGTH];
    TLSH_CTX_final(tlshA, digestA);
    TLSH_CTX_final(tlshB, digestB);
    int tlsh_diff = TLSH_diff_digest(digestA, digestB);
    printf("TLSH difference (smaller=more similar): %d\n", tlsh_diff);
    TLSH_CTX_free(tlshA);
    TLSH_CTX_free(tlshB);

    // =========================
    // 3. Tokenization + Jaccard similarity
    // =========================
    char tokensA[1024][128];
    char tokensB[1024][128];
    int lenA = tokenize(textA, tokensA, 1024);
    int lenB = tokenize(textB, tokensB, 1024);
    double jaccard = jaccard_similarity(tokensA, lenA, tokensB, lenB);
    printf("Jaccard similarity: %.4f\n", jaccard);

    // =========================
    // 4. Cosine similarity (naive Bag-of-Words)
    // =========================
    // Simple vectorization by word count
    int word_count = 0;
    char vocabulary[2048][128];
    int vectorA[2048] = {0};
    int vectorB[2048] = {0};

    // Build vocabulary
    for (int i = 0; i < lenA; i++) {
        int found = 0;
        for (int j = 0; j < word_count; j++) {
            if (strcmp(tokensA[i], vocabulary[j]) == 0) { found=1; break;}
        }
        if (!found) strcpy(vocabulary[word_count++], tokensA[i]);
    }
    for (int i = 0; i < lenB; i++) {
        int found = 0;
        for (int j = 0; j < word_count; j++) {
            if (strcmp(tokensB[i], vocabulary[j]) == 0) { found=1; break;}
        }
        if (!found) strcpy(vocabulary[word_count++], tokensB[i]);
    }

    // Count occurrences
    for (int i = 0; i < word_count; i++) {
        for (int j = 0; j < lenA; j++) if(strcmp(tokensA[j], vocabulary[i])==0) vectorA[i]++;
        for (int j = 0; j < lenB; j++) if(strcmp(tokensB[j], vocabulary[i])==0) vectorB[i]++;
    }

    // Compute cosine similarity
    double dot=0, normA=0, normB=0;
    for(int i=0;i<word_count;i++){
        dot += vectorA[i]*vectorB[i];
        normA += vectorA[i]*vectorA[i];
        normB += vectorB[i]*vectorB[i];
    }
    double cos_sim = dot / (sqrt(normA)*sqrt(normB));
    printf("Cosine similarity: %.4f\n", cos_sim);

    return 0;
}

