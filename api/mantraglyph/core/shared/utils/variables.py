from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
CSV_COLORS = os.path.join(BASE_DIR, "mantraglyph", "core", "assets", "csv", "colors.csv",)
WURMIC_BRAVO = os.path.join(BASE_DIR, "mantraglyph", "core", "assets", "fonts", "Wurmics_Bravo.ttf",)

