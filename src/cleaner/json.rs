use std::error::Error;
use regex::{Captures, Regex};
use crate::cleaner::Clean;

pub struct Json<'a> {
    text: &'a str,
}

impl<'a> Json<'a> {
    pub fn new(text: &'a str) -> Self {
        Self { text }
    }
}

impl Clean<String> for Json<'_> {
    fn clean(&self) -> Result<String, Box<dyn Error>> {
        let mut cleaned_lines = String::new();
        let mut brace_balance = 0;

        let decimal_re = Regex::new(r"(:|\s)\.(\d+)")?;
        let enum_re = Regex::new(r"([:\[,])\s*([A-Z_][A-Z0-9_]*)\b")?;

        for line in self.text.lines() {
            let line_content = if let Some(idx) = line.find('#') {
                &line[..idx]
            } else if let Some(idx) = line.find("//") {
                &line[..idx]
            } else {
                line
            };

            let skip_regex = line_content.contains("\"description")
                || line_content.contains("\"hullName")
                || line_content.contains("\"name")
                || line_content.contains("\"spriteName")
                || line_content.contains("\"id");

            let processed_line = if skip_regex {
                line_content.to_string()
            } else {
                let fixed_decimal = decimal_re.replace_all(line_content, "${1}0.${2}");
                let fixed_enum = enum_re.replace_all(&fixed_decimal, |caps: &Captures| {
                    format!("{}\"{}\"", &caps[1], &caps[2])
                });
                fixed_enum.to_string()
            };

            let mut final_line_str = String::new();
            for c in processed_line.chars() {
                if c == '{' {
                    if brace_balance == 0 {
                        final_line_str.push(c);
                    } else {
                        final_line_str.push(c);
                    }
                    brace_balance += 1;
                } else if c == '}' {
                    if brace_balance > 0 {
                        brace_balance -= 1;
                        final_line_str.push(c);
                    }
                } else {
                    if brace_balance > 0 {
                        final_line_str.push(c);
                    }
                }
            }

            cleaned_lines.push_str(&final_line_str);
            cleaned_lines.push('\n');
        }

        let trailing_comma_re = Regex::new(r",(\s*[}\]])").unwrap();
        let final_json = trailing_comma_re.replace_all(&cleaned_lines, "$1");

        Ok(final_json.to_string())
    }
}
