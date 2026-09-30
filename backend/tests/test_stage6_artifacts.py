"""Stage 6 dossier artifacts.

`pins.zip` used to be a hardcoded empty-zip header, so the artifact announced in
`dossier.ready` never contained the characterization tests it advertised.
"""

import shutil
import zipfile
from pathlib import Path

import pytest

from backend.app.events.bus import EventBus
from backend.app.stages.stage2_record import PinsResult
from backend.app.stages.stage6_dossier import Stage6Dossier
from backend.app.store.db import init_db

PIN_CODE = "def test_tax_half_up():\n    assert calculate_tax(50.10) == 2.51\n"


class _Evidence:
    specimen_name = "invoice_totals"
    source_code = "def calculate_tax(amount):\n    return amount\n"
    pins = PinsResult(
        test_count=14,
        coverage=92.5,
        baseline_checkpoint="chk-demo",
        test_code=PIN_CODE,
    )


class _EvidenceWithoutPins:
    specimen_name = "invoice_totals"
    source_code = ""
    pins = None


@pytest.mark.asyncio
async def test_pins_zip_contains_characterization_tests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    await init_db()

    result = await Stage6Dossier(EventBus()).run("run-pins", _Evidence())
    pins_path = Path(result.pins_path)

    assert zipfile.is_zipfile(pins_path)
    with zipfile.ZipFile(pins_path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert "test_characterization.py" in names
        # A real archive, not the 22-byte empty-zip stub.
        assert len(names) >= 2
        assert archive.read("test_characterization.py").decode("utf-8") == PIN_CODE


@pytest.mark.asyncio
async def test_pins_zip_is_still_valid_without_pins(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    await init_db()

    result = await Stage6Dossier(EventBus()).run("run-nopins", _EvidenceWithoutPins())
    pins_path = Path(result.pins_path)

    assert zipfile.is_zipfile(pins_path)
    with zipfile.ZipFile(pins_path) as archive:
        assert archive.testzip() is None
        assert archive.namelist() == ["README.md"]


@pytest.mark.asyncio
async def test_pins_zip_is_reproducible(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Identical evidence must yield a byte-identical archive."""
    monkeypatch.chdir(tmp_path)
    await init_db()
    stage = Stage6Dossier(EventBus())
    run_dir = tmp_path / "data" / "runs" / "run-a"

    await stage.run("run-a", _Evidence())
    first = (run_dir / "pins.zip").read_bytes()
    shutil.rmtree(run_dir)
    await stage.run("run-a", _Evidence())
    second = (run_dir / "pins.zip").read_bytes()

    assert first == second
