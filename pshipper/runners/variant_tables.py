import logging
import time
import shipper
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

from pshipper.editors.editor import Editor
from pshipper.utils import fix_d_variants

logger = logging.getLogger(__name__)

def sync_variants_to_wiki(
        editor: Editor,
        starsector_data_folder: Path,
        update_ships: List[str],
        ship_whitelist: List[str],
        notes: Dict,
        template,
        collapse_whitelist: list,
        collapse_limit: int,
        rate_limit_delay: float = 2.5,
        update: bool = False,
) -> None:
    logger.info("Loading ship data from game files...")
    ships = shipper.get_ships(starsector_data_folder, "name")
    fix_d_variants(ships)

    if len(update_ships) > 0:
        update_ships = [ship for ship in update_ships if ship in ship_whitelist]
        bar = tqdm(update_ships, desc="Updating wiki tables...")
    else:
        bar = tqdm(ship_whitelist, desc="Updating wiki tables...")

    for ship_name in bar:
        ship_data = ships.get(ship_name, None)

        if ship_data is None:
            logger.warning(f"Could not find ship '{ship_name}'.")
            bar.set_description(f"Could not find ship '{ship_name}'.")
            continue

        bar.set_description(f"Updating '{ship_name}'...")

        try:
            if update:
                bar.set_description(editor.update_ship_variants(ship_data, notes, template, collapse_whitelist, collapse_limit))
            else:
                editor.add_ship_variants(ship_data, notes, template, collapse_whitelist, collapse_limit)
            time.sleep(rate_limit_delay)

        except Exception as e:
            logger.error(f"Failed to update '{ship_name}': {e}")
            time.sleep(rate_limit_delay * 2)

    print(f"Finished updating all pages.")
