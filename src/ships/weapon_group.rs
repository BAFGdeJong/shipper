use serde::Serialize;
use crate::ships::weapon::Weapon;

#[derive(Serialize, Debug)]
pub struct WeaponGroup {
    pub autofire: bool,
    pub mode: String,
    pub weapons: Vec<Weapon>,
} impl WeaponGroup {
    pub fn new(
        autofire: bool,
        mode: String,
        weapons: Vec<Weapon>,
    ) -> Self {
        Self {
            autofire,
            mode,
            weapons,
        }
    }
}
