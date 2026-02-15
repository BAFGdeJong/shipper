import difflib
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def normalize_value(value) -> str:
    """
    Tries to normalize numbers to look the same (1 == 1.0).
    Returns a stripped string.
    """
    if value is None:
        return ""

    s_val = str(value).strip()

    if len(s_val) > 50:
        return " ".join(s_val.split())

    try:
        f_val = float(s_val)
        if f_val.is_integer():
            return str(int(f_val))
        return str(f_val)
    except (ValueError, TypeError):
        return s_val


def make_diff_text(old_val: str, new_val: str) -> Text:
    """
    Returns a Rich Text object showing the transformation.
    """
    diff = difflib.ndiff(old_val, new_val)
    text = Text()

    for opcode in diff:
        code, char = opcode[0], opcode[2]
        if code == ' ':
            text.append(char, style="dim white")
        elif code == '-':
            text.append(char, style="red strike")
        elif code == '+':
            text.append(char, style="bold green")

    return text


def compare_dicts(wiki_data: dict, generated_data: dict, title: str, show_identical: bool = False):
    table = Table(title=title, show_lines=True)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Wiki", style="red")
    table.add_column("Game", style="green")
    table.add_column("Diff")

    all_keys = sorted(set(wiki_data.keys()) | set(generated_data.keys()))
    changes_found = False

    for key in all_keys:
        raw_old = wiki_data.get(key)
        raw_new = generated_data.get(key)

        str_old = normalize_value(raw_old)
        str_new = normalize_value(raw_new)

        if key in wiki_data and key in generated_data:
            if str_old != str_new:
                diff_vis = make_diff_text(str_old, str_new)
                table.add_row(key, str_old, str_new, diff_vis)
                changes_found = True
            elif show_identical:
                table.add_row(key, str_old, str_new, "[dim]Matches[/]")

        elif key not in wiki_data:
            table.add_row(key, "[italic dim]Missing[/]", str_new, "[bold green]++ ADDED[/]")
            changes_found = True

        elif key not in generated_data:
            table.add_row(key, str_old, "[italic dim]Missing[/]", "[bold red]-- REMOVED[/]")
            changes_found = True

    if changes_found or show_identical:
        console.print(table)
    else:
        console.print(f"[bold green]✔ No differences found for {title}. Page is up to date![/]")