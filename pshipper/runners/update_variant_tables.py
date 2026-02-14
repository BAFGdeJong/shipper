import os
import time
import shipper

from dotenv import load_dotenv
from mwcleric import AuthCredentials, WikiClient

from pshipper.editors.editor import Editor

def update_variant_tables(starsector_data_folder, ship_whitelist, notes, template):
    all_ships = shipper.get_ships(starsector_data_folder, "name")

    load_dotenv()

    username = os.getenv("WIKI_USERNAME")
    password = os.getenv("WIKI_PASSWORD")

    if not username or not password:
        print("Error: WIKI_USERNAME or WIKI_PASSWORD not found in .venv")
        return

    credentials = AuthCredentials(username=username, password=password, user_file=None)

    client = WikiClient('https://starsector.wiki.gg', credentials=credentials)

    editor = Editor(client)

    for ship in ship_whitelist:
        ship_data = all_ships.get(ship)

        if ship_data:
            print(f"Processing {ship}...")
            try:
                editor.add_ship_variants(ship_data, notes, template, 1)

                time.sleep(2.5)

            except Exception as e:
                print(f"Error updating {ship}: {e}")
                time.sleep(10)
        else:
            print(f"Warning: Ship data for '{ship}' not found.")
