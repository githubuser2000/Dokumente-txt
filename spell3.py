import sys
import string

# Wörterbücher für Deutsch und Englisch (kann beliebig erweitert werden)
woerterbuch = {
    "de": ["ich", "liebe", "programmieren", "und", "python", "korrigieren", "text", "ein", "beispiel"],
    "en": ["i", "love", "programming", "and", "python", "correct", "text", "an", "example"]
}

def levenshtein(a, b):
    """Berechnet die Levenshtein-Distanz zwischen zwei Wörtern."""
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0] = i
    for j in range(m+1): dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[n][m]

def korrektur(text, sprache="de"):
    korrigierter_text = []

    # Satzzeichen abtrennen
    translator = str.maketrans('', '', string.punctuation)
    woerter = text.split()

    for wort in woerter:
        wort_clean = wort.translate(translator).lower()  # Satzzeichen entfernen + lowercase
        if not wort_clean:  # z. B. nur Satzzeichen
            korrigierter_text.append(wort)
            continue

        # Bestes Wort im Wörterbuch suchen
        best_match = min(woerterbuch[sprache], key=lambda w: levenshtein(wort_clean, w))

        # Großschreibung des Originalwortes übernehmen
        if wort[0].isupper():
            best_match = best_match.capitalize()
        korrigierter_text.append(best_match)

    return " ".join(korrigierter_text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python korrektur.py <sprache: de/en> <text>")
        sys.exit(1)

    sprache = sys.argv[1]
    if sprache not in woerterbuch:
        print(f"Sprache '{sprache}' wird nicht unterstützt. Verwende 'de' oder 'en'.")
        sys.exit(1)

    text = " ".join(sys.argv[2:])
    korrigierter_text = korrektur(text, sprache)

    print("Original:   ", text)
    print("Korrigiert: ", korrigierter_text)

