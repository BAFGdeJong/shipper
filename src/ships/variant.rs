use std::collections::HashMap;
use serde::Serialize;
use serde_json::Value;
use crate::io::ParsePlan;
use crate::ships::weapon::Weapon;
use crate::ships::weapon_group::WeaponGroup;
use crate::ships::wing::Wing;

#[derive(Serialize, Debug)]
pub struct Variant {
    pub display_name: String,
    pub hull_id: String,
    pub variant_id: String,
    pub goal_variant: bool,
    pub flux_capacitors: i64,
    pub flux_vents: i64,
    pub hull_mods: Vec<String>,
    pub perma_mods: Vec<String>,
    pub s_mods: Vec<String>,
    pub weapon_groups: Vec<WeaponGroup>,
    pub wings: Vec<Wing>,
} impl Variant {
    pub fn new(
        display_name: String,
        hull_id: String,
        variant_id: String,
        goal_variant: bool,
        flux_capacitors: i64,
        flux_vents: i64,
        hull_mods: Vec<String>,
        perma_mods: Vec<String>,
        s_mods: Vec<String>,
        weapon_groups: Vec<WeaponGroup>,
        wings: Vec<Wing>,
    ) -> Self {
        Self {
            display_name,
            hull_id,
            variant_id,
            goal_variant,
            flux_capacitors,
            flux_vents,
            hull_mods,
            perma_mods,
            s_mods,
            weapon_groups,
            wings,
        }
    }
}

impl ParsePlan<(&HashMap<String, String>, &HashMap<String, String>)> for Variant {
    fn plan(json: &Value, ctx: &(&HashMap<String, String>, &HashMap<String, String>)) -> Option<Self> {
        let (hull_mods_map, weapons_map) = ctx;

        Some(Variant::new(
            json["displayName"].as_str().unwrap_or("Unknown").to_string(),
            json["hullId"].as_str().unwrap_or("").to_string(),
            json["variantId"].as_str().unwrap_or("").to_string(),
            json["goalVariant"].as_bool().unwrap_or(false),
            json["fluxCapacitors"].as_i64().unwrap_or(0),
            json["fluxVents"].as_i64().unwrap_or(0),

            json["hullMods"]
                .as_array()
                .map(|arr| {
                    arr.iter()
                        .map(|e| {
                            let id = e.as_str().unwrap_or("");
                            hull_mods_map.get(id).cloned().unwrap_or_else(|| id.to_string())
                        })
                        .collect()
                })
                .unwrap_or_else(Vec::new),

            json["permaMods"]
                .as_array()
                .map(|arr| arr.iter().map(|e| e.as_str().unwrap_or("").to_string()).collect())
                .unwrap_or_else(Vec::new),

            json["sMods"]
                .as_array()
                .map(|arr| arr.iter().map(|e| e.as_str().unwrap_or("").to_string()).collect())
                .unwrap_or_else(Vec::new),

            json["weaponGroups"]
                .as_array()
                .unwrap_or(&Vec::new())
                .iter()
                .map(|group_json| WeaponGroup::new(
                    group_json["autofire"].as_bool().unwrap_or(false),
                    group_json["mode"].as_str().unwrap_or("LINKED").to_string(),

                    group_json["weapons"]
                        .as_object()
                        .unwrap_or(&serde_json::Map::new())
                        .iter()
                        .map(|(slot_id, weapon_id_json)| {
                            let weapon_id = weapon_id_json.as_str().unwrap_or("");
                            let weapon_name = weapons_map.get(weapon_id)
                                .cloned()
                                .unwrap_or_else(|| weapon_id.to_string());

                            Weapon::new(slot_id.clone(), weapon_name)
                        })
                        .collect(),
                ))
                .collect(),

            json["wings"]
                .as_array()
                .map(|v| v.as_slice())
                .unwrap_or(&[])
                .iter()
                .map(|wing_id_json| Wing::new(
                    wing_id_json.as_str().unwrap_or("").to_string(),
                    "".to_string(),
                    "".to_string(),
                ))
                .collect(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*; // Import Variant and ParsePlan
    use serde_json::json;
    use std::collections::HashMap;

    #[test]
    fn test_parse_astral_elite_variant() {
        let mut mock_hull_mods = HashMap::new();
        mock_hull_mods.insert("expanded_deck_crew".to_string(), "Expanded Deck Crew".to_string());

        let mut mock_weapons = HashMap::new();
        mock_weapons.insert("squall".to_string(), "Squall MLRS".to_string());
        mock_weapons.insert("gravitonbeam".to_string(), "Graviton Beam".to_string());
        mock_weapons.insert("pdlaser".to_string(), "PD Laser".to_string());

        let ctx = (&mock_hull_mods, &mock_weapons);

        let json_input = json!({
            "displayName": "Elite",
            "fluxCapacitors": 50,
            "fluxVents": 18,
            "goalVariant": true,
            "hullId": "astral",
            "hullMods": ["expanded_deck_crew"],
            "permaMods": [],
            "sMods": [],
            "variantId": "astral_Elite",
            "weaponGroups": [
                {
                    "autofire": false,
                    "mode": "ALTERNATING",
                    "weapons": {
                        "WS 011": "squall",
                        "WS 012": "squall"
                    }
                },
                {
                    "autofire": true,
                    "mode": "LINKED",
                    "weapons": {
                        "WS 013": "gravitonbeam",
                        "WS 014": "gravitonbeam",
                        "WS 015": "gravitonbeam",
                        "WS 023": "gravitonbeam",
                        "WS 024": "gravitonbeam"
                    }
                },
                {
                    "autofire": true,
                    "mode": "LINKED",
                    "weapons": {
                        "WS 005": "pdlaser",
                        "WS 006": "pdlaser",
                        "WS 007": "pdlaser",
                        "WS 008": "pdlaser"
                    }
                }
            ],
            "wings": [
                "trident_wing",
                "trident_wing",
                "longbow_wing",
                "longbow_wing",
                "broadsword_wing",
                "broadsword_wing"
            ]
        });

        let variant = Variant::plan(&json_input, &ctx)
            .expect("Failed to parse Astral Elite variant");


        assert_eq!(variant.display_name, "Elite");
        assert_eq!(variant.hull_id, "astral");
        assert_eq!(variant.flux_capacitors, 50);
        assert_eq!(variant.flux_vents, 18);

        assert_eq!(variant.hull_mods.len(), 1);
        assert_eq!(variant.hull_mods[0], "Expanded Deck Crew");

        assert_eq!(variant.wings.len(), 6);
        assert_eq!(variant.wings[0].hull_id, "trident_wing");

        assert_eq!(variant.weapon_groups.len(), 3);

        let group1 = &variant.weapon_groups[0];
        assert_eq!(group1.mode, "ALTERNATING");
        assert_eq!(group1.weapons.len(), 2);

        let has_squall = group1.weapons.iter().any(|w| w.id == "Squall MLRS");
        assert!(has_squall, "Expected weapon name 'Squall MLRS' not found in group 1");

        // Group 2: Gravitons (LINKED)
        let group2 = &variant.weapon_groups[1];
        assert_eq!(group2.mode, "LINKED");
        assert!(group2.autofire);
        let has_graviton = group2.weapons.iter().any(|w| w.id == "Graviton Beam");
        assert!(has_graviton, "Expected 'Graviton Beam' in group 2");
    }
}


