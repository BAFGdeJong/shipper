import os

import shipper
from dotenv import load_dotenv

from pshipper.editors.editor import Editor
from pshipper.runners.get_wiki_ship_data import get_wiki_ship_data
from pshipper.runners.variant_tables import sync_variants_to_wiki
from pshipper.utils import load_variant_whitelist, load_variant_notes, load_template, fix_d_variants
from pshipper.formatter import create_ship_variant_table

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shipper Tool")

    parser.add_argument("-d", "--data", default="", help="Set starsector data directory", required=True)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    check_parser = subparsers.add_parser("check", help="Check if wiki page needs to be updated")
    check_parser.add_argument("-s", "--ships", default="", help="Ships tables to create", required=True)

    create_parser = subparsers.add_parser("create", help="Create ...")
    create_parser.add_argument("-s", "--ships", default="", help="Ships tables to create", required=True)
    create_parser.add_argument("-n", "--notes", default="notes.json", help="Path to the notes JSON")
    create_parser.add_argument("-t", "--template", default="ship_variant.template", help="Path to the template file")
    create_parser.add_argument("-o", "--collapse_whitelist", default="collapse_whitelist.json", help="Path to the whitelist JSON")
    create_parser.add_argument("-c", "--collapse_after_amount", default=0, type=int, help="After what amount of variants to collapse")
    create_parser.add_argument("-w", "--write_to_file", default="", help="Write table to disk") # TODO

    sync_parser = subparsers.add_parser("sync", help="Sync ...")
    sync_parser.add_argument("-u", "--update", default=False, type=bool, help="Write table to disk")
    sync_parser.add_argument("-w", "--whitelist", default="whitelist.json", help="Filename in data/variant/")
    sync_parser.add_argument("-n", "--notes", default="notes.json", help="Filename in data/variant/")
    sync_parser.add_argument("-t", "--template", default="ship_variant.template", help="Filename in templates/")
    sync_parser.add_argument("-o", "--collapse_whitelist", default="collapse_whitelist.json", help="Path to the whitelist JSON")
    sync_parser.add_argument("-c", "--collapse_after_amount", default=0, type=int, help="After what amount of variants to collapse")
    sync_parser.add_argument("-s", "--ships", default="", help="Ships to update")

    args = parser.parse_args()

    if not args.data.endswith("/") and not args.data.endswith("\\"):
        args.data += "/"

    if args.command == "check":
        ships = shipper.get_ships(args.data, "name")

        fix_d_variants(ships)

        ship_names = [s.strip() for s in args.ships.split(",") if s.strip() != '']
        r_ships = []
        for ship_name in ship_names:
            r_ships.append(ships.get(ship_name))

        load_dotenv()
        username = os.getenv("WIKI_USERNAME")
        password = os.getenv("WIKI_PASSWORD")

        if not username or not password:
            print("Error: WIKI_USERNAME or WIKI_PASSWORD not found in .env")
            exit(1)

        for ship in r_ships:
            get_wiki_ship_data(Editor(username, password), ship)

    if args.command == "create":
        ships = shipper.get_ships(args.data, "name")

        fix_d_variants(ships)

        ship_names = [s.strip() for s in args.ships.split(",") if s.strip() != '']
        r_ships = []
        for ship_name in ship_names:
            r_ships.append(ships.get(ship_name))

        results = []

        for ship in r_ships:
            print(ship)
            result = create_ship_variant_table(
                ship,
                load_variant_notes(args.notes),
                load_template(args.template),
                load_variant_whitelist(args.collapse_whitelist),
                args.collapse_after_amount
            )

            results.append(f"{ship['name']}\n{'=' * len(ship['name'])}\n{result}\n")

        if len(args.write_to_file) > 0:
            with open(args.write_to_file, "w") as f:
                for result in results:
                    f.write(result)
        else:
            for result in results:
                print(result)

    if args.command == "sync":
        load_dotenv()
        username = os.getenv("WIKI_USERNAME")
        password = os.getenv("WIKI_PASSWORD")

        if not username or not password:
            print("Error: WIKI_USERNAME or WIKI_PASSWORD not found in .env")
            exit(1)

        update_ships = [s.strip() for s in args.ships.split(",") if s.strip() != '']

        sync_variants_to_wiki(
            editor=Editor(username, password),
            starsector_data_folder=args.data,
            update_ships=update_ships,
            ship_whitelist=load_variant_whitelist(args.whitelist),
            notes=load_variant_notes(args.notes),
            template=load_template(args.template),
            collapse_whitelist=load_variant_whitelist(args.collapse_whitelist),
            collapse_limit=args.collapse_after_amount,
            rate_limit_delay=2.5,
            update=args.update,
        )
