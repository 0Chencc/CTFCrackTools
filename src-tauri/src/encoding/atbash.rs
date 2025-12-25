//! Atbash cipher encoding/decoding
//! A=Z, B=Y, C=X, ... (symmetric, encode == decode)

fn atbash_transform(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            if c.is_ascii_lowercase() {
                // a-z: a(97) -> z(122), b(98) -> y(121), etc.
                let offset = c as u8 - b'a';
                (b'z' - offset) as char
            } else if c.is_ascii_uppercase() {
                // A-Z: A(65) -> Z(90), B(66) -> Y(89), etc.
                let offset = c as u8 - b'A';
                (b'Z' - offset) as char
            } else {
                c
            }
        })
        .collect()
}

pub fn encode(input: &str) -> String {
    atbash_transform(input)
}

pub fn decode(input: &str) -> Result<String, String> {
    // Atbash is symmetric - encoding and decoding are the same
    Ok(atbash_transform(input))
}
