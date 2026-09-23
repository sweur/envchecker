#!/usr/bin/env python3
import sys
from pathlib import Path

def parse_env_file(path):
    """Returns a dict of key -> value from a .env-style file."""
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env

def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    example_path = directory / ".env.example"
    env_path = directory / ".env"

    if not example_path.exists():
        print("no .env.example found in this directory")
        sys.exit(1)

    required = parse_env_file(example_path)
    actual = parse_env_file(env_path)

    missing = []
    empty = []

    for key in required:
        if key not in actual:
            missing.append(key)
        elif actual[key] == "":
            empty.append(key)

    if not missing and not empty:
        print(f"✓ all {len(required)} required vars present")
        sys.exit(0)

    if missing:
        print(f"missing ({len(missing)}):")
        for key in missing:
            print(f"  {key}")

    if empty:
        print(f"empty ({len(empty)}):")
        for key in empty:
            print(f"  {key}")

    sys.exit(1)