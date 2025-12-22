#include <iostream>
#include <vector>
#include <array>
#include <random>
#include <cmath>
#include <iostream>

struct Rational {
    int num;
    int den;

    double toDouble() const {
        return static_cast<double>(num) / static_cast<double>(den);
    }
};

using Space = std::array<int,6>;

// Zufalls-Engine
std::mt19937 rng(std::random_device{}());

int randInt(int a, int b) {
    std::uniform_int_distribution<int> dist(a,b);
    return dist(rng);
}

// zufällige Länge, 3¿20
int randomLength() {
    return randInt(3,20);
}

// zufälliges Rational oder Int
Rational randomRational() {
    int choose = randInt(0,1);
    if (choose == 0) {
        // Fraction
        int n = randInt(1,9);
        int d = randInt(1,9);
        return {n,d};
    } else {
        // Int
        int x = randInt(1,20);
        return {x,1};
    }
}

// zufällige Liste
std::vector<Rational> randomFractionList() {
    int len = randomLength();
    std::vector<Rational> v;
    v.reserve(len);
    for (int i=0; i<len; i++)
        v.push_back(randomRational());
    return v;
}

std::pair<int,int> convertOne(const Rational& r) {
    int val = static_cast<int>(std::floor(r.toDouble() * 10.0));
    int minv = val;
    int maxv = std::max(val * 2, val);
    return {minv,maxv};
}

Space fractionTripletToSpace(const Rational& a,
                             const Rational& b,
                             const Rational& c)
{
    auto [a1,a2] = convertOne(a);
    auto [b1,b2] = convertOne(b);
    auto [c1,c2] = convertOne(c);
    return {a1,a2, b1,b2, c1,c2};
}

std::vector<Space> fractionsToSpaces(const std::vector<Rational>& v) {
    std::vector<Space> out;
    for (size_t i=0; i+2 < v.size(); i+=3) {
        out.push_back(fractionTripletToSpace(v[i], v[i+1], v[i+2]));
    }
    return out;
}
void endtext1()
{
    int n = 3;

    std::cout << "\n";
    std::cout << "==============================================\n";
    std::cout << "[INT]  GANZZAHL - Zustand im dimensionalen Raum\n";
    std::cout << "==============================================\n";
    std::cout << "Value: n = " << n << "\n\n";

    std::cout << "Meaning:\n";
    std::cout << "  (1) Market Economy\n";
    std::cout << "      -> absolute drive / value state\n\n";

    std::cout << "  (2) Currency\n";
    std::cout << "      -> isolated currency\n";
    std::cout << "      -> no exchange ratio\n\n";

    std::cout << "  (3) Communism States\n";
    std::cout << "      * poverty\n";
    std::cout << "      * repair state\n";
    std::cout << "      * health / illness\n";
    std::cout << "      * weakness / centrality / impulsivity\n\n";

    std::cout << "  (4) Geometry\n";
    std::cout << "      -> volume or area unit\n\n";

    std::cout << "  (5) Hierarchy\n";
    std::cout << "      -> rank (top / bottom)\n";
    std::cout << "==============================================\n";
}

void endtext2()
{
    int a = 2;
    int b = 5;
    double r = static_cast<double>(a) / b;

    std::cout << "\n";
    std::cout << "==============================================\n";
    std::cout << "[RAT]  RATIONAL NUMBER - Relation in space\n";
    std::cout << "==============================================\n";
    std::cout << "Value: r = " << a << "/" << b << " = " << r << "\n\n";

    std::cout << "Meaning:\n";
    std::cout << "  (1) Currencies\n";
    std::cout << "      -> exchange ratio\n\n";

    std::cout << "  (2) Geometry (2D)\n";
    std::cout << "      -> direction / slope\n\n";

    std::cout << "  (3) Diplomacy\n";
    std::cout << "      -> power / influence relation\n\n";

    std::cout << "  (4) Social System\n";
    std::cout << "      -> who with whom\n";
    std::cout << "      -> relation structure\n";
    std::cout << "Tradeable: Tickets, real estate, movable as cars, property, land, animals, people humans, spaceships, ferries, alloys, and houses can be traded using blocks currency instead of currency, based on numerical values, as currency for NATO and Warsaw Pact organizations.\n";
    std::cout << "==============================================\n";
}
void out() {
  auto xs = randomFractionList();

    std::cout << "Liste:\n";
    for (auto& r : xs)
        std::cout << r.num << "/" << r.den << " ";
    std::cout << "\n\nSpaces:\n";

    auto spaces = fractionsToSpaces(xs);
    for (auto& s : spaces)
        std::cout << "("
                  << s[0] << "," << s[1] << "; "
                  << s[2] << "," << s[3] << "; "
                  << s[4] << "," << s[5] << ")\n";
   
}

int main() {
     out();
     endtext1();
     endtext2();
     out();
}




