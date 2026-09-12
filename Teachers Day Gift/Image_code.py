"""
Teacher's Day — prints Devesh Sir's photo as ASCII art right in the terminal.

Usage:
    python teacher_day_terminal.py
    python teacher_day_terminal.py --file my_photo.jpg
    python teacher_day_terminal.py --width 60 --blocks
    python teacher_day_terminal.py --plain
"""

import argparse
import io
import math
import random
import re
import shutil
import sys
import time

from PIL import Image, ImageOps
import requests

# GitHub avatar for github.com/deveshpatwa
DEFAULT_IMAGE_URL = "https://avatars.githubusercontent.com/u/119609993?v=4"

# Characters ordered from "empty" to "dense" — used when --no-color is passed.
RAMP = "@%#*+=-:. "

# Terminal character cells are roughly twice as tall as they are wide,
# so we shrink the height to keep the picture looking proportional.
CHAR_ASPECT = 0.55

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))


def load_image(path: str = None, url: str = None) -> Image.Image:
    if path:
        return Image.open(path).convert("RGB")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGB")


def resize_for_terminal(img: Image.Image, width: int) -> Image.Image:
    w, h = img.size
    new_h = max(1, int(width * (h / w) * CHAR_ASPECT))
    return img.resize((width, new_h), Image.LANCZOS)


def prep_grayscale(img: Image.Image) -> Image.Image:
    """Grayscale with contrast stretched to the full range. Avatars are often
    low-contrast (dark hair close in tone to a dark background), which is what
    makes hair disappear into empty space in the ASCII output — this pulls
    those tones apart so hair, skin, and background map to distinct characters."""
    gray = img.convert("L")
    return ImageOps.autocontrast(gray, cutoff=1)


def render_blocks(img: Image.Image) -> str:
    """Solid colored block per pixel — looks like a tiny photo, no shading detail."""
    pixels = img.load()
    w, h = img.size
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = pixels[x, y]
            row.append(f"\x1b[38;2;{r};{g};{b}m█\x1b[0m")
        lines.append("".join(row))
    return "\n".join(lines)


def render_color_ascii(img: Image.Image) -> str:
    """Density characters (shading + edges) printed in each pixel's true color."""
    gray = prep_grayscale(img)
    pixels_gray = gray.load()
    pixels_rgb = img.load()
    w, h = img.size
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            brightness = pixels_gray[x, y] / 255
            index = int(brightness * (len(RAMP) - 1))
            char = RAMP[index]
            r, g, b = pixels_rgb[x, y]
            row.append(f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m")
        lines.append("".join(row))
    return "\n".join(lines)


def render_ascii(img: Image.Image) -> str:
    """Plain ASCII characters, printed in the terminal's own default color —
    no forced white, no background styling, just the characters themselves."""
    gray = prep_grayscale(img)
    pixels = gray.load()
    w, h = gray.size
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            brightness = pixels[x, y] / 255
            index = int(brightness * (len(RAMP) - 1))
            row.append(RAMP[index])
        lines.append("".join(row))
    return "\n".join(lines)


def frame(art: str) -> str:
    """Wrap the art in a simple border so it reads as one clean piece, not loose text."""
    lines = art.split("\n")
    width = visible_len(lines[0])
    top = "┌" + "─" * width + "┐"
    bottom = "└" + "─" * width + "┘"
    boxed = [top]
    for line in lines:
        boxed.append("│" + line + "│")
    boxed.append(bottom)
    return "\n".join(boxed)


def safe_width(requested: int) -> int:
    """Cap the output so every row fits on one terminal line — a too-wide image
    wraps mid-row and makes the picture and its frame look broken/cut off."""
    columns = shutil.get_terminal_size(fallback=(80, 24)).columns
    max_width = max(20, columns - 4)  # leave room for the 2-char frame border
    return min(requested, max_width)


def print_message():
    gold = "\x1b[38;2;231;184;76m"
    reset = "\x1b[0m"
    print(f"\n{gold}Happy Teacher's Day, Devesh Sir!{reset}")
    print(
        "Thank you for turning confusing datasets into clear stories, "
        "and confused students into confident ones. We're grateful for "
        "your patience, your teaching, and your time.\n"
    )


# --- page 2: an animated "Happy Teacher's Day" banner --------------------

# A small 5-row block font, just for the letters this banner needs.
FONT = {
    "A": ["  #  ", " # # ", "#####", "#   #", "#   #"],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#####", "#    ", "#####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    " ": ["   ", "   ", "   ", "   ", "   "],
}

RAINBOW = [
    (230, 57, 70), (244, 162, 97), (233, 196, 106),
    (42, 157, 143), (129, 178, 154), (157, 78, 221),
]


def big_text(phrase: str) -> list:
    """Render a phrase (letters this FONT knows, plus spaces) as 5 banner lines."""
    rows = ["", "", "", "", ""]
    for ch in phrase.upper():
        glyph = FONT.get(ch, FONT[" "])
        for i in range(5):
            rows[i] += glyph[i] + " "
    return rows


def clear_screen():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def colorize(text: str, rgb: tuple) -> str:
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}\x1b[0m"


def play_fireworks(width: int, height: int = 16, frames: int = 55):
    """A small real-time particle simulation: rockets launch from the bottom,
    rise, and burst into radiating sparks that fall and fade — actual physics
    (position, velocity, gravity), not a canned animation."""
    rockets = []
    particles = []

    for frame_i in range(frames):
        # occasionally launch a new rocket, but don't let the sky get too busy
        if random.random() < 0.22 and len(rockets) < 3:
            rockets.append({
                "x": random.uniform(6, width - 6),
                "y": float(height - 1),
                "target_y": random.uniform(2, height * 0.5),
                "color": random.choice(RAINBOW),
            })

        # rockets rise; on reaching their target height they burst into particles
        still_rockets = []
        for r in rockets:
            r["y"] -= 1.1
            if r["y"] <= r["target_y"]:
                color = random.choice(RAINBOW)
                count = random.randint(16, 24)
                for i in range(count):
                    angle = (2 * math.pi * i / count) + random.uniform(-0.15, 0.15)
                    speed = random.uniform(0.7, 1.5)
                    particles.append({
                        "x": r["x"], "y": r["y"],
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed * 0.6,
                        "life": random.randint(7, 11),
                        "max_life": 11,
                        "color": color,
                    })
            else:
                still_rockets.append(r)
        rockets = still_rockets

        # particles fall under gravity and fade out over their lifetime
        still_particles = []
        for p in particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.09
            p["life"] -= 1
            if p["life"] > 0 and 0 <= p["x"] < width and 0 <= p["y"] < height:
                still_particles.append(p)
        particles = still_particles

        # render this frame
        grid = [[None] * width for _ in range(height)]
        for r in rockets:
            xi, yi = int(r["x"]), int(r["y"])
            if 0 <= yi < height and 0 <= xi < width:
                grid[yi][xi] = ("|", r["color"])
        for p in particles:
            xi, yi = int(p["x"]), int(p["y"])
            if 0 <= yi < height and 0 <= xi < width:
                ratio = p["life"] / p["max_life"]
                char = "*" if ratio > 0.66 else ("+" if ratio > 0.33 else ".")
                grid[yi][xi] = (char, p["color"])

        clear_screen()
        lines = []
        for row in grid:
            parts = [colorize(ch, col) if cell else " " for cell in row for ch, col in [cell or (" ", (0, 0, 0))]]
            lines.append("".join(parts))
        print("\n".join(lines))
        sys.stdout.flush()

        if frame_i > frames - 12 and not rockets and not particles:
            break  # sky's clear, no need to burn through the remaining frames

        time.sleep(0.06)


def play_next_page():
    """The second page: a real fireworks show, then the Happy Teacher's Day banner."""
    banner = big_text("HAPPY TEACHERS DAY")
    width = max(len(row) for row in banner) + 4

    play_fireworks(width=width, height=16)

    clear_screen()
    for i, row in enumerate(banner):
        print(colorize(row, RAINBOW[i % len(RAINBOW)]))
        time.sleep(0.2)

    print()
    print(colorize("     -- from all of us, with gratitude --", (231, 184, 76)))
    print()
    print(colorize("Wishing Devesh Sir a joyful Teacher's Day!", (129, 178, 154)))
    print()


def main():
    parser = argparse.ArgumentParser(description="Print a photo as ASCII art in the terminal.")
    parser.add_argument("--file", help="Path to a local image file (skips the download).")
    parser.add_argument("--url", default=DEFAULT_IMAGE_URL, help="Image URL to download.")
    parser.add_argument("--width", type=int, default=100, help="Output width in characters.")
    parser.add_argument("--color-dots", action="store_true", help="Same ASCII characters, but printed in true color.")
    parser.add_argument("--blocks", action="store_true", help="Solid color blocks instead of ASCII characters — looks more like the real photo.")
    args = parser.parse_args()

    try:
        img = load_image(path=args.file, url=args.url)
    except Exception as e:
        print(f"Couldn't load the image: {e}", file=sys.stderr)
        sys.exit(1)

    width = safe_width(args.width)
    img = resize_for_terminal(img, width)

    if args.blocks:
        art = render_blocks(img)
    elif args.color_dots:
        art = render_color_ascii(img)
    else:
        art = render_ascii(img)

    print()
    print(frame(art))
    print_message()

    try:
        input(colorize("Press Enter to see the next page...", (159, 176, 184)))
    except (EOFError, KeyboardInterrupt):
        return

    play_next_page()


if __name__ == "__main__":
    main()