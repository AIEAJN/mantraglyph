from pathlib import Path
import hashlib
import os
import random

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
CSV_COLORS = os.path.join(
    BASE_DIR,
    "mantraglyph",
    "core",
    "assets",
    "csv",
    "colors.csv",
)
WURMIC_BRAVO = os.path.join(
    BASE_DIR,
    "mantraglyph",
    "core",
    "assets",
    "fonts",
    "Wurmics_Bravo.ttf",
)
MANTRA_PATH = os.path.join(
    BASE_DIR,
    "mantraglyph",
    "core",
    "assets",
    "mantras",
    "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(7)) +".jpg",
)

print(MANTRA_PATH)
