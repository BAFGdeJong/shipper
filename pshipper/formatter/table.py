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

        goal_variant = variant.get('goal_variant', False)
        variant['goal_variant'] = "Yes" if goal_variant else "No"

        note = variant.get('notes', '')
        variant['notes'] = note

        # if len(note) <= 0: // TODO fix
        #     variant['notes'] = __find_variant_note(ship_data['name'], variant, notes)

    return ship_data

def __find_variant_note(ship_name, variant, notes):
    rules = notes.get(ship_name, [])

    if not rules:
        return ""

    for rule in rules:
        if rule["variant"] != variant["display_name"]:
            return ""

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

    return ""


def __check_if_collapse(ship_data, collapse_whitelist: list, collapse_limit: int):
    if ship_data['name'] in collapse_whitelist:
        return False
    else:
        return True if len(ship_data['variants']) > collapse_limit else False

def create_ship_variant_table(ship_data, notes: dict, template: Template, collapse_whitelist: list, collapse_limit: int) -> str:
    processed_data = __preprocess_data(ship_data, notes)
    return template.render(
        variants=processed_data['variants'],
        collapse=__check_if_collapse(processed_data, collapse_whitelist, collapse_limit)
    )
