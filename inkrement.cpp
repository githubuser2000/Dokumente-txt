#include <iostream>
#include <string>
#include <regex>
#include <map>

int main() {
    std::string line;
    std::regex re(R"(^(\d{4}))");
    std::smatch match;
    std::string start_val = "";
    int count = 0;
    std::map<std::string, int> val_counter;

    while (std::getline(std::cin, line)) {
        if (std::regex_search(line, match, re)) {
            std::string num = match[1];
            if (start_val.empty()) {
                start_val = num;
            }
            count++;
            std::string prefix = num.substr(0, 2);
            val_counter[prefix]++;
            std::cout << "Zeile " << count << ": Start=" << start_val << ", Aktuelle=" << num
                      << ", Gruppe=" << prefix << ", Vorkommen=" << val_counter[prefix] << "\n";
        }
    }

    return 0;
}

