"""Generate TypeScript types from backend Pydantic models.

Usage:
    uv run python scripts/gen_types.py

Exports JSON Schema from backend event models and converts to TypeScript.
Falls back to manual type generation if json-schema-to-typescript is not available.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_EVENTS = ROOT / "backend" / "app" / "events" / "models.py"
OUTPUT_DIR = ROOT / "frontend" / "src" / "lib"
OUTPUT_FILE = OUTPUT_DIR / "generated-types.ts"
SCHEMA_FILE = ROOT / "frontend" / "src" / "lib" / "event-schemas.json"


def export_schemas() -> dict:
    """Export JSON Schema from all event data models."""
    # Import the models
    sys.path.insert(0, str(ROOT))
    from backend.app.events.models import EVENT_DATA_MODELS, EventEnvelope

    schemas = {}

    # Envelope schema
    schemas["EventEnvelope"] = EventEnvelope.model_json_schema()

    # All event data models
    for _event_type, model_class in EVENT_DATA_MODELS.items():
        name = model_class.__name__
        schemas[name] = model_class.model_json_schema()

    return schemas


def generate_typescript(schemas: dict) -> str:
    """Generate TypeScript type definitions from JSON schemas."""
    lines = [
        "// Auto-generated from backend/app/events/models.py",
        "// Do not edit manually. Run: uv run python scripts/gen_types.py",
        "",
        "/* eslint-disable */",
        "",
    ]

    # Try to use json-schema-to-typescript via npx
    try:
        schema_json = json.dumps({"definitions": schemas}, indent=2)
        SCHEMA_FILE.write_text(schema_json, encoding="utf-8")

        result = subprocess.run(
            ["npx", "--yes", "json-schema-to-typescript", str(SCHEMA_FILE)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: generate basic types manually
    lines.append("// Generated manually (json-schema-to-typescript not available)")
    lines.append("")

    for name, schema in schemas.items():
        lines.append(f"export interface {name} {{")
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        for prop_name, prop_def in props.items():
            ts_type = _json_type_to_ts(prop_def)
            optional = "" if prop_name in required else "?"
            lines.append(f"  {prop_name}{optional}: {ts_type};")
        lines.append("}")
        lines.append("")

    return "\n".join(lines)


def _json_type_to_ts(prop: dict) -> str:
    """Convert a JSON Schema property to a TypeScript type."""
    if "enum" in prop:
        return " | ".join(f'"{v}"' for v in prop["enum"])
    if "anyOf" in prop:
        types = [_json_type_to_ts(t) for t in prop["anyOf"]]
        return " | ".join(types)
    if "const" in prop:
        return f'"{prop["const"]}"' if isinstance(prop["const"], str) else str(prop["const"])

    json_type = prop.get("type", "any")
    if json_type == "string":
        if prop.get("format") == "date-time":
            return "string"  # ISO date string
        return "string"
    if json_type == "integer" or json_type == "number":
        return "number"
    if json_type == "boolean":
        return "boolean"
    if json_type == "array":
        items = prop.get("items", {})
        item_type = _json_type_to_ts(items)
        return f"{item_type}[]"
    if json_type == "object":
        additional = prop.get("additionalProperties", {})
        if additional:
            val_type = _json_type_to_ts(additional)
            return f"Record<string, {val_type}>"
        return "Record<string, unknown>"
    if json_type == "null":
        return "null"
    return "unknown"


def main() -> None:
    print("Exporting schemas from backend event models...")
    schemas = export_schemas()

    print(f"Found {len(schemas)} models")

    ts_code = generate_typescript(schemas)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(ts_code, encoding="utf-8")
    print(f"Generated TypeScript types at {OUTPUT_FILE}")

    # Also save the raw schemas
    SCHEMA_FILE.write_text(json.dumps(schemas, indent=2, default=str), encoding="utf-8")
    print(f"Saved JSON schemas at {SCHEMA_FILE}")


if __name__ == "__main__":
    main()
