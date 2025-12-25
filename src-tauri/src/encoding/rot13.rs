/// ROT13 编码（同时用于编码和解码）
pub fn encode(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let offset = (c as u8 - base + 13) % 26;
                (base + offset) as char
            } else {
                c
            }
        })
        .collect()
}

/// ROT13 解码（与编码相同）
pub fn decode(input: &str) -> Result<String, String> {
    Ok(encode(input))
}
