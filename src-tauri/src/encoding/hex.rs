use hex::{decode, encode};

/// Hex 编码
pub fn hex_encode(input: &str) -> String {
    encode(input.as_bytes())
}

/// Hex 解码
pub fn hex_decode(input: &str) -> Result<String, String> {
    let decoded =
        decode(input.trim().replace(" ", "")).map_err(|e| format!("Hex decode error: {}", e))?;

    String::from_utf8(decoded).map_err(|e| format!("UTF-8 decode error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode() {
        assert_eq!(hex_encode("Hello"), "48656c6c6f");
        assert_eq!(hex_encode("CTF"), "435446");
    }

    #[test]
    fn test_decode() {
        assert_eq!(hex_decode("48656c6c6f").unwrap(), "Hello");
        assert_eq!(hex_decode("435446").unwrap(), "CTF");
    }
}
