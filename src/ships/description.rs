use serde::{Deserialize, Serialize};
use crate::io::CSVLoad;
use crate::ships::ship_data::ShipData;

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub struct Description {
    #[serde(alias = "id")]
    pub id: Option<String>,

    #[serde(alias = "type")]
    pub type_: Option<String>,

    #[serde(alias = "text1")]
    pub text: Option<String>,

    #[serde(alias = "text2")]
    pub text2: Option<String>,

    #[serde(alias = "text3")]
    pub text3: Option<String>,

    #[serde(alias = "text4")]
    pub text4: Option<String>,

    #[serde(alias = "text5")]
    pub text5: Option<String>,
}
impl Description {
    fn to_json(&self) -> serde_json::Result<String> {
        serde_json::ser::to_string_pretty(&self)
    }
}
impl CSVLoad for Description {
    fn get_field(&self, key: &str) -> Option<String> {
        match key {
            "id" => Some(self.id.clone()?),
            _ => None
        }
    }
}