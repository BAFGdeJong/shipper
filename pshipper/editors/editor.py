import re

from mwcleric import WikiClient, AuthCredentials
from pshipper.formatter import create_ship_variant_table

class Editor:
    def __init__(self, username, password):
        credentials = AuthCredentials(username=username, password=password, user_file=None)
        client = WikiClient('https://starsector.wiki.gg', credentials=credentials)
        self.client = client

    def add_ship_variants(self, ship, notes, template, collapse_whitelist: list, collapse_after_amount: int):
        page_name = ship.get('name', 'Unknown')
        page = self.client.client.pages[page_name]

        if not page.exists:
            print(f"Skipping {page_name}: Page does not exist.")
            return

        current_text = page.text()

        pattern = re.compile(r'(==\s*Variants\s*==)(.*?)(?=\n==|$)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(current_text)

        if match:
            existing_content = match.group(2)

            if not existing_content.strip():
                print(f"  Empty 'Variants' section found for {page_name}. Populating...")

                new_table = create_ship_variant_table(ship, notes, template, collapse_whitelist, collapse_after_amount)

                new_text = pattern.sub(f"\\1\n{new_table}\n", current_text)

                page.save(new_text, summary=f"Added variants")
            else:
                print(f"  Skipping {page_name}: Variants section already contains data.")
        else:
            print(f"  Skipping {page_name}: No '== Variants ==' header found.")
