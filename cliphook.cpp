#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <array>
#include <memory>
#include <chrono>
#include <thread>
#include <ctime>
#include <cstring>
#include <openssl/sha.h>

const std::string LOG_FILE = "/home/dein_user/clipboard.log";
const int INTERVAL = 2; // Sekunden

// Funktion, um einen Befehl auszuführen und stdout zurückzugeben
std::string exec(const char* cmd) {
    std::array<char, 4096> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

// SHA-256 Hash berechnen
std::string sha256(const std::string& str) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(str.c_str()), str.size(), hash);
    std::ostringstream oss;
    for(int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        oss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return oss.str();
}

// Clipboard-Inhalt loggen
void logClipboard(const std::string& content) {
    std::ofstream log(LOG_FILE, std::ios::app);
    if (!log) return;

    std::time_t t = std::time(nullptr);
    char buf[64];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&t));

    log << "[" << buf << "]\n" << content << "\n\n";
}

int main() {
    std::string lastHash;

    while(true) {
        try {
            std::string content = exec("wl-paste -n 2>/dev/null");

            // Entferne trailing newline
            if (!content.empty() && content.back() == '\n') content.pop_back();

            if (!content.empty()) {
                std::string currentHash = sha256(content);

                if (currentHash != lastHash) {
                    logClipboard(content);
                    std::cout << "Neuer Clipboard-Inhalt geloggt: " << content.substr(0,30) << "...\n";
                    lastHash = currentHash;
                }
            }
        } catch (const std::exception& e) {
            std::cerr << "Fehler: " << e.what() << "\n";
        }

        std::this_thread::sleep_for(std::chrono::seconds(INTERVAL));
    }

    return 0;
}

