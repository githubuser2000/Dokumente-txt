#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_WORD_LEN 100
#define MAX_DICT_WORDS 20
#define MAX_INPUT 1024

// Wörterbücher Deutsch und Englisch
const char* dict_de[MAX_DICT_WORDS] = {"ich", "liebe", "programmieren", "und", "python", "korrigieren", "text", "ein", "beispiel"};
const char* dict_en[MAX_DICT_WORDS] = {"i", "love", "programming", "and", "python", "correct", "text", "an", "example"};

// Größe der Wörterbücher
int size_de = 9;
int size_en = 9;

// Levenshtein-Distanz
int min(int a, int b, int c) {
    int m = a < b ? a : b;
    return m < c ? m : c;
}

int levenshtein(const char *s1, const char *s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);
    int dp[len1+1][len2+1];

    for (int i = 0; i <= len1; i++) dp[i][0] = i;
    for (int j = 0; j <= len2; j++) dp[0][j] = j;

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (s1[i-1] == s2[j-1]) ? 0 : 1;
            dp[i][j] = min(
                dp[i-1][j]+1,
                dp[i][j-1]+1,
                dp[i-1][j-1]+cost
            );
        }
    }
    return dp[len1][len2];
}

// Satzzeichen entfernen
void clean_word(const char* input, char* output) {
    int j = 0;
    for (int i = 0; input[i]; i++) {
        if (isalnum(input[i])) {
            output[j++] = tolower(input[i]);
        }
    }
    output[j] = '\0';
}

// Korrigiere Wort
const char* korrigiere_wort(const char* wort, const char* sprache) {
    char clean[MAX_WORD_LEN];
    clean_word(wort, clean);

    const char** dict;
    int dict_size;

    if (strcmp(sprache, "de") == 0) {
        dict = dict_de;
        dict_size = size_de;
    } else {
        dict = dict_en;
        dict_size = size_en;
    }

    int min_dist = MAX_WORD_LEN;
    const char* best_match = wort;

    for (int i = 0; i < dict_size; i++) {
        int dist = levenshtein(clean, dict[i]);
        if (dist < min_dist) {
            min_dist = dist;
            best_match = dict[i];
        }
    }

    // Großschreibung übernehmen, falls erstes Zeichen original groß
    static char result[MAX_WORD_LEN];
    if (isupper(wort[0])) {
        snprintf(result, MAX_WORD_LEN, "%c%s", toupper(best_match[0]), best_match+1);
        return result;
    }
    return best_match;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <de/en> <text>\n", argv[0]);
        return 1;
    }

    const char* sprache = argv[1];
    if (strcmp(sprache, "de") != 0 && strcmp(sprache, "en") != 0) {
        printf("Sprache '%s' wird nicht unterstützt. Verwende 'de' oder 'en'.\n", sprache);
        return 1;
    }

    // Text zusammensetzen
    char text[MAX_INPUT] = "";
    for (int i = 2; i < argc; i++) {
        strcat(text, argv[i]);
        if (i < argc-1) strcat(text, " ");
    }

    // Wörter tokenisieren und korrigieren
    char* token = strtok(text, " ");
    printf("Korrigierter Text: ");
    while (token != NULL) {
        printf("%s ", korrigiere_wort(token, sprache));
        token = strtok(NULL, " ");
    }
    printf("\n");
    return 0;
}

