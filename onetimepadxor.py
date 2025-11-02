import os

# Nachricht und zufälliger Schlüssel
msg = b"Hallo Welt"
key = os.urandom(len(msg))

# XOR-Verschlüsselung
cipher = bytes([m ^ k for m, k in zip(msg, key)])

# Entschlüsselung
plain = bytes([c ^ k for c, k in zip(cipher, key)])

print("Nachricht:", msg)
print("Schlüssel:", key.hex())
print("Cipher  :", cipher.hex())
print("Klartext:", plain)

