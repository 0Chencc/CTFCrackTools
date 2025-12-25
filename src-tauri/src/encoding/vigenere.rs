//! Vigenère cipher encoding/decoding
//! Default key: "KEY" (can be changed via parameter in the future)

const DEFAULT_KEY: &str = "KEY";

fn vigenere_transform(input: &str, key: &str, encrypt: bool) -> String {
    if key.is_empty() {
        return input.to_string();
    }

    let key_bytes: Vec<i32> = key
        .to_uppercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .map(|c| (c as i32) - ('A' as i32))
        .collect();

    if key_bytes.is_empty() {
        return input.to_string();
    }

    let mut result = String::new();
    let mut key_index = 0;

    for c in input.chars() {
        if c.is_ascii_alphabetic() {
            let is_upper = c.is_uppercase();
            let base = if is_upper { 'A' as i32 } else { 'a' as i32 };
            let char_val = (c as i32) - base;
            let key_val = key_bytes[key_index % key_bytes.len()];

            let new_val = if encrypt {
                (char_val + key_val).rem_euclid(26)
            } else {
                (char_val - key_val).rem_euclid(26)
            };

            result.push(char::from_u32((new_val + base) as u32).unwrap_or(c));
            key_index += 1;
        } else {
            result.push(c);
        }
    }

    result
}

pub fn encode(input: &str) -> String {
    vigenere_transform(input, DEFAULT_KEY, true)
}

pub fn decode(input: &str) -> Result<String, String> {
    Ok(vigenere_transform(input, DEFAULT_KEY, false))
}
