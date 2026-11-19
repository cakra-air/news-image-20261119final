"""Write the day's news poster to /output/entry.png.

The repository holds the finished poster (entry.png); this program copies it
to the required output path. Offline and deterministic: identical bytes on
every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png"))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, OUTPUT)
print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
