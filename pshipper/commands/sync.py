import os

from dotenv import load_dotenv

from pshipper.wiki.client import Client
from pshipper.runners import sync_variants_to_wiki
from pshipper.utils import load_variant_whitelist, load_variant_notes, load_template


def sync(args):

    load_dotenv()
    username = os.getenv("WIKI_USERNAME")
    password = os.getenv("WIKI_PASSWORD")

    if not username or not password:
        print("Error: WIKI_USERNAME or WIKI_PASSWORD not found in .env")
        exit(1)

    update_ships = [s.strip() for s in args.ships.split(",") if s.strip() != '']

    sync_variants_to_wiki(
        editor=Client(username, password),
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