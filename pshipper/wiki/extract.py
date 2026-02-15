import re

from pshipper.wiki.ship_mount import ShipMount


def extract_ship_info(text: str) -> dict:
    infobox_pattern = r"\{\{ShipInfobox\s*((?:[^{}]|\{\{.*?\}\})*)\}\}"
    match = re.search(infobox_pattern, text, re.DOTALL)

    if not match:
        return {}

    content = match.group(1)
    arguments = []
    current_arg = []
    depth = 0

    for char in content:
        if char == '{':
            depth += 1
            current_arg.append(char)
        elif char == '}':
            depth -= 1
            current_arg.append(char)
        elif char == '|' and depth == 0:
            arguments.append("".join(current_arg))
            current_arg = []
        else:
            current_arg.append(char)

    arguments.append("".join(current_arg))

    data = {}
    for arg in arguments:
        if '=' in arg:
            key, value = arg.split('=', 1)
            clean_key = key.strip()
            clean_value = value.strip()

            if clean_key:
                data[clean_key] = clean_value

    description = data.get('Description', None)
    add_description = data.get('AddDescription', None)

    if add_description and description:
        parts = [description, add_description]
        new_desc = "\n\n".join(p.strip() for p in parts if p and p.strip())

        data.update({'Description': new_desc})
        data.pop('AddDescription', None)

    mounts = data.get('Mounts', None)
    if mounts:
        new_mounts = []
        for mount in mounts.split(','):
            new_mounts.append(ShipMount.from_wiki_mount(mount).to_dict())
        data.update({'Mounts': ShipMount.sort_mounts(new_mounts)})

    hullmods = data.get('Hullmods', None)
    if hullmods:
        data.update({'Hullmods': [x.strip() for x in hullmods.split(',')].sort()})

    return data