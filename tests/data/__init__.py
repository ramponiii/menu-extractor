from pathlib import Path

from menu_extractor.models import Menu

DATA_DIR = Path(__file__).parent

RONIS_MENU = DATA_DIR / "ronis.pdf"


GARDEN_GATE_PDF = DATA_DIR / "garden_gate.pdf"
_GARDEN_GATE_EXPECTATION = (DATA_DIR / "garden_gate_expected_menu.json").read_text(
    encoding="utf-8"
)
GARDEN_GATE_EXPECTATION = Menu.model_validate_json(
    _GARDEN_GATE_EXPECTATION, strict=True
)


__all__ = ["GARDEN_GATE_EXPECTATION", "GARDEN_GATE_PDF"]
