import re

from mwcleric import WikiClient, AuthCredentials
from pshipper.formatter import create_ship_variant_table

class Editor:
    def __init__(self, username, password):
        credentials = AuthCredentials(username=username, password=password, user_file=None)
        client = WikiClient('https://starsector.wiki.gg', credentials=credentials)
        self.client = client

    def add_ship_variants(self, ship, notes, template, collapse_whitelist: list, collapse_after_amount: int):
        page_name = ship.get('name', False)

        if not page_name:
            return

        page = self.client.client.pages[page_name]

        if not page.exists:
            print(f"Skipping {page_name}: Page does not exist.")
            return

        current_text = page.text()

        pattern = re.compile(r'(==\s*Variants\s*==)(.*?)(?=\n==|$)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(current_text)

        if match:
            existing_content = match.group(2)
            wiki_data = self.extract_wiki_variants(existing_content)

            for wiki_variant in wiki_data:
                notes = wiki_variant.get('Notes', False)
                if notes:
                    v_id = wiki_variant.get('Id', False)
                    name = wiki_variant.get('Name', False)
                    if v_id:
                        variants = ship['variants']
                        for variant in variants:
                            if variant['variant_id'] == v_id:
                                variant['notes'] = notes
                    elif name:
                        variants = ship['variants']
                        for variant in variants:
                            if (
                                variant['display_name'] == wiki_variant.get('Name', "")
                                and variant['flux_capacitors'] == wiki_variant.get("Capacitors", -9999)
                                and variant['flux_vents'] == wiki_variant.get("Vents", -9999)
                                and variant['hull_mods'] == wiki_variant.get("Hullmods", [False])
                            ):
                                variant['notes'] = notes


            if not existing_content.strip():
                print(f"  Empty 'Variants' section found for {page_name}. Populating...")
                new_table = create_ship_variant_table(ship, notes, template, collapse_whitelist, collapse_after_amount)
                new_text = pattern.sub(f"\\1\n{new_table}\n", current_text)

                page.save(new_text, summary=f"Added variants")
            else:
                print(f"  Skipping {page_name}: Variants section already contains data.")
        else:
            print(f"  Skipping {page_name}: No '== Variants ==' header found.")

    def update_ship_variants(self, ship, notes, template, collapse_whitelist: list, collapse_after_amount: int):
        page_name = ship.get('name', False)

        if not page_name:
            return "Could not find page name"

        page = self.client.client.pages[page_name]

        if not page.exists:
            return f"Skipping {page_name}: Page does not exist."

        current_text = page.text()

        pattern = re.compile(r'(==\s*Variants\s*==)(.*?)(?=\n==|$)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(current_text)

        if match:
            existing_content = match.group(2)
            wiki_data = self.extract_wiki_variants(existing_content)

            for wiki_variant in wiki_data:
                notes = wiki_variant.get('Notes', False)
                if notes:
                    v_id = wiki_variant.get('Id', False)
                    name = wiki_variant.get('Name', False)
                    if v_id:
                        variants = ship['variants']
                        for variant in variants:
                            if variant['variant_id'] == v_id:
                                variant['notes'] = notes
                    elif name:
                        variants = ship['variants']
                        for variant in variants:
                            if ( # TODO multiple exact same variants will clone the note
                                    variant['display_name'] == wiki_variant.get('Name', "")
                                    and variant['flux_capacitors'] == wiki_variant.get("Capacitors", -9999)
                                    and variant['flux_vents'] == wiki_variant.get("Vents", -9999)
                                    and variant['hull_mods'] == wiki_variant.get("Hullmods", [False])
                            ):
                                variant['notes'] = notes


            if existing_content.strip():
                new_table = create_ship_variant_table(ship, notes, template, collapse_whitelist, collapse_after_amount)
                new_text = pattern.sub(f"\\1\n{new_table}\n", current_text)

                page.save(new_text, summary=f"Updated variants")
                return f"Updated {page_name}"
            return f"No existing content on page {page_name} was found."
        else:
            return f"  Skipping {page_name}: No '== Variants ==' header found."

    def extract_wiki_variants(self, table_text: str) -> list[dict]:
        pattern = re.compile(r'(?m)^!(?!.*colspan).*$')
        headers = [h.lstrip('! ').strip() for h in pattern.findall(table_text)]
        rows = table_text.split('|-')

        variants = []

        for row in rows:
            row = row.strip()

            if not row or row.startswith('{|') or row.startswith('!'):
                continue

            cells = row.split('\n|')

            if len(cells) > 0 and cells[0].strip() == '':
                cells.pop(0)

            if len(cells) > 0:
                last_cell = cells[-1].strip()
                if last_cell == '}' or last_cell == '|}':
                    cells.pop()

            cells = [c.strip() for c in cells]

            result = {}
            for header in headers:
                result[header] = cells.pop(0)

            variants.append(result)

        for variant in variants:
            v_id = variant.get('Id', False)
            if v_id:
                variant['Id'] = v_id.lstrip('| ')

            name = variant.get('Name', False)
            if name:
                variant['Name'] = name.lstrip('| ')

            capacitors = variant.get('Capacitors', False)
            if capacitors:
                match = re.search(r'\|(\d+)', capacitors)
                variant['Capacitors'] = int(match.group(1))

            vents = variant.get('Vents', False)
            if vents:
                match = re.search(r'\|(\d+)', vents)
                variant['Vents'] = int(match.group(1))

            hull_mods = variant.get('Hullmods', False)
            if hull_mods:
                matches = re.findall(r'\[\[(.*?)]]', hull_mods)
                variant['Hullmods'] = matches

            weapons = variant.get('Weapons & Fighters', False)
            if weapons:
                expanded_list = []
                pattern = re.compile(r'(\d+)x\s*\[\[(.*?)]]')

                for line in weapons.split('\n'):
                    match = pattern.search(line)
                    if match:
                        count = int(match.group(1))
                        name = match.group(2)
                        expanded_list.extend([name] * count)

                variant['Weapons & Fighters'] = expanded_list

        return variants
