#include <stdio.h>
#include <stdlib.h>
#include <aspell.h>

int main() {
    AspellConfig *config = new_aspell_config();
    aspell_config_replace(config, "lang", "de"); // oder "en"

    AspellSpeller *speller = new_aspell_speller(config);
    const char* wort = "Pythn";

    int correct = aspell_speller_check(speller, wort, strlen(wort));
    if (correct) {
        printf("%s ist korrekt.\n", wort);
    } else {
        AspellStringEnumeration *suggestions = aspell_speller_suggest(speller, wort, strlen(wort));
        const char *sug;
        printf("%s ist falsch. Vorschläge:\n", wort);
        while ((sug = aspell_string_enumeration_next(suggestions)) != NULL) {
            printf("  - %s\n", sug);
        }
        delete_aspell_string_enumeration(suggestions);
    }

    delete_aspell_speller(speller);
    delete_aspell_config(config);
    return 0;
}

