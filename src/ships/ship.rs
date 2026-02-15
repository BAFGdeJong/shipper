use std::collections::HashMap;
use serde::Serialize;
use serde_json::Value;
use crate::io::ParsePlan;
use crate::ships::description::Description;
use crate::ships::hull_mod::HullModData;
use crate::ships::ship_data::ShipData;
use crate::ships::ship_system::{ShipSystemData};
use crate::ships::variant::Variant;
use crate::ships::weapon_slot::WeaponSlot;

#[derive(Serialize, Debug)]
pub struct Ship {
    pub hull_id: String,
    pub skin_id: String,
    pub name: String,
    pub hull_size: String,
    pub weapon_slots: Vec<WeaponSlot>,
    pub system: Option<ShipSystemData>,
    pub hull_mods: Vec<Option<HullModData>>,

    #[serde(flatten)]
    pub data: Option<ShipData>,

    pub description: Option<Description>,

    pub variants: Vec<Variant>
}

impl Ship {
    pub fn new(
        hull_id: String,
        skin_id: String,
        name: String,
        hull_size: String,
        weapon_slots: Vec<WeaponSlot>,
        system: Option<ShipSystemData>,
        hull_mods: Vec<Option<HullModData>>,
        data: Option<ShipData>,
        description: Option<Description>,
        variants: Vec<Variant>
    ) -> Self {
        Self { hull_id, skin_id, name, hull_size, weapon_slots, system, hull_mods, data, description, variants }
    }

    pub fn add_variant(&mut self, variant: Variant) {
        self.variants.push(variant);
    }
}

type ShipStatsMap = HashMap<String, ShipData>;
type DescriptionsMap = HashMap<String, Description>;
type ShipSystemsMap = HashMap<String, ShipSystemData>;
type HullModMap = HashMap<String, HullModData>;
impl<'a> ParsePlan<(&'a ShipStatsMap, &'a DescriptionsMap, &'a ShipSystemsMap, &'a HullModMap)> for Ship {

    fn plan(json: &Value, ctx: &(&ShipStatsMap, &DescriptionsMap, &ShipSystemsMap, &HullModMap)) -> Option<Self> {
        let hull_id = json["hullId"].as_str()
            .or_else(|| json["baseHullId"].as_str())
            .unwrap_or("")
            .to_string();

        let skin_id = json["skinHullId"].as_str()
            .or_else(|| json["hullId"].as_str())
            .unwrap_or("")
            .to_string();

        let name = json["hullName"].as_str().unwrap_or("").to_string();

        let hull_size = json["hullSize"].as_str().unwrap_or("").to_string();

        let weapon_slots: Vec<WeaponSlot> = json["weaponSlots"]
            .as_array()
            .unwrap_or(&vec![])
            .iter()
            .map(|e|
                WeaponSlot::new(
                    e["angle"].as_i64(),
                    e["arc"].as_i64(),
                    e["id"].as_str().unwrap_or("").to_string(),
                    serde_json::from_value(e["locations"].clone()).unwrap_or(None),
                    e["mount"].as_str().unwrap_or("").to_string(),
                    e["size"].as_str().unwrap_or("").to_string(),
                    e["type"].as_str().unwrap_or("").to_string()
                )
            ).collect();

        let stats = ctx.0.get(&hull_id).cloned(); // TODO remove clone
        let description = ctx.1.get(&hull_id).cloned();

        let system_id = stats.as_ref()
            .and_then(|s| s.system_id.clone())
            .unwrap_or_default();

        let systems = ctx.2.get(&system_id).cloned();

        let mut hull_mods: Vec<Option<HullModData>> = vec![];

        let built_in_mods = json["builtInMods"].as_array();

        if let Some(mods_array) = built_in_mods {
            for e in mods_array {
                if let Some(mod_id) = e.as_str() {
                    hull_mods.push(ctx.3.get(mod_id).cloned());
                }
            }
        }

        Some(Ship::new(
            hull_id,
            skin_id,
            name,
            hull_size,
            weapon_slots,
            systems,
            hull_mods,
            stats,
            description,
            vec![]
        ))
    }

}

// #[cfg(test)]
// mod tests {
//     use super::*;
//     use serde_json::json;
//
//     #[test]
//     fn test_parse_base_hull_astral() {
//         let json_input = json!({
//             "bounds": [ 242, 69, 221, 80 ],
//             "hullId": "astral",
//             "hullName": "Astral",
//             "hullSize": "CAPITAL_SHIP",
//             "spriteName": "graphics/ships/astral/astral.png",
//             "style": "HIGH_TECH",
//             "width": 320
//         });
//
//         let ship = Ship::from_value(&json_input, &())
//             .expect("Failed to parse Astral");
//
//         assert_eq!(ship.hull_id, "astral");
//
//         assert_eq!(ship.skin_id, "astral");
//
//         assert_eq!(ship.name, "Astral");
//         assert_eq!(ship.variants.len(), 0);
//     }
//
//     #[test]
//     fn test_parse_skin_eagle_xiv() {
//         let json_input = json!({
//             "baseHullId": "eagle",
//             "skinHullId": "eagle_xiv",
//             "hullName": "Eagle (XIV)",
//             "descriptionId": "eagle",
//             "tags": ["XIV_bp"],
//             "tech": "XIV Battlegroup",
//             "fleetPoints": 17,
//             "spriteName": "graphics/ships/eagle/eagle_hegemony.png",
//             "builtInMods": ["fourteenth"]
//         });
//
//         let ship = Ship::from_value(&json_input, &())
//             .expect("Failed to parse Eagle XIV skin");
//
//         assert_eq!(ship.hull_id, "eagle");
//
//         assert_eq!(ship.skin_id, "eagle_xiv");
//
//         assert_eq!(ship.name, "Eagle (XIV)");
//     }
// }
