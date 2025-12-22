#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
txtToPicHD.py - robust auf Fedora/Linux
"""

import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess

def find_system_font():
    """Versucht, eine verfügbare Sans/Arial-ähnliche Font über fc-list zu finden"""
    try:
        output = subprocess.check_output(['fc-list', ':family'], text=True)
        lines = output.split('\n')
        # Suche nach DejaVu, Liberation oder FreeSans
        for line in lines:
            if any(name in line for name in ['DejaVu Sans', 'Liberation Sans', 'FreeSans']):
                font_name = line.split(':')[0].strip()
                return font_name
    except Exception:
        pass
    return None

def text_to_hd_image(text_file, image_file, scale=1.0):
    img_width, img_height = 1920, 1080
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    base_font_size = 30
    base_thickness = 2

    font_size = max(1, int(base_font_size * scale))
    thickness = max(1, int(base_thickness * scale))
    max_chars_per_line = int(40 * scale)

    # Text einlesen
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    # Text umbrechen
    wrapped_text = textwrap.fill(text, width=max_chars_per_line)
    lines = wrapped_text.split('\n')

    # Bild erstellen
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Schrift laden
    font_path = find_system_font()
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            print("Warnung: Systemfont kann nicht geladen werden, Fallback auf Default.")
            font = ImageFont.load_default()
    else:
        print("Warnung: Keine Systemfont gefunden, Fallback auf Default.")
        font = ImageFont.load_default()

    # Höhe aller Zeilen berechnen
    line_height = max(draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] + 5 for line in lines)
    total_text_height = line_height * len(lines)

    # Y-Startpunkt zentriert
    y_start = (img_height - total_text_height) // 2

    # Zeilen zeichnen mit Outline
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img_width - text_width) // 2
        y = y_start + i * line_height

        # Outline: 1 Pixel
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, y+dy), line, font=font, fill='gray')
        # Haupttext
        draw.text((x, y), line, font=font, fill=text_color)

    # Bild speichern
    img.save(image_file)
    print(f"Bild erstellt: {image_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python3 txtToPicHD.py textdatei.txt bilddatei.png [skalierungsfaktor]")
        sys.exit(1)

    text_file = sys.argv[1]
    image_file = sys.argv[2]
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    text_to_hd_image(text_file, image_file, scale)

