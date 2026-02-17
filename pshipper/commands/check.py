import logging
import os

import shipper
from dotenv import load_dotenv

from pshipper.views.dict_compare import compare_dicts
from pshipper.wiki.client import Client
from pshipper.utils import fix_d_variants
from pshipper.wiki.extract import extract_ship_info
from pshipper.wiki.login import Login
from pshipper.wiki.ship_mount import ShipMount

logger = logging.getLogger(__name__)

def validate_wiki_ship_info(starsector_data_dir, ships_to_validate, key_by, show_identical):
    client = Login.env()
    if client is None:
        logger.error("Could not login to Wiki")
        return

    ships = shipper.get_ships(starsector_data_dir, key_by)

    ship_names = [s.strip() for s in ships_to_validate.split(",") if s.strip() != '']
    r_ships = []
    for ship_name in ship_names:
        r_ships.append(ships.get(ship_name)) # TODO make this own function and error handling

    for ship in r_ships:
        if not ship:
            continue

        ship_name = ship.get('name', None)
        if not ship_name:
            continue

        text = client.get_page_text(ship_name)

        wiki_ship_info = extract_ship_info(text)

        wiki_ship_info.pop('AddDescription', None)
        wiki_ship_info.pop('Image', None)
        ship_in_wiki_format = convert_to_wiki_ship_format(ship)

        compare_dicts(wiki_ship_info, ship_in_wiki_format, ship_name, show_identical)


def safe_int(val, default=0):
    """Safely converts a value to int, defaulting to 0 if None."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def safe_float(val, default=0.0):
    """Safely converts a value to float, defaulting to 0.0 if None."""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def convert_to_wiki_ship_format(ship):
    new_ship = {}

    new_ship.update({'Name': ship.get('name')})
    new_ship.update({'ID': ship.get('hull_id')})
    new_ship.update({'Designation': ship.get('designation')})

    weapon_mounts = [ShipMount.from_game_data(x) for x in ship.get('weapon_slots')]

    fb = ship.get('fighter_bays', None)
    if fb:
        new_ship.update({'FighterBays': fb})

    weapon_mounts = [x.to_dict() for x in ShipMount.consolidate_mounts(weapon_mounts) if
                     ((x.mount_type == "TURRET" or x.mount_type == "HARDPOINT") and x.type_ != "DECORATIVE")]

    new_ship.update({'Mounts': ShipMount.sort_mounts(weapon_mounts)})

    new_ship.update({'HullSize': ship.get('hull_size').split("_")[0].title()})
    new_ship.update({'DesignType': ship.get('tech_manufacturer')})

    hull_mods = ship.get('hull_mods')
    if hull_mods:
        hmods = []
        for mod in hull_mods:
            hmods.append(mod.get('name'))
        new_ship.update({'Hullmods': hmods.sort()})

    new_ship.update({'HullIntegrity': safe_int(ship.get('hitpoints'))})
    new_ship.update({'ArmorRating': safe_int(ship.get('armor_rating'))})
    new_ship.update({'FluxCapacity': safe_int(ship.get('max_flux'))})
    new_ship.update({'FluxDissipation': safe_int(ship.get('flux_dissipation'))})
    new_ship.update({'OrdnancePoints': safe_int(ship.get('ordnance_points'))})
    new_ship.update({'PeakPerformance': safe_int(ship.get('peak_cr_sec'))})
    new_ship.update({'System': ship.get('system_id')})

    dissipation = safe_float(ship.get('flux_dissipation'))
    upkeep_ratio = safe_float(ship.get('shield_upkeep'))

    if ship.get('shield_upkeep') is not None:
        new_ship.update({'ShieldUpkeep': int(dissipation * upkeep_ratio)})
    else:
        new_ship.update({'ShieldUpkeep': 0})

    new_ship.update({'ShieldArc': safe_int(ship.get('shield_arc'))})
    new_ship.update({'ShieldFluxPerDamage': safe_float(ship.get('shield_efficiency'))})

    shield_map = { # TODO move to file to have one source of truth
        'FRONT': 'Front Shield',
        'OMNI': 'Omni Shield',
        'PHASE': 'Phase Coil'
    }

    new_ship.update({'Defense': shield_map.get(ship.get('shield_type'), 'None')})

    new_ship.update({'TopSpeed': safe_int(ship.get('max_speed'))})
    new_ship.update({'Acceleration': safe_int(ship.get('acceleration'))})
    new_ship.update({'Deceleration': safe_int(ship.get('deceleration'))})
    new_ship.update({'TurnRate': safe_int(ship.get('max_turn_rate'))})
    new_ship.update({'TurnAcceleration': safe_int(ship.get('turn_acceleration'))})
    new_ship.update({'Mass': safe_int(ship.get('mass'))})
    new_ship.update({'MaximumBurn': safe_int(ship.get('max_burn'))})

    new_ship.update({'BaseValue': safe_int(ship.get('base_value'))})
    new_ship.update({'FleetPoints': safe_int(ship.get('fleet_pts'))})
    new_ship.update({'DeploymentPoints': safe_int(ship.get('supplies_per_rec'))})
    new_ship.update({'RecoveryCost': safe_int(ship.get('supplies_per_rec'))})
    new_ship.update({'RecoveryRate': safe_int(ship.get('cr_percent_per_day'))})
    new_ship.update({'CRPerDeployment': safe_int(ship.get('cr_to_deploy'))})
    new_ship.update({'Maintenance': safe_int(ship.get('supplies_per_month'))})

    new_ship.update({'FuelCapacity': safe_int(ship.get('fuel_capacity'))})
    new_ship.update({'FuelPerLY': safe_int(ship.get('fuel_per_lightyear'))})
    new_ship.update({'CargoCapacity': safe_int(ship.get('cargo_capacity'))})
    new_ship.update({'MaximumCrew': safe_int(ship.get('max_crew'))})
    new_ship.update({'SkeletonCrew': safe_int(ship.get('min_crew'))})

    new_ship.update({'Hints': ship.get('hints') or ''})
    new_ship.update({'Tags': ship.get('tags') or ''})
    new_ship.update({'Rarity': ship.get('rarity') or ''})

    desc = ship.get('description', None)
    texts = []
    if desc:
        texts.append(desc.get('text'))
        texts.append(desc.get('text2'))
        texts.append(desc.get('text2'))
        texts.append(desc.get('text3'))
        texts.append(desc.get('text4'))
        texts.append(desc.get('text5'))
        texts = [t for t in texts if t is not None or t != '']
        new_ship.update({'Description': texts[0]})

    system = ship.get('system', None)
    if system is not None:
        new_ship.update({'System': system.get('name', None)})

    return new_ship

def check_variant_table(args):
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

    client = Client(username, password)

    for ship in r_ships:
        ship_name = ship.get('name', None)

        if not ship_name:
            continue

        text = client.get_page_text(ship_name)

        print(text)