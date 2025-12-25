use percent_encoding::{percent_decode_str, utf8_percent_encode, NON_ALPHANUMERIC};

/// URL 编码
pub fn encode(input: &str) -> String {
    utf8_percent_encode(input, NON_ALPHANUMERIC).to_string()
}

/// URL 解码
pub fn decode(input: &str) -> Result<String, String> {
    percent_decode_str(input.trim())
        .decode_utf8()
        .map(|s| s.into_owned())
        .map_err(|e| format!("URL decode error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode() {
        assert_eq!(encode("Hello World!"), "Hello%20World%21");
        assert_eq!(encode("flag{test}"), "flag%7Btest%7D");
    }

    #[test]
    fn test_decode() {
        assert_eq!(decode("Hello%20World%21").unwrap(), "Hello World!");
        assert_eq!(decode("flag%7Btest%7D").unwrap(), "flag{test}");
    }
}
