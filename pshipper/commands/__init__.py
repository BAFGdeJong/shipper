import shipper

from .generate import generate_variant_table
from .check import validate_wiki_ship_info
from .view_ship import view_ship

from pshipper.views.json_tree import json_tree


def view_hull_mod(starsector_data_dir, hull_mod, key_by):
    json_tree(shipper.get_hull_mods(starsector_data_dir, key_by).get(hull_mod, {}))

def view_ship_system(starsector_data_dir, ship_system, key_by):
    json_tree(shipper.get_ship_systems(starsector_data_dir, key_by).get(ship_system, {}))