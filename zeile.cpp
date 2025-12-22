#include <iostream>
#include <string>
#include <cstdlib>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <zeilennummer>\n";
        return 1;
    }

    int zeile;
    try {
        zeile = std::stoi(argv[1]);
    } catch (...) {
        std::cerr << "Fehler: Zeilennummer muss eine Zahl sein.\n";
        return 1;
    }

    int ziel = zeile + 1;
    std::string line;
    int index = 1;
    while (std::getline(std::cin, line)) {
        if (index == ziel) {
            std::cout << line << std::endl;
            break;
        }
        ++index;
    }

    return 0;
}

