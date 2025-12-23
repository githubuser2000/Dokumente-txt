#include <iostream>
#include <vector>
#include <set>
#include <functional>

// ----------------------
// Typdefinitionen T-CORE
// ----------------------
using IntSeq = std::vector<int>;
using IntSet = std::set<int>;

// ----------------------
// State-Definition
// ----------------------
struct State {
    IntSeq nums;
    IntSet selected;
};

// ----------------------
// Toggle-Funktion (T-CORE / M-FLOW)
// ----------------------
void ToggleSelection(State &S) {
    for (int v : S.nums) {
        if (S.selected.count(v)) S.selected.erase(v);
        else S.selected.insert(v);
    }
}

// ----------------------
// Pipeline / Regeln
// ----------------------
void EmitToggle(State &S, int v) {
    if (S.selected.count(v)) S.selected.erase(v);
    else S.selected.insert(v);
}

// Beispiel: generische Schleifenregel
void ForEach(IntSeq &seq, std::function<void(int)> body) {
    for (int v : seq)
        body(v);
}

// ----------------------
// Main / ECO-L Layer
// ----------------------
int main() {
    // Initialzustand
    State S;
    S.nums = {1, 2, 3, 2, 4};

    // Pipeline-Aufruf
    ToggleSelection(S);

    // Ausgabe
    std::cout << "{ ";
    for (int v : S.selected)
        std::cout << v << " ";
    std::cout << "}" << std::endl;

    return 0;
}
