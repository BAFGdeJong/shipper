pub mod json;

pub use json::Json;

pub trait Clean<T> {
    fn clean(&self) -> Result<T, Box<dyn std::error::Error>>;
}
