# ==========================================
# Run-Length Encoding (RLE)
# Encoder & Decoder in Python
# ==========================================

def rle_encode(data: str) -> str:
    """Kodiert eine Zeichenkette mit Run-Length-Encoding (RLE)."""
    if not data:
        return ""
    encoded = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded.append(f"{data[i - 1]}{count}")
            count = 1
    # letztes Token anhängen
    encoded.append(f"{data[-1]}{count}")
    return "".join(encoded)


def rle_decode(encoded: str) -> str:
    """Dekodiert eine mit RLE komprimierte Zeichenkette."""
    if not encoded:
        return ""
    decoded = []
    symbol = ""
    count = ""
    for char in encoded:
        if char.isdigit():
            count += char
        else:
            # falls vorher ein Symbol+Zahl fertig war
            if symbol and count:
                decoded.append(symbol * int(count))
                count = ""
            symbol = char
    # letztes Symbol ausgeben
    if symbol and count:
        decoded.append(symbol * int(count))
    return "".join(decoded)


# ==========================================
# Beispiel
# ==========================================
if __name__ == "__main__":
    text = "AAAAABBBBCCCCCCDD"
    encoded = rle_encode(text)
    decoded = rle_decode(encoded)

    print("Original :", text)
    print("Kodiert  :", encoded)
    print("Dekodiert:", decoded)
    print("Korrekt? ", decoded == text)

