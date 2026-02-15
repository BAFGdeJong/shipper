use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct WeaponSlot {
    pub angle: Option<i64>,
    pub arc: Option<i64>,
    pub id: String,
    pub locations: Option<Vec<i64>>,
    pub mount: String,
    pub size: String,
    pub type_: String
}

impl WeaponSlot {
    pub fn new(
        angle: Option<i64>,
        arc: Option<i64>,
        id: String,
        locations: Option<Vec<i64>>,
        mount: String,
        size: String,
        type_: String
    ) -> Self {
        Self {
            angle,
            arc,
            id,
            locations,
            mount,
            size,
            type_
        }
    }
}