#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    FILE *f;
    char buf[8192];
    size_t n;

    if (argc == 1) {
        // Keine Argumente -> stdin
        while ((n = fread(buf, 1, sizeof(buf), stdin)) > 0) {
            fwrite(buf, 1, n, stdout);
        }
    } else {
        for (int i = 1; i < argc; i++) {
            if (argv[i][0] == '-' && argv[i][1] == '\0') {
                f = stdin;
            } else {
                f = fopen(argv[i], "rb");
                if (!f) {
                    fprintf(stderr, "cat: %s: cannot open\n", argv[i]);
                    continue;
                }
            }

            while ((n = fread(buf, 1, sizeof(buf), f)) > 0) {
                fwrite(buf, 1, n, stdout);
            }

            if (f != stdin) fclose(f);
        }
    }

    return 0;
}
