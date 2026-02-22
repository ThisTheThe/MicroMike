#!/usr/bin/env python3
"""
watch_assets.py
───────────────
Drop this file into any folder containing your Obsidian CSS theme assets.
Run it once; it watches the folder and rebuilds `_art.scss` whenever an
image file is added, changed, or removed.

_art.scss will contain one CSS custom property per image:
    :root {
      --art-logo-png: url("data:image/png;base64,...");
      --art-icon-svg: url("data:image/svg+xml;base64,...");
    }

Variable names are derived from filenames:
    logo.png  →  --art-logo-png
    my icon.svg  →  --art-my-icon-svg   (spaces → hyphens, lowercased)

Requirements:
    pip install watchdog
"""

import base64
import mimetypes
import re
import sys
import time
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".ico"}
OUTPUT_FILENAME   = "_art.scss"
VAR_PREFIX        = "--art-"

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Convert a filename stem+ext to a CSS-safe identifier segment."""
    # Replace dots and spaces/underscores with hyphens, lowercase everything
    slug = re.sub(r"[\s_.]+", "-", name).lower()
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def mime_for(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    # SVG isn't always in the system mime db
    if mime is None and path.suffix.lower() == ".svg":
        mime = "image/svg+xml"
    return mime or "application/octet-stream"


def file_to_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    mime = mime_for(path)
    return f'url("data:{mime};base64,{data}")'


def build_scss(folder: Path) -> str:
    images = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not images:
        return "/* no images found – _art.scss is empty */\n"

    lines = [":root {"]
    for img in images:
        var_name  = VAR_PREFIX + slugify(img.stem)
        data_uri  = file_to_data_uri(img)
        lines.append(f"  {var_name}: {data_uri};")
    lines.append("}\n")
    return "\n".join(lines)


def rebuild(folder: Path) -> None:
    output = folder / OUTPUT_FILENAME
    scss   = build_scss(folder)
    output.write_text(scss, encoding="utf-8")
    count  = scss.count(VAR_PREFIX)
    print(f"[rebuilt]  {output.name}  ({count} variable{'s' if count != 1 else ''})")

# ── Watcher ───────────────────────────────────────────────────────────────────

def watch(folder: Path) -> None:
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        print("watchdog is not installed.  Run:  pip install watchdog")
        sys.exit(1)

    class Handler(FileSystemEventHandler):
        def _relevant(self, path: str) -> bool:
            p = Path(path)
            return (
                p.suffix.lower() in IMAGE_EXTENSIONS
                and p.parent == folder
            )

        def on_created(self, event):
            if not event.is_directory and self._relevant(event.src_path):
                print(f"[detected] + {Path(event.src_path).name}")
                rebuild(folder)

        def on_deleted(self, event):
            if not event.is_directory and self._relevant(event.src_path):
                print(f"[detected] - {Path(event.src_path).name}")
                rebuild(folder)

        def on_modified(self, event):
            if not event.is_directory and self._relevant(event.src_path):
                print(f"[detected] ~ {Path(event.src_path).name}")
                rebuild(folder)

        def on_moved(self, event):
            src_rel = self._relevant(event.src_path)
            dst_rel = self._relevant(event.dest_path)
            if src_rel or dst_rel:
                print(f"[detected] mv {Path(event.src_path).name} → {Path(event.dest_path).name}")
                rebuild(folder)

    observer = Observer()
    observer.schedule(Handler(), str(folder), recursive=False)
    observer.start()
    print(f"Watching  {folder}")
    print(f"Output →  {folder / OUTPUT_FILENAME}")
    print("Press Ctrl-C to stop.\n")

    # Initial build
    rebuild(folder)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        print("\nStopped.")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    folder = Path(__file__).parent.resolve()
    watch(folder)
