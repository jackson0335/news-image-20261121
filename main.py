"""Generate a one-page infographic summarising world news of
Saturday 21 November 2026.

Usage:
    pip install Pillow
    python generate.py

Writes exactly one image, output.png (1600 x 1200), next to this file.
The program is deterministic: no randomness, no current time, no network
access and no external files. All text is embedded below.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1600, 1200
OUTPUT = Path(__file__).resolve().parent / "output.png"

# Colours
NAVY = (15, 42, 68)
NAVY_LIGHT = (27, 68, 104)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (24, 30, 38)
MUTED = (84, 94, 108)
GOLD = (214, 164, 32)

STORIES = [
    (
        "CLIMATE",
        (14, 122, 106),
        "Climate talks run into overtime in Antalya",
        "Negotiators missed the Friday deadline as a draft text dropped "
        "any mention of phasing out fossil fuels, leaving the COP31 "
        "summit at risk of failure.",
    ),
    (
        "MIDDLE EAST",
        (178, 58, 48),
        "Houthi missiles intercepted over Saudi Arabia",
        "The Saudi-led coalition said it intercepted ballistic missiles "
        "aimed at the kingdom, as air-raid alerts sounded for a third "
        "night.",
    ),
    (
        "DISASTER",
        (176, 106, 24),
        "Strong earthquake shakes Peru",
        "A magnitude 6.7 quake struck the Junin region and was felt in "
        "Lima. There were no immediate reports of casualties or major "
        "damage.",
    ),
    (
        "EUROPE",
        (44, 92, 168),
        "Denmark expels Russian defence attache",
        "Copenhagen also halted non-essential visas for Russians after "
        "police said they had foiled an assassination plot.",
    ),
    (
        "JUSTICE",
        (104, 68, 150),
        "ICJ: Myanmar committed genocide against the Rohingya",
        "The World Court ruled 9-6 in favour of The Gambia's case. "
        "Rohingya groups welcomed the ruling and urged enforcement.",
    ),
    (
        "SPACE",
        (22, 110, 138),
        "BepiColombo enters orbit around Mercury",
        "After an eight-year, 9-billion-km journey, the ESA-JAXA probe "
        "began its science mission around the Solar System's smallest "
        "planet.",
    ),
]


def load_font(size, bold=False):
    """Try common system fonts, then fall back to Pillow's default."""
    names = (
        ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
        if bold
        else ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    )
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, font, colour, max_width, line_height):
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=colour)
        y += line_height
    return y


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)

    # Header
    draw.rectangle([0, 0, WIDTH, 218], fill=NAVY)
    draw.rectangle([0, 218, WIDTH, 226], fill=GOLD)
    title_font = load_font(68, bold=True)
    subtitle_font = load_font(30)
    date_font = load_font(26, bold=True)
    draw.text((64, 42), "THE WORLD IN ONE DAY", font=title_font, fill=(255, 255, 255))
    draw.text(
        (64, 132),
        "Saturday 21 November 2026  -  Six stories that shaped the day",
        font=subtitle_font,
        fill=(196, 210, 224),
    )
    date_text = "21 NOV 2026"
    date_w = draw.textlength(date_text, font=date_font)
    draw.rounded_rectangle(
        [WIDTH - 64 - date_w - 36, 58, WIDTH - 64, 58 + 62],
        radius=10,
        fill=GOLD,
    )
    draw.text(
        (WIDTH - 64 - date_w - 18, 74),
        date_text,
        font=date_font,
        fill=NAVY,
    )

    # Six cards: two columns x three rows
    tag_font = load_font(22, bold=True)
    head_font = load_font(33, bold=True)
    body_font = load_font(25)
    foot_font = load_font(20)
    margin = 48
    gap = 28
    card_w = (WIDTH - margin * 2 - gap) // 2
    card_h = 258
    top = 258
    for index, (tag, accent, headline, summary) in enumerate(STORIES):
        col = index % 2
        row = index // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=CARD)
        draw.rounded_rectangle([x, y, x + card_w, y + 10], radius=5, fill=accent)
        draw.rectangle([x, y + 5, x + card_w, y + 10], fill=accent)
        draw.text((x + 32, y + 28), tag, font=tag_font, fill=accent)
        draw_wrapped(
            draw, x + 32, y + 66, headline, head_font, INK, card_w - 64, 42
        )
        draw_wrapped(
            draw, x + 32, y + 158, summary, body_font, MUTED, card_w - 64, 33
        )

    # Footer
    draw.text(
        (64, 1132),
        "Sources: Reuters, Associated Press, The Guardian, Anadolu Agency, ESA, Al Jazeera",
        font=foot_font,
        fill=MUTED,
    )
    draw.text(
        (64, 1160),
        "Generated deterministically by generate.py (Python + Pillow). No external files.",
        font=foot_font,
        fill=MUTED,
    )

    image.save(OUTPUT, format="PNG")
    print(f"Wrote {OUTPUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
