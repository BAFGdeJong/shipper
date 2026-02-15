use crate::io::bool_from_str;
use serde::{Deserialize, Serialize};
use crate::io::CSVLoad;

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "snake_case", default)]
#[derive(Default)]
pub struct ShipSystemData {
    #[serde(alias = "name")]
    pub name: Option<String>,

    #[serde(alias = "id")]
    pub id: Option<String>,

    #[serde(alias = "flux/second")]
    pub flux_per_second: Option<f64>,

    #[serde(alias = "f/s (base rate)")]
    pub flux_per_second_base_rate: Option<f64>,

    #[serde(alias = "f/s (base cap)")]
    pub flux_per_second_base_cap: Option<f64>,

    #[serde(alias = "flux/use")]
    pub flux_per_use: Option<f64>,

    #[serde(alias = "f/u (base rate)")]
    pub flux_per_use_base_rate: Option<f64>,

    #[serde(alias = "f/u (base cap)")]
    pub flux_per_use_base_cap: Option<f64>,

    #[serde(alias = "cr/u")]
    pub cr_per_use: Option<f64>,

    #[serde(alias = "max uses")]
    pub max_uses: Option<f64>,

    #[serde(alias = "regen")]
    pub regen: Option<f64>,

    #[serde(alias = "charge up")]
    pub charge_up: Option<f64>,

    #[serde(alias = "active")]
    pub active: Option<f64>,

    #[serde(alias = "down")]
    pub down: Option<f64>,

    #[serde(alias = "cooldown")]
    pub cooldown: Option<f64>,

    #[serde(alias = "toggle", deserialize_with = "bool_from_str")]
    pub toggle: Option<bool>,

    #[serde(alias = "noDissipation", deserialize_with = "bool_from_str")]
    pub no_dissipation: Option<bool>,

    #[serde(alias = "noHardDissipation", deserialize_with = "bool_from_str")]
    pub no_hard_dissipation: Option<bool>,

    #[serde(alias = "hardFlux", deserialize_with = "bool_from_str")]
    pub hard_flux: Option<bool>,

    #[serde(alias = "noFiring", deserialize_with = "bool_from_str")]
    pub no_firing: Option<bool>,

    #[serde(alias = "noTurning", deserialize_with = "bool_from_str")]
    pub no_turning: Option<bool>,

    #[serde(alias = "noStrafing", deserialize_with = "bool_from_str")]
    pub no_strafing: Option<bool>,

    #[serde(alias = "noAccel", deserialize_with = "bool_from_str")]
    pub no_accel: Option<bool>,

    #[serde(alias = "noShield", deserialize_with = "bool_from_str")]
    pub no_shield: Option<bool>,

    #[serde(alias = "noVent", deserialize_with = "bool_from_str")]
    pub no_vent: Option<bool>,

    #[serde(alias = "isPhaseCloak", deserialize_with = "bool_from_str")]
    pub is_phase_cloak: Option<bool>,

    #[serde(alias = "tags")]
    pub tags: Option<String>,

    #[serde(alias = "icon")]
    pub icon: Option<String>,
}
impl CSVLoad for ShipSystemData {
    fn get_field(&self, key: &str) -> Option<String> {
        match key {
            "name" => Some(self.name.clone()?),
            "id" => Some(self.id.clone()?),
            _ => None
        }
    }
}