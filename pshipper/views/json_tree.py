from rich.console import Console
from rich.tree import Tree

console = Console()


def add_to_tree(tree: Tree, data):
    """
    Recursively adds data to a Rich Tree.
    """
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, (dict, list)):
                branch = tree.add(f"[bold cyan]{key}[/]")
                add_to_tree(branch, val)
            else:
                tree.add(f"[bold cyan]{key}[/]: [green]{val}[/]")

    elif isinstance(data, list):
        for i, item in enumerate(data):
            label = f"[bold magenta]Item {i}[/]"
            if isinstance(item, dict):
                if 'variant_id' in item:
                    label = f"[bold magenta]{item['variant_id']}[/]"
                elif 'id' in item:
                    label = f"[bold magenta]{item['id']}[/]"
                elif 'name' in item:
                    label = f"[bold magenta]{item['name']}[/]"

            branch = tree.add(label)
            add_to_tree(branch, item)

    else:
        tree.add(str(data))


def json_tree(data: dict, title: str = "Ship Data"):
    """
    Renders JSON as a Tree.
    """
    root = Tree(f"[bold underline white]{title}[/]")
    add_to_tree(root, data)
    console.print(root)