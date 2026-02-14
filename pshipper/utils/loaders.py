import json
from pathlib import Path
from jinja2 import FileSystemLoader, Environment, Template

BASE_DIR = Path(__file__).resolve().parent.parent

def load_variant_whitelist(name: str) -> list[str]:
    path = BASE_DIR / "data" / "variant" / name
    try:
        content = path.read_text(encoding='utf-8')
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: Whitelist not found at {path}")
        return []

def load_variant_notes(name: str) -> dict:
    path = BASE_DIR / "data" / "variant" / name
    try:
        content = path.read_text(encoding='utf-8')
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: Notes not found at {path}")
        return {}

def load_template(name: str) -> Template | None:
    template_dir = BASE_DIR / "templates"

    file_loader = FileSystemLoader(str(template_dir))
    env = Environment(loader=file_loader)

    try:
        return env.get_template(name)
    except Exception as e:
        print(f"Error loading template {name} from {template_dir}: {e}")
        return None
