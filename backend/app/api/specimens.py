"""Specimens API."""

from pathlib import Path

from fastapi import APIRouter

from backend.app.settings import get_settings

router = APIRouter()


@router.get("")
async def list_specimens():
    settings = get_settings()
    specimens_dir = Path(settings.data_dir).parent.parent / "backend" / "specimens"
    if not specimens_dir.exists():
        return []

    specimens = []
    for d in specimens_dir.iterdir():
        if d.is_dir():
            notes_file = d / "NOTES.md"
            description = ""
            if notes_file.exists():
                with open(notes_file, encoding="utf-8") as f:
                    description = f.read().split("\n")[0]
            specimens.append({"name": d.name, "description": description})

    return specimens
