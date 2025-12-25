use sha1::Sha1;
use sha2::{Digest, Sha256, Sha512};

/// MD5 哈希
pub fn md5_hash(input: &str) -> String {
    format!("{:x}", md5::compute(input.as_bytes()))
}

/// SHA1 哈希
pub fn sha1_hash(input: &str) -> String {
    use sha1::Digest;
    let mut hasher = Sha1::new();
    hasher.update(input.as_bytes());
    format!("{:x}", hasher.finalize())
}

/// SHA256 哈希
pub fn sha256_hash(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    format!("{:x}", hasher.finalize())
}

/// SHA512 哈希
pub fn sha512_hash(input: &str) -> String {
    let mut hasher = Sha512::new();
    hasher.update(input.as_bytes());
    format!("{:x}", hasher.finalize())
}

// ==================== HMAC ====================

use hmac::{Hmac, Mac};

type HmacSha256 = Hmac<Sha256>;

/// HMAC 默认密钥
const HMAC_KEY: &[u8] = b"CTFCrackToolsHMACKey";

/// HMAC-SHA256
pub fn hmac_sha256(input: &str) -> String {
    let mut mac = HmacSha256::new_from_slice(HMAC_KEY).expect("HMAC can take key of any size");
    mac.update(input.as_bytes());
    let result = mac.finalize();
    hex::encode(result.into_bytes())
}

/// HMAC-SHA256 验证
#[allow(dead_code)]
pub fn hmac_sha256_verify(input: &str, expected: &str) -> Result<String, String> {
    let computed = hmac_sha256(input);
    if computed.eq_ignore_ascii_case(expected) {
        Ok("HMAC verification successful".to_string())
    } else {
        Err(format!(
            "HMAC mismatch: expected {}, got {}",
            expected, computed
        ))
    }
}

// ==================== PBKDF2 ====================

/// PBKDF2 默认参数
const PBKDF2_SALT: &[u8] = b"CTFCrackSalt";
const PBKDF2_ITERATIONS: u32 = 10000;
const PBKDF2_KEY_LEN: usize = 32;

/// PBKDF2-HMAC-SHA256 密钥导出
pub fn pbkdf2_derive(input: &str) -> String {
    let mut key = [0u8; PBKDF2_KEY_LEN];
    pbkdf2::pbkdf2_hmac::<Sha256>(input.as_bytes(), PBKDF2_SALT, PBKDF2_ITERATIONS, &mut key);
    hex::encode(key)
}

/// PBKDF2 参数信息
#[allow(dead_code)]
pub fn pbkdf2_info() -> String {
    format!(
        "PBKDF2-HMAC-SHA256 (iterations: {}, salt: {}, key_len: {} bytes)",
        PBKDF2_ITERATIONS,
        String::from_utf8_lossy(PBKDF2_SALT),
        PBKDF2_KEY_LEN
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_md5() {
        assert_eq!(md5_hash("hello"), "5d41402abc4b2a76b9719d911017c592");
        assert_eq!(md5_hash(""), "d41d8cd98f00b204e9800998ecf8427e");
    }

    #[test]
    fn test_sha1() {
        assert_eq!(
            sha1_hash("hello"),
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
        );
    }

    #[test]
    fn test_sha256() {
        assert_eq!(
            sha256_hash("hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        );
    }

    #[test]
    fn test_sha512() {
        let hash = sha512_hash("hello");
        assert_eq!(hash.len(), 128); // SHA512 produces 64 bytes = 128 hex chars
        assert!(hash.starts_with("9b71d224"));
    }

    #[test]
    fn test_hmac_sha256() {
        let hmac1 = hmac_sha256("hello");
        let hmac2 = hmac_sha256("hello");
        // 相同输入应产生相同输出
        assert_eq!(hmac1, hmac2);
        // HMAC 应产生 64 个十六进制字符
        assert_eq!(hmac1.len(), 64);
    }

    #[test]
    fn test_hmac_sha256_different_inputs() {
        let hmac1 = hmac_sha256("hello");
        let hmac2 = hmac_sha256("world");
        // 不同输入应产生不同输出
        assert_ne!(hmac1, hmac2);
    }

    #[test]
    fn test_hmac_sha256_verify() {
        let input = "test message";
        let computed = hmac_sha256(input);
        assert!(hmac_sha256_verify(input, &computed).is_ok());
        assert!(hmac_sha256_verify(input, "wrong_hmac").is_err());
    }

    #[test]
    fn test_pbkdf2() {
        let key1 = pbkdf2_derive("password");
        let key2 = pbkdf2_derive("password");
        // 相同密码应产生相同密钥
        assert_eq!(key1, key2);
        // PBKDF2 应产生 64 个十六进制字符 (32 bytes)
        assert_eq!(key1.len(), 64);
    }

    #[test]
    fn test_pbkdf2_different_passwords() {
        let key1 = pbkdf2_derive("password1");
        let key2 = pbkdf2_derive("password2");
        // 不同密码应产生不同密钥
        assert_ne!(key1, key2);
    }

    #[test]
    fn test_pbkdf2_info() {
        let info = pbkdf2_info();
        assert!(info.contains("PBKDF2"));
        assert!(info.contains("10000"));
    }
}
