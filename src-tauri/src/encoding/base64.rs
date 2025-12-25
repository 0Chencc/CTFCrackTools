use base64::{engine::general_purpose::STANDARD, Engine};

/// Base64 编码
pub fn encode(input: &str) -> String {
    STANDARD.encode(input.as_bytes())
}

/// Base64 解码
pub fn decode(input: &str) -> Result<String, String> {
    let decoded = STANDARD
        .decode(input.trim())
        .map_err(|e| format!("Base64 decode error: {}", e))?;

    String::from_utf8(decoded).map_err(|e| format!("UTF-8 decode error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode() {
        assert_eq!(encode("Hello, World!"), "SGVsbG8sIFdvcmxkIQ==");
        assert_eq!(encode("CTFCrackTools"), "Q1RGQ3JhY2tUb29scw==");
    }

    #[test]
    fn test_decode() {
        assert_eq!(decode("SGVsbG8sIFdvcmxkIQ==").unwrap(), "Hello, World!");
        assert_eq!(decode("Q1RGQ3JhY2tUb29scw==").unwrap(), "CTFCrackTools");
    }

    #[test]
    fn test_decode_invalid() {
        assert!(decode("invalid!!!").is_err());
    }
}
