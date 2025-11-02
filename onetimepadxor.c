#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char *msg = "Hallo Welt";
    size_t len = strlen(msg);
    unsigned char *key = malloc(len);
    unsigned char *cipher = malloc(len);
    unsigned char *plain = malloc(len);

    // zufälligen Schlüssel erzeugen
    FILE *urand = fopen("/dev/urandom", "rb");
    fread(key, 1, len, urand);
    fclose(urand);

    // XOR-Verschlüsselung
    for (size_t i = 0; i < len; i++)
        cipher[i] = msg[i] ^ key[i];

    // Entschlüsselung
    for (size_t i = 0; i < len; i++)
        plain[i] = cipher[i] ^ key[i];

    // Ausgabe
    printf("Nachricht:  %s\n", msg);
    printf("Schlüssel:  ");
    for (size_t i = 0; i < len; i++) printf("%02x", key[i]);
    printf("\nCipher:     ");
    for (size_t i = 0; i < len; i++) printf("%02x", cipher[i]);
    printf("\nKlartext:   %.*s\n", (int)len, plain);

    free(key);
    free(cipher);
    free(plain);
    return 0;
}
