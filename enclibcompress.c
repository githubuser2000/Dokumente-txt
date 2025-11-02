#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

#define MAX_LINE 1024

// Prüft, ob eine Datei textlich ist (hier einfache Heuristik)
int is_text_file(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    int c;
    while ((c = fgetc(f)) != EOF) {
        if ((c < 0 || c > 127) && c != '\n' && c != '\r' && c != '\t') {
            fclose(f);
            return 0; // vermutlich Binär
        }
    }
    fclose(f);
    return 1;
}

// Tokens zwischen Leerzeilen extrahieren und in CSV schreiben
void extract_tokens(const char *file_path, FILE *csv) {
    FILE *f = fopen(file_path, "r");
    if (!f) return;

    char line[MAX_LINE];
    char block[MAX_LINE * 10] = ""; // Sammelblock
    while (fgets(line, sizeof(line), f)) {
        // Zeilen-Trimming
        char *p = line;
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == '\0') {
            // Leerzeile → Block auswerten
            if (strlen(block) > 0) {
                char *token = strtok(block, " \t\n\r");
                while (token) {
                    fprintf(csv, "%s\n", token);
                    token = strtok(NULL, " \t\n\r");
                }
                block[0] = '\0';
            }
        } else {
            strcat(block, line);
        }
    }
    // Letzter Block
    if (strlen(block) > 0) {
        char *token = strtok(block, " \t\n\r");
        while (token) {
            fprintf(csv, "%s\n", token);
            token = strtok(NULL, " \t\n\r");
        }
    }

    fclose(f);
}

int main() {
    const char *folder = "/pfad/zu/deinem/ordner";
    const char *output_csv = "tokens.csv";

    FILE *csv = fopen(output_csv, "w");
    if (!csv) {
        perror("Fehler beim Öffnen der CSV");
        return 1;
    }

    DIR *dir = opendir(folder);
    if (!dir) {
        perror("Fehler beim Öffnen des Ordners");
        return 1;
    }

    struct dirent *entry;
    char filepath[1024];
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) { // reguläre Datei
            snprintf(filepath, sizeof(filepath), "%s/%s", folder, entry->d_name);
            if (is_text_file(filepath)) {
                extract_tokens(filepath, csv);
            }
        }
    }

    closedir(dir);
    fclose(csv);
    printf("Fertig! Tokens gespeichert in %s\n", output_csv);
    return 0;
}

