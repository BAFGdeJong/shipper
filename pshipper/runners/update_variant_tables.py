import logging
import time
import shipper
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

from pshipper.editors.editor import Editor

logger = logging.getLogger(__name__)

def sync_variants_to_wiki(
        editor: Editor,
        starsector_data_folder: Path,
        ship_whitelist: List[str],
        notes: Dict,
        template,
        collapse_whitelist: list,
        collapse_limit: int,
        rate_limit_delay: float = 2.5
) -> None:
    logger.info("Loading ship data from game files...")
    ships = shipper.get_ships(starsector_data_folder, "name")
    bar = tqdm(ship_whitelist, desc="Updating wiki tables...")

    for ship_name in bar:
        ship_data = ships.get(ship_name, None)

        if not ship_data:
            logger.warning(f"Skipping '{ship_name}': Data not found in game files.")
            continue

        bar.set_description(f"Updating '{ship_name}'...")

        try:
            editor.add_ship_variants(ship_data, notes, template, collapse_whitelist, collapse_limit)
            time.sleep(rate_limit_delay)

        except Exception as e:
            logger.error(f"Failed to update '{ship_name}': {e}")
            time.sleep(rate_limit_delay * 2)

    print(f"Finished updating all pages.")
