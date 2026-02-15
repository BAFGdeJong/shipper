import shipper

from pshipper.views.json_tree import json_tree


def view_ship(starsector_data_dir, ship, key_by):
    ships = shipper.get_ships(starsector_data_dir, key_by)

    ship = ships.get(ship, None)

    if ship is None:
        return

    json_tree(ship, ship.get('name', ship.get('skin_id', None)))