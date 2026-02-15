import shipper

from pshipper.formatter import create_ship_variant_table
from pshipper.utils import fix_d_variants, load_variant_notes, load_template, load_variant_whitelist

def generate_variant_table(data, key_by, ships_to_generate, template, notes,
                           collapse_whitelist, collapse_after_amount, write_to_file):

    ships = shipper.get_ships(data, key_by)

    fix_d_variants(ships)

    ship_names = [s.strip() for s in ships_to_generate.split(",") if s.strip() != '']
    r_ships = []
    for ship_name in ship_names:
        r_ships.append(ships.get(ship_name))

    results = []

    for ship in r_ships:
        result = create_ship_variant_table(
            ship,
            load_variant_notes(notes),
            load_template(template),
            load_variant_whitelist(collapse_whitelist),
            collapse_after_amount
        )

        results.append(f"{ship['name']}\n{'=' * len(ship['name'])}\n{result}\n")

    if write_to_file is not None and len(write_to_file) > 0:
        with open(write_to_file, "w") as f:
            for result in results:
                f.write(result)
    else:
        for result in results:
            print(result)