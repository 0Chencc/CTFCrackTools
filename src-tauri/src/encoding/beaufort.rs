/// Beaufort 密码
/// Vigenère 密码的变体，使用减法而非加法
/// 加密公式: C = (K - P) mod 26
/// 解密公式: P = (K - C) mod 26
/// 特点：加密和解密使用相同的操作
const DEFAULT_KEY: &str = "BEAUFORT";

/// Beaufort 加密/解密 (对称操作)
fn transform(input: &str, key: &str) -> String {
    let key_chars: Vec<char> = key
        .to_uppercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .collect();

    if key_chars.is_empty() {
        return input.to_string();
    }

    let mut key_idx = 0;
    input
        .chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let p = (c.to_ascii_uppercase() as i32) - ('A' as i32);
                let k = (key_chars[key_idx % key_chars.len()] as i32) - ('A' as i32);
                key_idx += 1;

                // Beaufort: C = (K - P) mod 26
                let result = ((k - p) % 26 + 26) % 26;
                let result_char = ((result as u8) + b'A') as char;

                if c.is_ascii_lowercase() {
                    result_char.to_ascii_lowercase()
                } else {
                    result_char
                }
            } else {
                c
            }
        })
        .collect()
}

/// Beaufort 加密
pub fn encode(input: &str) -> String {
    transform(input, DEFAULT_KEY)
}

/// Beaufort 解密 (与加密相同)
pub fn decode(input: &str) -> Result<String, String> {
    // Beaufort 是对称的，解密和加密使用相同的操作
    Ok(transform(input, DEFAULT_KEY))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_beaufort_symmetric() {
        let original = "HELLO";
        let encrypted = encode(original);
        let decrypted = decode(&encrypted).unwrap();
        assert_eq!(decrypted, original);
    }

    #[test]
    fn test_beaufort_preserve_case() {
        let input = "Hello World";
        let encrypted = encode(input);
        let decrypted = decode(&encrypted).unwrap();
        assert_eq!(decrypted, input);
    }

    #[test]
    fn test_beaufort_preserve_non_alpha() {
        let input = "Hello, World! 123";
        let encrypted = encode(input);
        let decrypted = decode(&encrypted).unwrap();
        assert_eq!(decrypted, input);
    }
}
