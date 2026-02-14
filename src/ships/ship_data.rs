use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io;
use std::path::Path;
use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub struct ShipData {
    // #[serde(alias = "name")]
    // pub name: Option<String>,

    // #[serde(alias = "id")]
    // pub id: Option<String>,

    #[serde(alias = "designation")]
    pub designation: Option<String>,

    #[serde(alias = "tech/manufacturer")]
    pub tech_manufacturer: Option<String>,

    #[serde(alias = "system id")]
    pub system_id: Option<String>,

    #[serde(alias = "codex variant id")]
    pub codex_variant_id: Option<String>,

    #[serde(alias = "fleet pts")]
    pub fleet_pts: Option<f64>,

    #[serde(alias = "hitpoints")]
    pub hitpoints: Option<f64>,

    #[serde(alias = "armor rating")]
    pub armor_rating: Option<f64>,

    #[serde(alias = "mass")]
    pub mass: Option<f64>,

    #[serde(alias = "max flux")]
    pub max_flux: Option<f64>,

    // This will now appear in Python as "flux_capacity_tiers"
    #[serde(alias = "8/6/5/4%")]
    pub flux_capacity_tiers: Option<f64>,

    #[serde(alias = "flux dissipation")]
    pub flux_dissipation: Option<f64>,

    #[serde(alias = "ordnance points")]
    pub ordnance_points: Option<f64>,

    #[serde(alias = "fighter bays")]
    pub fighter_bays: Option<f64>,

    #[serde(alias = "max speed")]
    pub max_speed: Option<f64>,

    #[serde(alias = "acceleration")]
    pub acceleration: Option<f64>,

    #[serde(alias = "deceleration")]
    pub deceleration: Option<f64>,

    #[serde(alias = "max turn rate")]
    pub max_turn_rate: Option<f64>,

    #[serde(alias = "turn acceleration")]
    pub turn_acceleration: Option<f64>,

    #[serde(alias = "travel drive")]
    pub travel_drive: Option<String>,

    #[serde(alias = "max burn")]
    pub max_burn: Option<f64>,

    #[serde(alias = "shield type")]
    pub shield_type: Option<String>,

    #[serde(alias = "defense id")]
    pub defense_id: Option<String>,

    #[serde(alias = "shield arc")]
    pub shield_arc: Option<f64>,

    #[serde(alias = "shield upkeep")]
    pub shield_upkeep: Option<f64>,

    #[serde(alias = "shield efficiency")]
    pub shield_efficiency: Option<f64>,

    #[serde(alias = "phase cost")]
    pub phase_cost: Option<f64>,

    #[serde(alias = "phase upkeep")]
    pub phase_upkeep: Option<f64>,

    // --- Crew & Logistics ---
    #[serde(alias = "min crew")]
    pub min_crew: Option<f64>,

    #[serde(alias = "max crew")]
    pub max_crew: Option<f64>,

    #[serde(alias = "cargo")]
    pub cargo_capacity: Option<f64>,

    #[serde(alias = "fuel")]
    pub fuel_capacity: Option<f64>,

    #[serde(alias = "fuel/ly")]
    pub fuel_per_lightyear: Option<f64>,

    #[serde(alias = "range")]
    pub range: Option<f64>,

    #[serde(alias = "base value")]
    pub base_value: Option<f64>,

    #[serde(alias = "cr %/day")]
    pub cr_percent_per_day: Option<f64>,

    #[serde(alias = "CR to deploy")]
    pub cr_to_deploy: Option<f64>,

    #[serde(alias = "peak CR sec")]
    pub peak_cr_sec: Option<f64>,

    #[serde(alias = "CR loss/sec")]
    pub cr_loss_per_sec: Option<f64>,

    #[serde(alias = "supplies/rec")]
    pub supplies_per_rec: Option<f64>,

    #[serde(alias = "supplies/mo")]
    pub supplies_per_month: Option<f64>,

    #[serde(alias = "c/s")]
    pub cargo_per_supply: Option<f64>,

    #[serde(alias = "c/f")]
    pub cargo_per_fuel: Option<f64>,

    #[serde(alias = "f/s")]
    pub fuel_per_supply: Option<f64>,

    #[serde(alias = "f/f")]
    pub fuel_per_fuel: Option<f64>,

    #[serde(alias = "crew/s")]
    pub crew_per_supply: Option<f64>,

    #[serde(alias = "crew/f")]
    pub crew_per_fuel: Option<f64>,

    #[serde(alias = "hints")]
    pub hints: Option<String>,

    #[serde(alias = "tags")]
    pub tags: Option<String>,

    #[serde(alias = "logistics n/a reason")]
    pub logistics_na_reason: Option<String>,

    #[serde(alias = "rarity")]
    pub rarity: Option<f64>,

    #[serde(alias = "breakProb")]
    pub break_prob: Option<f64>,

    #[serde(alias = "minPieces")]
    pub min_pieces: Option<f64>,

    #[serde(alias = "maxPieces")]
    pub max_pieces: Option<f64>,

    #[serde(alias = "number")]
    pub number: Option<f64>,

} impl ShipData {
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Vec<Self>, Box<dyn Error>> {
        let file = File::open(path)?;

        let mut rdr = csv::ReaderBuilder::new()
            .has_headers(true) // Line 1 is headers
            .from_reader(file);

        let mut ships = Vec::new();

        for result in rdr.deserialize() {
            match result {
                Ok(record) => {
                    ships.push(record);
                }
                Err(e) => {
                    eprintln!("Skipping invalid row: {}", e);
                }
            }
        }

        Ok(ships)
    }

    pub fn load_as_map<P: AsRef<Path>>(path: P, key_field: &str) -> Result<HashMap<String, Self>, Box<dyn Error>> {
        match Self::load(path) {
            Ok(vec) => {
                let mut ship_map = HashMap::new();
                for ship in vec {
                    let map_key = match key_field {
                        "id" => ship.id.clone(),
                        "name" => ship.name.clone(),
                        _ => {
                            return Err(Box::new(io::Error::new(
                                io::ErrorKind::InvalidInput,
                                format!("Field '{}' is not supported as a map key", key_field)
                            )));
                        }
                    };

                    if let Some(k) = map_key {
                        ship_map.insert(k, ship);
                    }

                }
                Ok(ship_map)
            },
            Err(e) => {
                Err(e)
            }
        }
    }

    fn to_json(&self) -> serde_json::Result<String> {
        serde_json::ser::to_string_pretty(&self)
    }

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_loading_csv() {
        // match ShipData::load("D:/NonSteamLibrary/Starsector/starsector-core/data/hulls/ship_data.csv") {
        //     Ok(ships) => {
        //         println!("{}", serde_json::ser::to_string_pretty(&ships).unwrap());
        //     }
        //     Err(e) => {
        //         eprintln!("Skipping invalid row: {}", e);
        //     }
        // }

        match ShipData::load_as_map("D:/NonSteamLibrary/Starsector/starsector-core/data/hulls/ship_data.csv", "id") {
            Ok(ships) => {
                // println!("{}", serde_json::ser::to_string_pretty(ships.get("warthog").unwrap()).unwrap());
                println!("{}", ships.get("warthog").unwrap().to_json().unwrap());
            }
            Err(_) => {

            }
        }

        // match ShipData::load("D:/NonSteamLibrary/Starsector/starsector-core/data/hulls/ship_data.csv") {
        //     Ok(ships) => {
        //         for ship in ships {
        //             if let Some(name) = ship.name {
        //                 println!("Ship name: {}", name);
        //             }
        //         }
        //     }
        //     Err(e) => {
        //         eprintln!("Critical error: {}", e);
        //     }
        // }

        // match ShipData::load("D:/NonSteamLibrary/Starsector/starsector-core/data/hulls/ship_data.csv") { // TODO don't hardcode
        //     Ok(ships) => {
        //         for ship in ships {
        //             if let Some(pts) = ship.fleet_pts {
        //                 println!("Loaded: {:?} ({} pts)", ship.name, pts);
        //             } else {
        //                 println!("Loaded: {:?} (Drone/Module - No points)", ship.name);
        //             }
        //         }
        //     },
        //     Err(e) => eprintln!("Critical Error: {}", e),
        // }
    }
}