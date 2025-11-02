#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

#define MAX_LINE 1024

typedef struct {
    char *token;
    int count;
} TokenCount;

TokenCount *token_array = NULL;
size_t token_size = 0;
size_t token_capacity = 0;

// Fügt Token hinzu oder erhöht Zähler
void add_token(const char *tok) {
    for (size_t i = 0; i < token_size; i++) {
        if (strcmp(token_array[i].token, tok) == 0) {
            token_array[i].count++;
            return;
        }
    }
    // Neues Token hinzufügen
    if (token_size == token_capacity) {
        token_capacity = token_capacity ? token_capacity * 2 : 128;
        token_array = realloc(token_array, token_capacity * sizeof(TokenCount));
    }
    token_array[token_size].token = strdup(tok);
    token_array[token_size].count = 1;
    token_size++;
}

// Prüft, ob Datei textlich ist
int is_text_file(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    int c;
    while ((c = fgetc(f)) != EOF) {
        if ((c < 0 || c > 127) && c != '\n' && c != '\r' && c != '\t') {
            fclose(f);
            return 0;
        }
    }
    fclose(f);
    return 1;
}

// Tokens aus Datei extrahieren
void extract_tokens(const char *file_path) {
    FILE *f = fopen(file_path, "r");
    if (!f) return;

    char line[MAX_LINE];
    char block[MAX_LINE * 10] = "";
    while (fgets(line, sizeof(line), f)) {
        char *p = line;
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == '\0') {
            if (strlen(block) > 0) {
                char *token = strtok(block, " \t\n\r");
                while (token) {
                    add_token(token);
                    token = strtok(NULL, " \t\n\r");
                }
                block[0] = '\0';
            }
        } else {
            strcat(block, line);
        }
    }
    if (strlen(block) > 0) {
        char *token = strtok(block, " \t\n\r");
        while (token) {
            add_token(token);
            token = strtok(NULL, " \t\n\r");
        }
    }

    fclose(f);
}

int main() {
    const char *folder = "/pfad/zu/deinem/ordner";
    const char *output_csv = "tokens.csv";

    DIR *dir = opendir(folder);
    if (!dir) {
        perror("Ordner konnte nicht geöffnet werden");
        return 1;
    }

    struct dirent *entry;
    char filepath[1024];
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            snprintf(filepath, sizeof(filepath), "%s/%s", folder, entry->d_name);
            if (is_text_file(filepath)) {
                extract_tokens(filepath);
            }
        }
    }
    closedir(dir);

    FILE *csv = fopen(output_csv, "w");
    if (!csv) {
        perror("CSV-Datei konnte nicht geöffnet werden");
        return 1;
    }

    for (size_t i = 0; i < token_size; i++) {
        fprintf(csv, "%s,%d\n", token_array[i].token, token_array[i].count);
        free(token_array[i].token);
    }
    free(token_array);
    fclose(csv);

    printf("Fertig! Tokens und Häufigkeit in %s gespeichert\n", output_csv);
    return 0;
}

