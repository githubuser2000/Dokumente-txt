#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <iomanip>
#include <algorithm>

// Funktion zum Auslesen einer Spalte aus einer CSV-Datei
void spalte_aus_csv_ausgeben(const std::string &dateiname, int spaltennummer) {
    try {
        std::ifstream infile(dateiname);
        if (!infile.is_open()) {
            std::cerr << "[FEHLER] Datei nicht gefunden: " << dateiname << "\n";
            return;
        }

        std::string line;
        int merkezeile = 0;
        std::vector<std::vector<std::string>> csvlines;

        // CSV-Datei einlesen
        while (std::getline(infile, line)) {
            std::vector<std::string> cols;
            std::string col;
            std::stringstream ss(line);
            while (std::getline(ss, col, ';')) {
                cols.push_back(col);
            }
            csvlines.push_back(cols);
        }

        // merkezeile bestimmen (erste Spalte mit >3 Zeichen)
        for (size_t i = 0; i < csvlines.size(); ++i) {
            if (spaltennummer < csvlines[i].size() && csvlines[i][spaltennummer].length() > 3) {
                merkezeile = i + 1;
            }
        }

        // Ausgabe der Spalte
        for (size_t i = 0; i < csvlines.size(); ++i) {
            if (spaltennummer < csvlines[i].size()) {
                if (static_cast<int>(i+1) <= merkezeile) {
                    std::cout << std::setw(4) << std::setfill('0') << i << ".:   " << csvlines[i][spaltennummer] << "\n";

                } else {
                    std::cout << std::setw(4) << (i+1) << ".\n";
                }
            } else {
                std::cout << "[WARNUNG] Zeile zu kurz: " << i+1 << "\n";
                break;
            }
        }

    } catch (const std::exception &e) {
        std::cerr << "[FEHLER] " << e.what() << "\n";
    }
}

// --- Hauptprogramm ---
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <key>\n";
        return 1;
    }

    std::string arg = argv[1];

    // dictA
    std::map<std::string, std::vector<std::pair<std::string, std::string>>> dictA = {
        {"q", {{"020","1"}, {"020","2"}}},
        {"w", {{"001","7"}, {"019","0"}}},
        {"ac", {{"001","8"}, {"031","0"}}},
        {"ad", {{"001","9"}, {"003","2"}, {"049","0"}}},
        {"ae", {{"001","10"}, {"048","0"}, {"048", "1"}}},
        {"ak", {{"001","11"}}},
        {"au", {{"001","12"}}},
        {"z", {{"002","2"}}},
        {"x", {{"009","0"}, {"018","0"}, {"018","1"}, {"053", "0"}}},
        {"r", {{"011","0"}, {"018","0"}}},
        {"aa", {{"013","0"}, {"013","1"}, {"013","2"}}},
        {"at", {{"019","1"}}},
        {"t", {{"021","1"}, {"021","2"}}},
        {"p", {{"044","0"}, {"020","1"}, {"073", "0"}}},
        {"s", {{"022","1"}}},
        {"k", {{"023","0"}, {"023","1"}}},
        {"ab", {{"032","0"}}}
    };

    // dict1
    std::map<std::string, std::vector<std::pair<std::string, std::string>>> dict1 = {
        {"17", {{"020","1"}, {"020","2"}}},
        {"23", {{"001","7"}, {"019","0"}}},
        {"29", {{"001","8"}, {"031","0"}}},
        {"30", {{"001","9"}, {"003","2"}, {"049","0"}}},
        {"31", {{"001","10"}, {"048","0"}, {"048", "1"}}},
        {"37", {{"001","11"}}},
        {"47", {{"001","12"}}},
        {"26", {{"002","2"}}},
        {"24", {{"009","0"}, {"018","0"}, {"018","1"}, {"053", "0"}}},
        {"18", {{"011","0"}, {"018","0"}}},
        {"27", {{"013","0"}, {"013","1"}, {"013","2"}}},
        {"46", {{"019","1"}}},
        {"16", {{"044","0"}, {"020","1"}, {"073", "0"}}},
        {"20", {{"021","1"}, {"021","2"}}},
        {"19", {{"022","1"}}},
        {"11", {{"023","0"}, {"023","1"}}},
        {"28", {{"032","0"}}}
    };

    std::vector<std::pair<std::string,std::string>> bla;

    auto it1 = dict1.find(arg);
    if (it1 != dict1.end()) {
        bla = it1->second;
    } else {
        auto it2 = dictA.find(arg);
        if (it2 != dictA.end()) {
            bla = it2->second;
        } else {
            std::cerr << "[FEHLER] Key nicht gefunden: " << arg << "\n";
            return 1;
        }
    }

    for (auto &b : bla) {
        std::string dateiname = "concat-reli-" + b.first + ".csv";
        int spaltennummer = std::stoi(b.second);
        spalte_aus_csv_ausgeben(dateiname, spaltennummer);
    }

    return 0;
}

