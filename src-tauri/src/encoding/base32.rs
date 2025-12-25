use data_encoding::BASE32;

/// Base32 编码
pub fn encode(input: &str) -> String {
    BASE32.encode(input.as_bytes())
}

/// Base32 解码
pub fn decode(input: &str) -> Result<String, String> {
    let decoded = BASE32
        .decode(input.trim().to_uppercase().as_bytes())
        .map_err(|e| format!("Base32 decode error: {}", e))?;

    String::from_utf8(decoded).map_err(|e| format!("UTF-8 decode error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode() {
        assert_eq!(encode("Hello"), "JBSWY3DP");
        assert_eq!(encode("CTF"), "INKEM===");
        assert_eq!(encode("test"), "ORSXG5A=");
    }

    #[test]
    fn test_decode() {
        assert_eq!(decode("JBSWY3DP").unwrap(), "Hello");
        assert_eq!(decode("INKEM===").unwrap(), "CTF");
        assert_eq!(decode("ORSXG5A=").unwrap(), "test");
    }

    #[test]
    fn test_roundtrip() {
        let inputs = ["", "a", "ab", "abc", "CTFCrackTools", "Hello World!"];
        for input in inputs {
            assert_eq!(decode(&encode(input)).unwrap(), input);
        }
    }
}
