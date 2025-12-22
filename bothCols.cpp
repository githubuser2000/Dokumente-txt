#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <iomanip>
#include <algorithm>
#include <sys/ioctl.h>
#include <unistd.h>

int get_terminal_width() {
    struct winsize w;
    if(ioctl(STDOUT_FILENO, TIOCGWINSZ, &w) == -1) return 80;
    return w.ws_col;
}

std::vector<std::string> wrap_text(const std::string &s, size_t width) {
    std::vector<std::string> lines;
    for(size_t i = 0; i < s.size(); i += width) {
        lines.push_back(s.substr(i, width));
    }
    if(lines.empty()) lines.push_back("");
    return lines;
}

int main(int argc, char* argv[]) {
    if(argc != 5) {
        std::cerr << "Usage: " << argv[0] << " file1.csv file2.csv col1 col2\n";
        return 1;
    }

    std::ifstream file1(argv[1]), file2(argv[2]);
    if(!file1 || !file2) { std::cerr << "Error opening files\n"; return 1; }

    int col1 = std::stoi(argv[3]);
    int col2 = std::stoi(argv[4]);

    std::vector<std::string> column1, column2;
    std::string line;

    while(std::getline(file1, line)) {
        std::stringstream ss(line);
        std::string cell;
        int i = 0;
        while(std::getline(ss, cell, ',')) {
            if(i == col1) column1.push_back(cell);
            ++i;
        }
    }

    while(std::getline(file2, line)) {
        std::stringstream ss(line);
        std::string cell;
        int i = 0;
        while(std::getline(ss, cell, ',')) {
            if(i == col2) column2.push_back(cell);
            ++i;
        }
    }

    size_t size = std::max(column1.size(), column2.size());
    column1.resize(size, "");
    column2.resize(size, "");

    int term_width = get_terminal_width();

    const size_t width_num = 4; // Zeilennummer immer 4-stellig
    size_t width1 = 0, width2 = 0;
    for(auto &s : column1) width1 = std::max(width1, s.size());
    for(auto &s : column2) width2 = std::max(width2, s.size());

    if(width_num + 3 + width1 + 3 + width2 > term_width) {
        double ratio = double(term_width - 6) / (width_num + width1 + width2);
        width1 = std::max<size_t>(1, width1 * ratio);
        width2 = std::max<size_t>(1, width2 * ratio);
    }

    for(size_t i = 0; i < size; ++i) {
        std::string num_str;
        if(i + 1 == 0) { // Zeilennummer 0000 -> vier Leerzeichen
            num_str = "    ";
        } else {
            std::stringstream num_ss;
            num_ss << std::setw(4) << std::setfill('0') << (i + 1);
            num_str = num_ss.str();
        }

        std::vector<std::string> lines_num = wrap_text(num_str, width_num);
        std::vector<std::string> lines1 = wrap_text(column1[i], width1);
        std::vector<std::string> lines2 = wrap_text(column2[i], width2);

        size_t lines = std::max({lines_num.size(), lines1.size(), lines2.size()});
        lines_num.resize(lines, "");
        lines1.resize(lines, "");
        lines2.resize(lines, "");

        for(size_t j = 0; j < lines; ++j) {
            std::cout << std::left << std::setw(width_num) << std::setfill(' ') << lines_num[j] << " | "
                      << std::left << std::setw(width1) << std::setfill(' ') << lines1[j] << " | "
                      << std::left << std::setw(width2) << std::setfill(' ') << lines2[j] << "\n";
        }
    }

    return 0;
}
