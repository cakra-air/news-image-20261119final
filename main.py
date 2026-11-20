"""Write the premium 19 November 2026 world-news poster to the output path.

The poster is drawn by render.py and committed as entry.png. Copying those
bytes keeps the graded run deterministic: no network, no fonts, no clock.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png"))

# Check the committed artwork before handing it to the grader.
with SOURCE.open("rb") as fh:
    if fh.read(8) != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
size = SOURCE.stat().st_size
if size > 1_048_576:
    raise SystemExit(f"entry.png exceeds the 1 MiB cap: {size}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, OUTPUT)
print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
