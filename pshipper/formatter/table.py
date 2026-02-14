from collections import Counter

from jinja2 import Template


def __preprocess_data(ship_data, notes):

    for variant in ship_data['variants']:
        all_weapon_ids = []

        for group in variant.get('weapon_groups', []):
            for weapon in group.get('weapons', []):
                all_weapon_ids.append(weapon['id'])

        for wing in variant.get('wings', []):
            wing_name = f"{wing.get('name', '')} {wing.get('display_name', '')}"
            all_weapon_ids.append(wing_name)

        counts = Counter(all_weapon_ids)
        variant['consolidated_weapons'] = {
            pid: count for pid, count in counts.items()
        }

        raw_mods = variant.get('hull_mods', [])
        variant['hull_mods'] = [m for m in raw_mods]

        note = __find_variant_note(ship_data['name'], variant, notes)

        if note:
            variant['note'] = note
        else:
            variant['note'] = ""

    return ship_data

def __find_variant_note(ship_name, variant, notes):
    rules = notes.get(ship_name, [])

    if not rules:
        return None

    for rule in rules:
        if rule["variant"] != variant["display_name"]:
            return None

        constraints = rule.get("constraints")

        if constraints:
            match = True
            for key, required_value in constraints.items():
                if variant.get(key) != required_value:
                    match = False
                    break

            if not match:
                continue

        return rule["note"]

    return None


def __check_if_collapse(ship_data, collapse_whitelist: list, collapse_limit: int):
    if ship_data['name'] in collapse_whitelist:
        return False
    else:
        return True if len(ship_data['variants']) > collapse_limit else False

def create_ship_variant_table(ship_data, notes: dict, template: Template, collapse_whitelist: list, collapse_limit: int):
    processed_data = __preprocess_data(ship_data, notes)
    return template.render(
        variants=processed_data['variants'],
        collapse=__check_if_collapse(processed_data, collapse_whitelist, collapse_limit)
    )
