#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>

#ifdef _WIN32
#include <io.h>
#define PATHSEP '\\'
#else
#define PATHSEP '/'
#endif

static void write_uint32_le(FILE *f, uint32_t val) {
    unsigned char b[4];
    b[0] = val & 0xFF;
    b[1] = (val >> 8) & 0xFF;
    b[2] = (val >> 16) & 0xFF;
    b[3] = (val >> 24) & 0xFF;
    fwrite(b, 1, 4, f);
}

static void write_uint64_le(FILE *f, uint64_t val) {
    unsigned char b[8];
    for (int i = 0; i < 8; i++)
        b[i] = (val >> (8 * i)) & 0xFF;
    fwrite(b, 1, 8, f);
}

static uint32_t read_uint32_le(FILE *f) {
    unsigned char b[4];
    if (fread(b, 1, 4, f) != 4) return 0;
    return (uint32_t)b[0] | ((uint32_t)b[1] << 8) |
           ((uint32_t)b[2] << 16) | ((uint32_t)b[3] << 24);
}

static uint64_t read_uint64_le(FILE *f) {
    unsigned char b[8];
    if (fread(b, 1, 8, f) != 8) return 0;
    uint64_t val = 0;
    for (int i = 0; i < 8; i++)
        val |= ((uint64_t)b[i]) << (8 * i);
    return val;
}

static void pack_file(FILE *out, const char *base, const char *path) {
    struct stat st;
    if (stat(path, &st) != 0 || !S_ISREG(st.st_mode))
        return;

    const char *rel = path + strlen(base);
    if (*rel == PATHSEP) rel++;
    uint32_t path_len = strlen(rel);
    uint64_t size = st.st_size;

    write_uint32_le(out, path_len);
    fwrite(rel, 1, path_len, out);
    write_uint64_le(out, size);

    FILE *in = fopen(path, "rb");
    if (!in) return;
    char buf[65536];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), in)) > 0)
        fwrite(buf, 1, n, out);
    fclose(in);
}

static void pack_dir(FILE *out, const char *base, const char *dirpath) {
    DIR *dir = opendir(dirpath);
    if (!dir) return;
    struct dirent *entry;
    while ((entry = readdir(dir))) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        char fullpath[4096];
        snprintf(fullpath, sizeof(fullpath), "%s%c%s", dirpath, PATHSEP, entry->d_name);
        struct stat st;
        if (stat(fullpath, &st) != 0) continue;

        if (S_ISDIR(st.st_mode)) {
            pack_dir(out, base, fullpath);
        } else if (S_ISREG(st.st_mode)) {
            pack_file(out, base, fullpath);
        }
    }
    closedir(dir);
}

static void unpack_file(FILE *in, const char *outdir) {
    uint32_t path_len = read_uint32_le(in);
    if (path_len == 0) return;

    char *path = malloc(path_len + 1);
    fread(path, 1, path_len, in);
    path[path_len] = '\0';
    uint64_t size = read_uint64_le(in);

    char fullpath[4096];
    snprintf(fullpath, sizeof(fullpath), "%s%c%s", outdir, PATHSEP, path);
    free(path);

    // Verzeichnisse anlegen
    for (char *p = fullpath; *p; p++) {
        if (*p == PATHSEP) {
            *p = '\0';
            mkdir(fullpath, 0755);
            *p = PATHSEP;
        }
    }

    FILE *out = fopen(fullpath, "wb");
    if (!out) return;
    char buf[65536];
    uint64_t remaining = size;
    while (remaining > 0) {
        size_t to_read = (remaining > sizeof(buf)) ? sizeof(buf) : (size_t)remaining;
        size_t n = fread(buf, 1, to_read, in);
        if (n == 0) break;
        fwrite(buf, 1, n, out);
        remaining -= n;
    }
    fclose(out);
}

void pack(const char *folder, const char *outfile) {
    FILE *out = fopen(outfile, "wb");
    if (!out) {
        perror("open output");
        exit(1);
    }
    pack_dir(out, folder, folder);
    write_uint32_le(out, 0); // Endmarkierung
    fclose(out);
}

void unpack(const char *infile, const char *outfolder) {
    FILE *in = fopen(infile, "rb");
    if (!in) {
        perror("open input");
        exit(1);
    }
    while (1) {
        long pos = ftell(in);
        uint32_t len = read_uint32_le(in);
        if (len == 0 || feof(in)) break;
        fseek(in, pos, SEEK_SET);
        unpack_file(in, outfolder);
    }
    fclose(in);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s pack <folder> <outfile>\n", argv[0]);
        fprintf(stderr, "       %s unpack <infile> <outfolder>\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "pack") == 0) {
        pack(argv[2], argv[3]);
    } else if (strcmp(argv[1], "unpack") == 0) {
        unpack(argv[2], argv[3]);
    } else {
        fprintf(stderr, "Unknown mode: %s\n", argv[1]);
        return 1;
    }
    return 0;
}
