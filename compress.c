#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// =====================================
// RLE Encoder
// =====================================
char* rle_encode(const char* input) {
    if (input == NULL) return NULL;

    int len = strlen(input);
    // Schätzung: jedes Symbol + max. 4-stellige Zahl
    char* encoded = malloc(len * 5 + 1);
    if (!encoded) return NULL;

    int count = 1;
    int pos = 0;

    for (int i = 1; i <= len; i++) {
        if (i < len && input[i] == input[i - 1]) {
            count++;
        } else {
            pos += sprintf(encoded + pos, "%c%d", input[i - 1], count);
            count = 1;
        }
    }

    encoded[pos] = '\0';
    return encoded;
}

// =====================================
// RLE Decoder
// =====================================
char* rle_decode(const char* encoded) {
    if (encoded == NULL) return NULL;

    int len = strlen(encoded);
    char* decoded = malloc(len * 10 + 1); // grobe Schätzung
    if (!decoded) return NULL;

    int pos = 0;
    char symbol;
    int count = 0;

    for (int i = 0; i < len; i++) {
        if (encoded[i] >= '0' && encoded[i] <= '9') {
            count = count * 10 + (encoded[i] - '0');
        } else {
            if (i != 0) {
                for (int j = 0; j < count; j++) {
                    decoded[pos++] = symbol;
                }
            }
            symbol = encoded[i];
            count = 0;
        }
    }
    // Letztes Symbol
    for (int j = 0; j < count; j++) {
        decoded[pos++] = symbol;
    }
    decoded[pos] = '\0';
    return decoded;
}

// =====================================
// Test
// =====================================
int main() {
    const char* text = "AAAAABBBBCCCCCCDD";

    char* encoded = rle_encode(text);
    printf("Original: %s\n", text);
    printf("Encoded : %s\n", encoded);

    char* decoded = rle_decode(encoded);
    printf("Decoded : %s\n", decoded);

    printf("Correct ? %s\n", strcmp(text, decoded) == 0 ? "Yes" : "No");

    free(encoded);
    free(decoded);
    return 0;
}

