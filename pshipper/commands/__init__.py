import shipper

import random

from .generate import generate_variant_table
from .check import validate_wiki_ship_info
from .view_ship import view_ship

from pshipper.views.json_tree import json_tree


def view_hull_mod(starsector_data_dir, hull_mod, key_by, is_random):
    m = shipper.get_hull_mods(starsector_data_dir, key_by)
    title = "Hull Mod"
    if is_random:
        json_tree(random.choice(list(m.values())))
    else:
        json_tree(m.get(hull_mod, {}), title)

def view_ship_system(starsector_data_dir, ship_system, key_by, is_random):
    m = shipper.get_ship_systems(starsector_data_dir, key_by)
    title = "Ship System"
    if is_random:
        json_tree(random.choice(list(m.values())))
    else:
        json_tree(m.get(ship_system, {}), title)