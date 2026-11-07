"""Fetch and verify the pinned QnVoice Filipino model files."""

import argparse
import hashlib
import shutil
import tempfile
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent
REVISION = "5b912ca3328145b384134040dcc520114f000e32"
SOURCE = f"https://huggingface.co/CholoAsis/qnvoice-filipino-voxcpm2-gguf/resolve/{REVISION}"


def matches(path, expected):
    if not path.is_file():
        return False
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest() == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=ROOT / "model")
    parser.add_argument("--verify", action="store_true", help="Check local files without downloading.")
    args = parser.parse_args()
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split()
        path = args.directory / name
        if not matches(path, expected):
            if args.verify:
                parser.exit(1, f"Missing or mismatched file {path}\n")
            args.directory.mkdir(parents=True, exist_ok=True)
            print(f"Downloading {name}", flush=True)
            with tempfile.TemporaryDirectory(dir=args.directory) as temporary:
                staged = Path(temporary) / name
                with urlopen(f"{SOURCE}/{name}", timeout=120) as response, staged.open("wb") as output:
                    shutil.copyfileobj(response, output, length=1024 * 1024)
                if not matches(staged, expected):
                    parser.exit(1, f"SHA-256 mismatch for {name}\n")
                staged.replace(path)
        print(f"Verified {name}", flush=True)


if __name__ == "__main__":
    main()
