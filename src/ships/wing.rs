use serde::Serialize;

#[derive(Serialize, Debug)]
pub struct Wing {
    pub hull_id: String,
    pub name: String,
    pub display_name: String
} impl Wing {
    pub fn new(
        hull_id: String,
        name: String,
        display_name: String,
    ) -> Self {
        Self {
            hull_id,
            name,
            display_name,
        }
    }
}
