use serde::Serialize;
use serde_json::Value;
use crate::io::ParsePlan;
use crate::ships::variant::Variant;

#[derive(Serialize, Debug)]
pub struct Ship {
    pub hull_id: String,
    pub skin_id: String,
    pub name: String,
    pub variants: Vec<Variant>
}

impl Ship {
    pub fn new(hull_id: String, skin_id: String, name: String, variants: Vec<Variant>) -> Self {
        Self { hull_id, skin_id, name, variants }
    }

    pub fn add_variant(&mut self, variant: Variant) {
        self.variants.push(variant);
    }
}

impl ParsePlan<()> for Ship {

    fn from_value(json: &Value, _ctx: &()) -> Option<Self> {

        let hull_id = json["hullId"].as_str()
            .or_else(|| json["baseHullId"].as_str())
            .unwrap_or("")
            .to_string();

        let skin_id = json["skinHullId"].as_str()
            .or_else(|| json["hullId"].as_str())
            .unwrap_or("")
            .to_string();

        let name = json["hullName"].as_str().unwrap_or("").to_string();

        Some(Ship::new(
            hull_id,
            skin_id,
            name,
            vec![]
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn test_parse_base_hull_astral() {
        let json_input = json!({
            "bounds": [ 242, 69, 221, 80 ],
            "hullId": "astral",
            "hullName": "Astral",
            "hullSize": "CAPITAL_SHIP",
            "spriteName": "graphics/ships/astral/astral.png",
            "style": "HIGH_TECH",
            "width": 320
        });

        let ship = Ship::from_value(&json_input, &())
            .expect("Failed to parse Astral");

        assert_eq!(ship.hull_id, "astral");

        assert_eq!(ship.skin_id, "astral");

        assert_eq!(ship.name, "Astral");
        assert_eq!(ship.variants.len(), 0);
    }

    #[test]
    fn test_parse_skin_eagle_xiv() {
        let json_input = json!({
            "baseHullId": "eagle",
            "skinHullId": "eagle_xiv",
            "hullName": "Eagle (XIV)",
            "descriptionId": "eagle",
            "tags": ["XIV_bp"],
            "tech": "XIV Battlegroup",
            "fleetPoints": 17,
            "spriteName": "graphics/ships/eagle/eagle_hegemony.png",
            "builtInMods": ["fourteenth"]
        });

        let ship = Ship::from_value(&json_input, &())
            .expect("Failed to parse Eagle XIV skin");

        assert_eq!(ship.hull_id, "eagle");

        assert_eq!(ship.skin_id, "eagle_xiv");

        assert_eq!(ship.name, "Eagle (XIV)");
    }
}
