#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#include <iostream>

// Keywords für einfaches Highlighting
std::vector<std::string> keywords = {
    "int","float","double","if","else","for","while","return","void","class","struct"
};

// Farben für Highlighting (RGB)
SDL_Color keywordColor   = {0, 0, 255, 255};
SDL_Color commentColor   = {0, 150, 0, 255};
SDL_Color stringColor    = {255, 140, 0, 255};
SDL_Color normalColor    = {0, 0, 0, 255};
SDL_Color bgColor        = {255, 255, 255, 255};

// Prüft, ob Wort ein Keyword ist
bool isKeyword(const std::string& word) {
    for (auto& k : keywords) if (word == k) return true;
    return false;
}

// Funktion, um Text zu rendern
void renderText(SDL_Renderer* renderer, TTF_Font* font, const std::string& line, int y) {
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

        // Kommentar bis Ende der Zeile
        if (token.rfind("//", 0) == 0) break;
    }
}

int main() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) return 1;
    if (TTF_Init() < 0) return 1;

    const int width = 800, height = 1200;
    SDL_Window* window = SDL_CreateWindow("Code Renderer", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_HIDDEN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    TTF_Font* font = TTF_OpenFont("DejaVuSansMono.ttf", 18);
    if (!font) return 1;

    std::ifstream file("test.cpp");
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) lines.push_back(line);

    // Render-Target vorbereiten
    SDL_Texture* target = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, width, height);
    SDL_SetRenderTarget(renderer, target);
    SDL_SetRenderDrawColor(renderer, bgColor.r, bgColor.g, bgColor.b, bgColor.a);
    SDL_RenderClear(renderer);

    int y = 0;
    for (auto& l : lines) {
        renderText(renderer, font, l, y);
        y += 20; // Zeilenhöhe
        if (y + 20 > height) break; // hier optional mehrere Bilder erstellen
    }

    SDL_SetRenderTarget(renderer, nullptr);

    // Pixel auslesen
    std::vector<unsigned char> pixels(width * height * 4);
    SDL_SetRenderTarget(renderer, target);
    SDL_RenderReadPixels(renderer, nullptr, SDL_PIXELFORMAT_RGBA8888, pixels.data(), width * 4);

    stbi_write_png("output.png", width, height, 4, pixels.data(), width * 4);

    // Cleanup
    SDL_DestroyTexture(target);
    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();

    std::cout << "Bild erstellt: output.png\n";
    return 0;
}
