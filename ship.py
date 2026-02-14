import shipper

from pshipper.runners import update_variant_tables
from pshipper.utils import load_variant_whitelist, load_variant_notes, load_template, VariantTabler

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shipper Tool")

    parser.add_argument("-d", "--data", default="", help="Set starsector data directory", required=True)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_parser = subparsers.add_parser("create", help="Create ...")
    create_parser.add_argument("-p", "--ship", help="Path to the whitelist JSON", required=True)
    create_parser.add_argument("-n", "--notes", default="notes.json", help="Path to the notes JSON")
    create_parser.add_argument("-t", "--template", default="ship_variant.template", help="Path to the template file")
    create_parser.add_argument("-c", "--collapse_after_amount", default=3, type=int, help="After what amount of variants to collapse")
    create_parser.add_argument("-w", "--write_to_file", default="", help="Write table to disk") # TODO

    update_parser = subparsers.add_parser("update", help="Update ...")
    update_parser.add_argument("-w", "--whitelist", default="whitelist.json", help="Filename in data/variant/")
    update_parser.add_argument("-n", "--notes", default="notes.json", help="Filename in data/variant/")
    update_parser.add_argument("-t", "--template", default="ship_variant.template", help="Filename in templates/")

    args = parser.parse_args()

    if not args.data.endswith("/") and not args.data.endswith("\\"):
        args.data += "/"

    if args.command == "create":
        ship = shipper.get_ships(args.data, "name").get(args.ship, None)

        if ship is None:
            print("Ship does not exist or could not be found")
        else:
            result = VariantTabler.render_ship_table(
                ship,
                load_variant_notes(args.notes),
                load_template(args.template),
                args.collapse_after_amount
            )

            if len(args.write_to_file) > 0:
                with open(args.write_to_file, "w") as f:
                    f.write(result)

            print(result)

    if args.command == "update":
        update_variant_tables(
            args.data,
            load_variant_whitelist(args.whitelist),
            load_variant_notes(args.notes),
            load_template(args.template)
        )
