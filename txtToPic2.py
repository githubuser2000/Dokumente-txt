#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
txtToPicHD.py - HD-Textbild, lesbare Outline, automatische Skalierung
"""

import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess

def find_system_font():
    """Systemweite Sans- oder Arial-ähnliche Font über fc-list finden"""
    try:
        output = subprocess.check_output(['fc-list', ':family'], text=True)
        lines = output.split('\n')
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
    base_outline = 1  # halbierte Outline
    base_max_chars = 40

    # Text einlesen
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    # Skalierung vorbereiten
    max_chars_per_line = int(base_max_chars * scale)

    # Zeilen umbrechen
    wrapped_text = textwrap.fill(text, width=max_chars_per_line)
    lines = wrapped_text.split('\n')

    # Bild erstellen
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Schrift laden
    font_path = find_system_font()
    font_size = 30  # Startgröße, wird automatisch angepasst
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        print("Warnung: Keine Systemfont gefunden, Fallback auf Default.")
        font = ImageFont.load_default()

    # Automatische Skalierung: Texthöhe an Bildhöhe anpassen
    while True:
        line_heights = [draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in lines]
        total_height = sum(line_heights) + 5 * len(lines)
        if total_height < img_height * 0.9:
            break
        font_size = max(1, font_size - 1)
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
        if font_size == 1:
            break

    # Outline-Radius
    outline_radius = max(1, int(base_outline * scale))

    # Zeilenhöhe
    line_height = max(draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] + 5 for line in lines)
    total_text_height = line_height * len(lines)
    y_start = (img_height - total_text_height) // 2

    # Text zeichnen mit feiner Outline
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img_width - text_width) // 2
        y = y_start + i * line_height

        # Outline nur 1 Pixel (halbiert)
        for dx in range(-outline_radius, outline_radius+1):
            for dy in range(-outline_radius, outline_radius+1):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, y+dy), line, font=font, fill='gray')
        draw.text((x, y), line, font=font, fill=text_color)

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

