#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <random>
#include <tuple>
#include <string>

using namespace std;

// Primfaktorzerlegung
vector<int> primeFactors(int n) {
    vector<int> factors;
    for (int i = 2; i * i <= n; ++i) {
        while (n % i == 0) {
            factors.push_back(i);
            n /= i;
        }
    }
    if (n > 1) factors.push_back(n);
    return factors;
}

// Produkt aller Elemente
int productList(const vector<int>& v) {
    return accumulate(v.begin(), v.end(), 1, multiplies<int>());
}

// Größter gemeinsamer Teiler von drei Zahlen
int gcd3(int a, int b, int c) {
    return gcd(gcd(a, b), c);
}

// Kürzt einen Bruch
tuple<int,int> reduceFraction(int num, int den) {
    int g = gcd(num, den);
    return {num/g, den/g};
}

// Drei unterschiedliche Zahlen >1 mit gemeinsamen Primfaktor >=3
tuple<int,int,int,int> generateThreeUnique(int maxVal) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(3, maxVal);

    while (true) {
        int n1 = dis(gen);
        int n2 = dis(gen);
        int n3 = dis(gen);

        if (n1 == n2 || n1 == n3 || n2 == n3) continue;

        auto f1 = primeFactors(n1);
        auto f2 = primeFactors(n2);
        auto f3 = primeFactors(n3);

        int p1 = productList(f1);
        int p2 = productList(f2);
        int p3 = productList(f3);

        int common = gcd3(p1, p2, p3);

        vector<int> intersect;
        sort(f1.begin(), f1.end());
        sort(f2.begin(), f2.end());
        sort(f3.begin(), f3.end());
        set_intersection(f1.begin(), f1.end(), f2.begin(), f2.end(), back_inserter(intersect));
        vector<int> finalIntersect;
        set_intersection(intersect.begin(), intersect.end(), f3.begin(), f3.end(), back_inserter(finalIntersect));

        if (!finalIntersect.empty() && common >= 3) {
            return {p1, p2, p3, common};
        }
    }
}

// Bruch als String ausgeben
string showRational(int num, int den) {
    auto [rnum, rden] = reduceFraction(num, den);
    return to_string(rnum) + " / " + to_string(rden);
}

int main() {
    auto [n1, n2, n3, common] = generateThreeUnique(42);

    // Rationalzahlen
    int q1_num = n1, q1_den = n2; // q1 = n1/n2
    int q2_num = n2, q2_den = n3; // q2 = n2/n3

    // q3 = q1/q2 = (n1/n2)/(n2/n3) = (n1*n3)/(n2*n2)
    int q3_num = q1_num * q2_den;
    int q3_den = q1_den * q2_num;

    // q4 = q2/q1 = (n2/n3)/(n1/n2) = (n2*n2)/(n3*n1)
    int q4_num = q2_num * q1_den;
    int q4_den = q2_den * q1_num;

    vector<string> labels = {
        "Wert Geld Währung Nummer Zahlen Wert Währung (folgende sind Währungen von nicht Nummern Zahlen Werten)",
        "Gutartigkeit Selbstlosigkeit Führungschicht Regierung Herrschaft",
        "Ganzheit Kaputtheit Nicht-Armut Zentralität Unterschicht",
        "Primfaktor-Zerlegungs-Verwandschafts-Gemeinsamkeit dreier positiver zufälliger ganzer Natürlicher Zahlen Zahl",
        "Verhältnis Wert zu Führungsschicht, Gutartigkeit Produkt, Firma, Leistung als Winkel-Richtung",
        "Wert Verhältnis zu Unterschicht, Kaputtheit Armut Ganzheit Gesundheit zum Wert statt ins Verhältnis eine Skalierung",
        "Führungsschicht Regierer Parteien gegenüber Unterschicht Relation Verhältnis oder als Skarierung gemeint und zu verstehen, entweder oder",
        "Unterschicht Verhältnis zu Führungsschicht Regierung Herrscher Relation Verhältnis, oder als Skarierung gemeint und zu verstehen, entweder oder"
    };

    vector<string> values = {
        to_string(n1),
        to_string(n2),
        to_string(n3),
        to_string(common),
        showRational(q1_num, q1_den),
        showRational(q2_num, q2_den),
        showRational(q3_num, q3_den),
        showRational(q4_num, q4_den)
    };

    for (size_t i = 0; i < labels.size(); ++i) {
        cout << labels[i] << ": " << values[i] << endl;
    }

    return 0;
}
