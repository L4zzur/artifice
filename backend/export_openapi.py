import json
from pathlib import Path

from main import app

frontend_dir = Path(__file__).parent.parent / "frontend"
openapi_path = frontend_dir / "openapi.json"

schema = app.openapi()

with open(openapi_path, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print(f"OpenAPI schema saved to {openapi_path}")
