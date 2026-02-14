use std::fs;
use std::path::Path;
use serde_json::Value;
use crate::cleaner;
use crate::cleaner::Clean;

///
/// Dictates how the loaded file needs to be parsed.
///
pub trait ParsePlan<C>: Sized {
    fn from_value(value: &Value, ctx: &C) -> Option<Self>;

    fn parse(path: &Path, ctx: &C) -> Option<Self> {
        let content = fs::read_to_string(path).ok()?;
        let valid_json: String = cleaner::Json::new(&content).clean().ok()?;
        let json_value: Value = serde_json::from_str(&valid_json).ok()?;
        Self::from_value(&json_value, ctx)
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
