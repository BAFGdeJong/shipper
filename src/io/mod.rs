use std::collections::HashMap;
use std::error::Error;
use std::{fs};
use std::fs::File;
use std::path::Path;
use serde::de::DeserializeOwned;
use serde::{Deserialize, Deserializer};
use serde_json::Value;
use crate::cleaner;
use crate::cleaner::Clean;

///
/// Dictates how the loaded file needs to be parsed.
///
pub trait ParsePlan<C>: Sized {
    fn plan(value: &Value, ctx: &C) -> Option<Self>;

    fn parse(path: &Path, ctx: &C) -> Option<Self> {
        let content = fs::read_to_string(path).ok()?;
        let valid_json: String = cleaner::Json::new(&content).clean().ok()?;
        let json_value: Value = serde_json::from_str(&valid_json).ok()?;
        Self::plan(&json_value, ctx)
    }
}

pub trait LoadPlan<C>: ParsePlan<C> {
    ///
    /// Load data from folder.
    ///
    fn load_folder(folder: &str, valid_extensions: &[&str], ctx: &C) -> Vec<Self> {
        let mut results = Vec::new();
        let path = Path::new(folder);
        if path.exists() {
            Self::recursive_walk(path, valid_extensions, ctx, &mut results);
        }
        results
    }

    fn recursive_walk(dir: &Path, exts: &[&str], ctx: &C, results: &mut Vec<Self>) {
        if let Ok(entries) = fs::read_dir(dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_dir() {
                    Self::recursive_walk(&path, exts, ctx, results);
                } else if path.is_file() {
                    if let Some(ext) = path.extension().and_then(|s| s.to_str()) {
                        if exts.contains(&ext) {
                            if let Some(item) = Self::parse(&path, ctx) {
                                results.push(item);
                            }
                        }
                    }
                }
            }
        }
    }
}

impl<C, T: ParsePlan<C>> LoadPlan<C> for T {}


pub fn bool_from_str<'de, D>(deserializer: D) -> Result<Option<bool>, D::Error>
where
    D: Deserializer<'de>,
{
    let s: Option<String> = Option::deserialize(deserializer)?;
    match s {
        Some(text) => {
            let lower = text.trim().to_lowercase();
            if lower == "true" {
                Ok(Some(true))
            } else if lower == "false" {
                Ok(Some(false))
            } else {
                Ok(None)
            }
        }
        None => Ok(None),
    }
}


pub trait CSVLoad: Sized + DeserializeOwned {
    fn get_field(&self, key: &str) -> Option<String>;

    fn load<P: AsRef<Path>>(path: P) -> Result<Vec<Self>, Box<dyn Error>>  {
        let file = File::open(path)?;

        let mut rdr = csv::ReaderBuilder::new()
            .has_headers(true) // Line 1 is headers
            .from_reader(file);

        let mut res = Vec::new();

        for result in rdr.deserialize() {
            match result {
                Ok(record) => {
                    res.push(record);
                }
                Err(_) => {
                    // TODO Silent fail
                    // eprintln!("Skipping invalid row: {}", e);
                }
            }
        }

        Ok(res)
    }

    fn load_as_map<P: AsRef<Path>>(path: P, key: &str) -> Result<HashMap<String, Self>, Box<dyn Error>> {
        match Self::load(path) {
            Ok(vec) => {
                let mut csv_map = HashMap::new();
                for row in vec {
                    if let Some(key_val) = row.get_field(key) {
                        csv_map.insert(key_val, row);
                    }
                }
                Ok(csv_map)
            },
            Err(e) => {
                Err(e)
            }
        }
    }
}
