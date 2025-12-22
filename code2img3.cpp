#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <iostream>
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// ====== Einstellungen ======
const int width = 800;
const int height = 1200;
const int lineHeight = 20;
const int linesPerPage = height / lineHeight;

std::vector<std::string> keywords = {
    "int","float","double","if","else","for","while","return","void","class","struct"
};

// Farben
SDL_Color keywordColor   = {0, 0, 255, 255};
SDL_Color commentColor   = {0, 150, 0, 255};
SDL_Color stringColor    = {255, 140, 0, 255};
SDL_Color normalColor    = {0, 0, 0, 255};
SDL_Color bgColor        = {255, 255, 255, 255};

// ====== Hilfsfunktionen ======
bool isKeyword(const std::string& word) {
    for (auto& k : keywords) if (word == k) return true;
    return false;
}

void renderLine(SDL_Renderer* renderer, TTF_Font* font, const std::string& line, int y) {
    int x = 0;
    std::regex wordRegex(R"(\w+|.)");
    std::sregex_iterator it(line.begin(), line.end(), wordRegex);
    std::sregex_iterator end;

    bool inString = false;
    for (; it != end; ++it) {
        std::string token = it->str();
        SDL_Color color = normalColor;

        if (token == "\"" || token == "'") inString = !inString;

        if (inString) color = stringColor;
        else if (token.rfind("//", 0) == 0) color = commentColor;
        else if (isKeyword(token)) color = keywordColor;

        SDL_Surface* surf = TTF_RenderText_Blended(font, token.c_str(), color);
        SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer, surf);

        int w, h;
        SDL_QueryTexture(tex, nullptr, nullptr, &w, &h);
        SDL_Rect dst = {x, y, w, h};
        SDL_RenderCopy(renderer, tex, nullptr, &dst);
        x += w;

        SDL_DestroyTexture(tex);
        SDL_FreeSurface(surf);

        if (token.rfind("//", 0) == 0) break;
    }
}

// ====== Hauptprogramm ======
int main() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) return 1;
    if (TTF_Init() < 0) return 1;

    TTF_Font* font = TTF_OpenFont("DejaVuSansMono.ttf", 18);
    if (!font) {
        std::cerr << "Font nicht gefunden!\n";
        return 1;
    }

    std::ifstream file("econ678cpp2.cpp");
    if (!file.is_open()) {
        std::cerr << "Datei nicht gefunden!\n";
        return 1;
    }

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) lines.push_back(line);

    int page = 0;
    for (size_t startLine = 0; startLine < lines.size(); startLine += linesPerPage) {
        SDL_Window* window = SDL_CreateWindow("Code Renderer", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_HIDDEN);
        SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
        SDL_Texture* target = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, width, height);

        SDL_SetRenderTarget(renderer, target);
        SDL_SetRenderDrawColor(renderer, bgColor.r, bgColor.g, bgColor.b, bgColor.a);
        SDL_RenderClear(renderer);

        int y = 0;
        for (size_t i = startLine; i < startLine + linesPerPage && i < lines.size(); ++i) {
            renderLine(renderer, font, lines[i], y);
            y += lineHeight;
        }

        SDL_SetRenderTarget(renderer, nullptr);

        std::vector<unsigned char> pixels(width * height * 4);
        SDL_SetRenderTarget(renderer, target);
        SDL_RenderReadPixels(renderer, nullptr, SDL_PIXELFORMAT_RGBA8888, pixels.data(), width * 4);

        std::string filename = "output_" + std::to_string(page) + ".png";
        stbi_write_png(filename.c_str(), width, height, 4, pixels.data(), width * 4);
        std::cout << "Bild erstellt: " << filename << "\n";
        page++;

        SDL_DestroyTexture(target);
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
    }

    TTF_CloseFont(font);
    TTF_Quit();
    SDL_Quit();

    return 0;
}
