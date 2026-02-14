use serde::Serialize;

#[derive(Serialize, Debug)]
pub struct Weapon {
    pub ws: String,
    pub id: String,
} impl Weapon {
    pub fn new(
        ws: String,
        id: String
    ) -> Self {
        Self {
            ws,
            id,
        }
    }
}
