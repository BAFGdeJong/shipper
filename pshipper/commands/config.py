from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    data_path: Path
    ships: str = ""
    notes: Path = Path("notes.json")
    template: Path = Path("ship_variant.template")