#!/usr/bin/env python3
"""
Recursively finds all .scss files from the script's directory
and generates an index.scss with @use statements for each.
Files named 'index.scss' are excluded to avoid self-reference.
"""

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "index6.scss")

scss_files = []

for root, dirs, files in os.walk(script_dir):
    # Sort dirs for consistent ordering
    dirs.sort()
    for filename in sorted(files):
        if filename.endswith(".scss") and filename != "index.scss":
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, script_dir)
            # Normalize to forward slashes
            rel_path = rel_path.replace(os.sep, "/")
            scss_files.append(rel_path)

lines = [f'@use "{path}";' for path in scss_files]
content = "\n".join(lines) + "\n"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Written {len(scss_files)} entries to {output_path}")
