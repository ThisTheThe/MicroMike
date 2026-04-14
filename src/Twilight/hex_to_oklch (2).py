#!/usr/bin/env python3
"""
Convert hex color values in CSS files to OKLCH.
Backs up originals to backup/ before modifying.
Supports #RGB, #RRGGBB, #RRGGBBAA formats.
"""

import re
import shutil
import math
from pathlib import Path


# ── Color math ────────────────────────────────────────────────────────────────

def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_oklab(r: float, g: float, b: float) -> tuple[float, float, float]:
    # Linear sRGB → LMS (approximate)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = l ** (1 / 3)
    m_ = m ** (1 / 3)
    s_ = s ** (1 / 3)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return L, a, b_


def oklab_to_oklch(L: float, a: float, b: float) -> tuple[float, float, float]:
    C = math.sqrt(a * a + b * b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


def hex_to_oklch(hex_str: str) -> tuple[float, float, float, float | None]:
    """Returns (L, C, H, alpha_or_None). L is 0–1, C ~0–0.4, H 0–360, alpha 0–1."""
    h = hex_str.lstrip("#")

    # Expand shorthand
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    elif len(h) == 4:
        h = "".join(c * 2 for c in h)

    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        alpha = None
    elif len(h) == 8:
        r, g, b, a = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)
        alpha = round(a / 255, 4)
    else:
        raise ValueError(f"Unrecognised hex: {hex_str}")

    rl = srgb_to_linear(r / 255)
    gl = srgb_to_linear(g / 255)
    bl = srgb_to_linear(b / 255)

    L, a_ok, b_ok = linear_to_oklab(rl, gl, bl)
    L, C, H = oklab_to_oklch(L, a_ok, b_ok)

    return L, C, H, alpha


def format_oklch(L: float, C: float, H: float, alpha: float | None) -> str:
    Lp = f"{L:.4f}".rstrip("0").rstrip(".")
    Cp = f"{C:.4f}".rstrip("0").rstrip(".")
    Hp = f"{H:.2f}".rstrip("0").rstrip(".")
    if alpha is not None:
        ap = f"{alpha:.4f}".rstrip("0").rstrip(".")
        return f"oklch({Lp} {Cp} {Hp} / {ap})"
    return f"oklch({Lp} {Cp} {Hp})"


# ── Regex & replacement ───────────────────────────────────────────────────────

HEX_RE = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")


def replace_hex(match: re.Match) -> str:
    try:
        L, C, H, alpha = hex_to_oklch(match.group(0))
        return format_oklch(L, C, H, alpha)
    except Exception as e:
        print(f"  ⚠ Could not convert {match.group(0)}: {e}")
        return match.group(0)


def convert_css_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, count = HEX_RE.subn(replace_hex, text)
    if count:
        path.write_text(new_text, encoding="utf-8")
    return count


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    script_dir = Path(__file__).parent
    css_files = list(script_dir.glob("*.css")) + list(script_dir.glob("*.scss"))

    if not css_files:
        print("No CSS/SCSS files found in the same folder as this script.")
        return

    backup_dir = script_dir / "backup"
    backup_dir.mkdir(exist_ok=True)

    print(f"Found {len(css_files)} CSS/SCSS file(s). Backing up to {backup_dir}/\n")

    for css in css_files:
        dest = backup_dir / css.name
        # Keep existing backups safe by numbering
        if dest.exists():
            i = 1
            while (backup_dir / f"{css.stem}.{i}{css.suffix}").exists():
                i += 1
            dest = backup_dir / f"{css.stem}.{i}{css.suffix}"
        shutil.copy2(css, dest)
        print(f"  backed up → {dest.name}")

    print()

    total = 0
    for css in css_files:
        count = convert_css_file(css)
        print(f"  {css.name}: {count} color(s) converted")
        total += count

    print(f"\nDone. {total} hex value(s) converted to oklch across {len(css_files)} file(s).")


if __name__ == "__main__":
    main()
