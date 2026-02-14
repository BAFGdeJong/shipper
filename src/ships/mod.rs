use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use serde::Serialize;
use crate::io::LoadPlan;
use crate::ships::ship::Ship;
use crate::ships::variant::Variant;

pub mod ship;
pub mod variant;
pub mod weapon;
pub mod weapon_group;
mod wing;

#[derive(Serialize)]
pub struct Data {
    data_folder: String,
    hulls_folder: String,
    variants_folder: String,
    weapons_folder: String,
    hull_mods_folder: String,
    ship_systems_folder: String,
    pub ships: HashMap<String, Ship>,
}

impl Data {
    pub fn new(data_folder: &str, key_by: &str) -> Self {
        let mut dt = Self {
            data_folder: data_folder.to_string(),
            hulls_folder: format!("{}hulls/", data_folder),
            variants_folder: format!("{}variants/", data_folder),
            weapons_folder: format!("{}weapons/", data_folder),
            hull_mods_folder: format!("{}hullmods/", data_folder),
            ship_systems_folder: format!("{}shipsystems/", data_folder),
            ships: HashMap::new(),
        };

        dt.map(key_by);

        dt
    }

    fn map(&mut self, key_type: &str) {
        // let ship_data_csv = Self::load_csv(&format!("{}ship_data.csv", &self.hulls_folder)).unwrap_or_default();
        let weapons_data_csv = Self::load_csv(&format!("{}weapon_data.csv", &self.weapons_folder)).unwrap_or_default();
        let hull_mods_csv = Self::load_csv(&format!("{}hull_mods.csv", &self.hull_mods_folder)).unwrap_or_default();

        let mut ships = Ship::load_folder(&self.hulls_folder, &["ship", "skin"], &());
        let mut variants = Variant::load_folder(&self.variants_folder, &["variant"], &(&hull_mods_csv, &weapons_data_csv));

        let mut hull_to_name: HashMap<String, String> = HashMap::new();
        for ship in &ships {
            hull_to_name.insert(ship.hull_id.clone(), ship.name.clone());
            hull_to_name.insert(format!("{}_wing", ship.hull_id), ship.name.clone());
        }

        let mut hull_to_variant_dn: HashMap<String, String> = HashMap::new();
        for v in &variants {
            hull_to_variant_dn.entry(v.hull_id.clone()).or_insert(v.display_name.clone());
            hull_to_variant_dn.entry(format!("{}_wing", v.hull_id)).or_insert(v.display_name.clone());
        }

        for variant in &mut variants {
            if !variant.wings.is_empty() {
                for wing in &mut variant.wings {
                    if let Some(name) = hull_to_name.get(&wing.hull_id) {
                        wing.name = name.clone();
                    }

                    if let Some(dn) = hull_to_variant_dn.get(&wing.hull_id) {
                        wing.display_name = dn.clone();
                    }
                }
            }
        }

        let mut skin_to_index: HashMap<String, usize> = HashMap::new();
        for (index, ship) in ships.iter().enumerate() {
            skin_to_index.insert(ship.skin_id.clone(), index);
        }

        for variant in variants {
            if let Some(&index) = skin_to_index.get(&variant.hull_id) {
                ships[index].add_variant(variant);
            }
        }

        match key_type {
            "name" => {
                for ship in ships { self.ships.insert(ship.name.clone(), ship); }
            }
            "hull_id" => {
                for ship in ships { self.ships.insert(ship.hull_id.clone(), ship); }
            }
            "skin_id" => {
                for ship in ships { self.ships.insert(ship.skin_id.clone(), ship); }
            }
            _ => {}
        }
    }

    fn load_csv(csv: &str) -> Result<HashMap<String, String>, Box<dyn Error>> {
        let file = File::open(csv)?;

        let mut rdr = csv::Reader::from_reader(file);
        let mut map = HashMap::new();

        for result in rdr.deserialize() {
            let record: RawCsv = result?;

            map.insert(record.id, record.name);
        }

        Ok(map)
    }


}

#[derive(Debug, serde::Deserialize)]
struct RawCsv {
    name: String,
    id: String,
}

