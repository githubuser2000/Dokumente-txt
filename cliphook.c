#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <openssl/sha.h>
#include <time.h>

#define LOG_FILE "/home/dein_user/clipboard.log"
#define INTERVAL 2  // Sekunden
#define MAX_LEN 65536

// Funktion zum Hashen des Inhalts
void sha256_hash(const char *str, unsigned char output[SHA256_DIGEST_LENGTH]) {
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, str, strlen(str));
    SHA256_Final(output, &ctx);
}

// Vergleicht zwei Hashes
int hash_equal(unsigned char a[SHA256_DIGEST_LENGTH], unsigned char b[SHA256_DIGEST_LENGTH]) {
    return memcmp(a, b, SHA256_DIGEST_LENGTH) == 0;
}

// Loggt Clipboard-Inhalt mit Timestamp
void log_clipboard(const char *content) {
    FILE *f = fopen(LOG_FILE, "a");
    if (!f) return;

    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm_info);

    fprintf(f, "[%s]\n%s\n\n", buf, content);
    fclose(f);
}

int main() {
    unsigned char last_hash[SHA256_DIGEST_LENGTH] = {0};
    unsigned char current_hash[SHA256_DIGEST_LENGTH];

    while (1) {
        FILE *fp = popen("wl-paste -n 2>/dev/null", "r");
        if (!fp) {
            fprintf(stderr, "Fehler beim Ausführen von wl-paste\n");
            exit(1);
        }

        char buffer[MAX_LEN] = {0};
        fread(buffer, 1, MAX_LEN-1, fp);
        pclose(fp);

        // Entferne mögliche neue Zeilen am Ende
        buffer[strcspn(buffer, "\n")] = 0;

        if (strlen(buffer) > 0) {
            sha256_hash(buffer, current_hash);

            if (!hash_equal(current_hash, last_hash)) {
                log_clipboard(buffer);
                printf("Neuer Clipboard-Inhalt geloggt: %.30s...\n", buffer);
                memcpy(last_hash, current_hash, SHA256_DIGEST_LENGTH);
            }
        }

        sleep(INTERVAL);
    }

    return 0;
}

