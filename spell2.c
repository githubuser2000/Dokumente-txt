#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_WORD_LEN 100
#define DICT_SIZE 5

// Wörterbuch
const char* dictionary[DICT_SIZE] = {"python", "programmieren", "liebe", "ich", "und"};

// Levenshtein-Distanz berechnen
int min(int a, int b, int c) {
    int m = a < b ? a : b;
    return m < c ? m : c;
}

int levenshtein(const char *s1, const char *s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);
    int matrix[len1+1][len2+1];

    for (int i = 0; i <= len1; i++) matrix[i][0] = i;
    for (int j = 0; j <= len2; j++) matrix[0][j] = j;

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (s1[i-1] == s2[j-1]) ? 0 : 1;
            matrix[i][j] = min(
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + cost
            );
        }
    }
    return matrix[len1][len2];
}

// Wort korrigieren
const char* korrigiere_wort(const char *word) {
    int min_dist = MAX_WORD_LEN;
    const char* best_match = word;

    for (int i = 0; i < DICT_SIZE; i++) {
        int dist = levenshtein(word, dictionary[i]);
        if (dist < min_dist) {
            min_dist = dist;
            best_match = dictionary[i];
        }
    }
    return best_match;
}

int main() {
    char text[] = "Ich liebe Pythn und proggrammieren";
    char *token = strtok(text, " ");

    printf("Korrigierter Text: ");
    while (token != NULL) {
        printf("%s ", korrigiere_wort(token));
        token = strtok(NULL, " ");
    }
    printf("\n");
    return 0;
}

