# -*- coding: utf-8 -*-
import sys
from textblob import TextBlob

# Wörterbücher für Deutsch und Englisch
woerterbuch = {
    "de": ["ich", "liebe", "programmieren", "und", "python", "korrigieren", "text"],
    "en": ["i", "love", "programming", "and", "python", "correct", "text"]
}

def korrektur(text, sprache="de"):
    """
    Korrigiert kleine Tippfehler in einem Text basierend auf der Sprache.
    """
    textblob = TextBlob(text)
    korrigierter_text = []

    for wort in textblob.words:
        # Versuche mit TextBlob zu korrigieren
        wort_korrigiert = str(TextBlob(wort).correct())

        # Wörterbuch-Prüfung: Falls das korrigierte Wort nicht im Wörterbuch, nehme Original
        if wort_korrigiert.lower() in woerterbuch[sprache]:
            korrigierter_text.append(wort_korrigiert)
        else:
            korrigierter_text.append(wort)

    return " ".join(korrigierter_text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python korrektur.py <sprache: de/en> <text>")
        sys.exit(1)

    sprache = sys.argv[1]
    text = " ".join(sys.argv[2:])

    korrigierter_text = korrektur(text, sprache)
    print("Original:   ", text)
    print("Korrigiert: ", korrigierter_text)

