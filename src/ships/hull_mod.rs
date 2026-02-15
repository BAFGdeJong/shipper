use crate::io::bool_from_str;
use serde::{Deserialize, Serialize};
use crate::io::CSVLoad;

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "snake_case", default)]
#[derive(Default)]
pub struct HullModData {

    #[serde(alias = "name")]
    pub name: Option<String>,

    #[serde(alias = "id")]
    pub id: Option<String>,

    #[serde(alias = "tier")]
    pub tier: Option<f64>,

    #[serde(alias = "rarity")]
    pub rarity: Option<f64>,

    #[serde(alias = "tech/manufacturer")]
    pub tech_manufacturer: Option<String>,

    #[serde(alias = "tags")]
    pub tags: Option<String>,

    #[serde(alias = "uiTags")]
    pub ui_tags: Option<String>,

    #[serde(alias = "base value")]
    pub base_value: Option<f64>,

    #[serde(alias = "unlocked", deserialize_with = "bool_from_str")]
    pub unlocked: Option<bool>,

    #[serde(alias = "hidden", deserialize_with = "bool_from_str")]
    pub hidden: Option<bool>,

    #[serde(alias = "hiddenEverywhere", deserialize_with = "bool_from_str")]
    pub hidden_everywhere: Option<bool>,

    #[serde(alias = "cost_frigate")]
    pub cost_frigate: Option<f64>,

    #[serde(alias = "cost_dest")]
    pub cost_dest: Option<f64>,

    #[serde(alias = "cost_cruiser")]
    pub cost_cruiser: Option<f64>,

    #[serde(alias = "cost_capital")]
    pub cost_capital: Option<f64>,

    #[serde(alias = "script")]
    pub script: Option<String>,

    #[serde(alias = "desc")]
    pub description: Option<String>,

    #[serde(alias = "short")]
    pub short_description: Option<String>,

    #[serde(alias = "sModDesc")]
    pub s_mod_description: Option<String>,

    #[serde(alias = "sprite")]
    pub sprite: Option<String>,
}
impl CSVLoad for HullModData {
    fn get_field(&self, key: &str) -> Option<String> {
        match key {
            "name" => Some(self.name.clone()?),
            "id" => Some(self.id.clone()?),
            _ => None
        }
    }
}