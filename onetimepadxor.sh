#!/usr/bin/env bash
msg="Hallo Welt"

# Schlüssel gleicher Länge, zufällig aus /dev/urandom
key=$(head -c ${#msg} /dev/urandom)

# XOR-Verschlüsselung
cipher=""
for ((i=0; i<${#msg}; i++)); do
  m=$(printf "%d" "'${msg:$i:1}")
  k=$(printf "%d" "'${key:$i:1}")
  c=$((m ^ k))
  cipher+=$(printf "\\x%02x" "$c")
done

echo "Nachricht: $msg"
echo "Schlüssel (hex):" "$(echo -n "$key" | xxd -p)"
echo "Cipher   (hex):"  "$(echo -n -e "$cipher" | xxd -p)"

# Entschlüsselung (XOR nochmal)
plain=""
for ((i=0; i<${#msg}; i++)); do
  c=$(printf "%d" "'$(echo -n -e "$cipher" | cut -b $((i+1)))")
  k=$(printf "%d" "'${key:$i:1}")
  p=$((c ^ k))
  plain+=$(printf "\\x%02x" "$p")
done

echo "Entschlüsselt:" "$(echo -n -e "$plain")"

