def fix_d_variants(ships):
    # Attach (D) variants to main variant
    for name in list(ships.keys()):

        if name not in ships:
            continue

        ship = ships[name]
        d_variant_name = name + ' (D)'

        if d_variant_name in ships:
            d_variant = ships.pop(d_variant_name)
            base_variants = ship.get('variants', [])
            d_variants = d_variant.get('variants', [])
            base_variants.extend(d_variants)
            ship['variants'] = base_variants

    return ships
