#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// Beispiel: Syntax-Highlighting für C++
std::map<std::string, std::string> keywords = {
    {"int", "blue"}, {"float", "blue"}, {"double", "blue"},
    {"if", "purple"}, {"else", "purple"}, {"for", "purple"},
    {"while", "purple"}, {"return", "red"}
};

// Pseudocode für Rendering-Funktion
void renderLineToImage(const std::string& line, int y, unsigned char* img, int width, int height) {
    // Hier: Zeichen für Zeichen zeichnen, Farben je nach keyword/Kommentar/String
    // img ist ein RGB Array width*height*3
}

int main() {
    std::ifstream file("test.cpp");
    if (!file.is_open()) return 1;

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }

    int width = 800, height = 1200;
    unsigned char* image = new unsigned char[width * height * 3]();
    
    for (int i = 0; i < lines.size(); ++i) {
        renderLineToImage(lines[i], i*20, image, width, height); // 20px pro Zeile
    }

    stbi_write_png("output.png", width, height, 3, image, width*3);
    delete[] image;
    return 0;
}
