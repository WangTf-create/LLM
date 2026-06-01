"""Export OpenAPI schema to openapi.json (Phase 4)."""

import json
from pathlib import Path

from app import app

OUTPUT = Path(__file__).resolve().parent / "openapi.json"


def main():
    schema = app.openapi()
    OUTPUT.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
