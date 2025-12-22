#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
txtToPicHD_multi.py - HD-Textbild mit Rand, lesbarer Outline, automatischer Skalierung,
automatischer Mehrbild-Erzeugung bei zu langem Text und optionalem Bildformat.
"""

import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess
import os

def find_system_font():
    """Systemweite Sans- oder Arial-ähnliche Font über fc-list finden"""
    try:
        output = subprocess.check_output(['fc-list', ':family'], text=True)
        lines = output.split('\n')
        for line in lines:
            if any(name in line for name in ['DejaVu Sans', 'Liberation Sans', 'FreeSans']):
                return line.split(':')[0].strip()
    except Exception:
        pass
    return None

def text_to_hd_images(text_file, image_file, scale=1.0, fmt=None):
    img_width, img_height = 1060, 1080
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    base_outline = 1
    base_max_chars = 40
    base_line_spacing = 10

    margin_x = 25
    margin_y = 25

    # Text einlesen
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    max_chars_per_line = int(base_max_chars * scale)

    # Umbruch vorbereiten
    wrapped_text = textwrap.fill(text, width=max_chars_per_line)
    all_lines = wrapped_text.split('\n')

    # Temp-Bild zum Messen
    tmp_img = Image.new("RGB", (img_width, img_height))
    tmp_draw = ImageDraw.Draw(tmp_img)

    font_path = find_system_font()
    font_size = 30
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        print("Warnung: Keine Systemfont gefunden, Fallback auf Default.")
        font = ImageFont.load_default()

    # Automatische Schriftgrößenanpassung
    while True:
        line_heights = [(tmp_draw.textbbox((0,0), line, font=font)[3] -
                         tmp_draw.textbbox((0,0), line, font=font)[1] +
                         base_line_spacing)
                        for line in all_lines]

        total_height = sum(line_heights)

        max_line_width = max(
            tmp_draw.textbbox((0,0), line, font=font)[2] -
            tmp_draw.textbbox((0,0), line, font=font)[0]
            for line in all_lines
        )

        if (total_height < (img_height - 2*margin_y)
            and max_line_width < (img_width - 2*margin_x)):
            break

        font_size -= 1
        if font_size < 1:
            break

        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

    outline_radius = max(1, int(base_outline * scale))

    # Jetzt in mehrere Seiten aufteilen (Chunking)
    chunks = []
    current = []
    current_height = 0

    for line in all_lines:
        lh = (tmp_draw.textbbox((0,0), line, font=font)[3] -
              tmp_draw.textbbox((0,0), line, font=font)[1] +
              base_line_spacing)

        if current_height + lh > (img_height - 2*margin_y):
            chunks.append(current)
            current = [line]
            current_height = lh
        else:
            current.append(line)
            current_height += lh

    if current:
        chunks.append(current)

    # Ausgabeformat ermitteln
    if fmt is None:
        _, ext = os.path.splitext(image_file)
        fmt = ext.replace(".", "").lower()
        if fmt == "":
            fmt = "png"  # Standard

    # Für jede Seite ein Bild erzeugen
    for i, lines in enumerate(chunks, start=1):
        img = Image.new("RGB", (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)

        line_height = max(
            (draw.textbbox((0,0), line, font=font)[3] -
             draw.textbbox((0,0), line, font=font)[1] +
             base_line_spacing)
            for line in lines
        )

        total_text_height = line_height * len(lines)
        y_start = margin_y + ((img_height - 2*margin_y - total_text_height)//2)

        for idx, line in enumerate(lines):
            bbox = draw.textbbox((0,0), line, font=font)
            text_width = bbox[2] - bbox[0]

            x = margin_x + ((img_width - 2*margin_x - text_width)//2)
            y = y_start + idx * line_height

            # Outline
            for dx in range(-outline_radius, outline_radius+1):
                for dy in range(-outline_radius, outline_radius+1):
                    if dx or dy:
                        draw.text((x+dx, y+dy), line, font=font, fill='gray')

            draw.text((x, y), line, font=font, fill=text_color)

        # neue Dateinamen
        if len(chunks) == 1:
            outfile = image_file
        else:
            base, ext = os.path.splitext(image_file)
            outfile = f"{base}_{i}.{fmt}"

        img.save(outfile, format=fmt.upper())
        print(f"Bild erstellt: {outfile}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python3 txtToPicHD_multi.py text.txt bild.png [scale] [format]")
        sys.exit(1)

    text_file = sys.argv[1]
    image_file = sys.argv[2]
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    fmt = sys.argv[4] if len(sys.argv) > 4 else None

    text_to_hd_images(text_file, image_file, scale, fmt)

