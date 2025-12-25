use aes::Aes128;
use block_padding::Pkcs7;
use cbc::cipher::{BlockDecryptMut, BlockEncryptMut, KeyIvInit};
use cbc::{Decryptor, Encryptor};

type Aes128CbcEnc = Encryptor<Aes128>;
type Aes128CbcDec = Decryptor<Aes128>;

/// 默认密钥和 IV（16 字节）
const DEFAULT_KEY: &[u8; 16] = b"CTFCrackToolsKey";
const DEFAULT_IV: &[u8; 16] = b"CTFCrackToolsIV!";

/// AES-128-CBC 加密
pub fn aes_encrypt(input: &str) -> String {
    let cipher = Aes128CbcEnc::new(DEFAULT_KEY.into(), DEFAULT_IV.into());
    let plaintext = input.as_bytes();

    // 计算需要的缓冲区大小（包含填充）
    let block_size = 16;
    let padded_len = ((plaintext.len() / block_size) + 1) * block_size;
    let mut buffer = vec![0u8; padded_len];
    buffer[..plaintext.len()].copy_from_slice(plaintext);

    let ciphertext = cipher
        .encrypt_padded_mut::<Pkcs7>(&mut buffer, plaintext.len())
        .expect("encryption failed");

    hex::encode(ciphertext)
}

/// AES-128-CBC 解密
pub fn aes_decrypt(input: &str) -> Result<String, String> {
    let ciphertext = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;

    if ciphertext.is_empty() {
        return Err("Empty ciphertext".to_string());
    }

    let cipher = Aes128CbcDec::new(DEFAULT_KEY.into(), DEFAULT_IV.into());
    let mut buffer = ciphertext.clone();

    let plaintext = cipher
        .decrypt_padded_mut::<Pkcs7>(&mut buffer)
        .map_err(|e| format!("Decryption failed: {:?}", e))?;

    String::from_utf8(plaintext.to_vec()).map_err(|e| format!("UTF-8 error: {}", e))
}

/// RC4 加密
pub fn rc4_encrypt(input: &str) -> String {
    use rc4::{KeyInit, Rc4, StreamCipher};

    let key = b"CTFCrackToolsRC4";
    let mut cipher = Rc4::new(key.into());
    let mut buffer = input.as_bytes().to_vec();
    cipher.apply_keystream(&mut buffer);

    hex::encode(buffer)
}

/// RC4 解密
pub fn rc4_decrypt(input: &str) -> Result<String, String> {
    use rc4::{KeyInit, Rc4, StreamCipher};

    let ciphertext = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;

    let key = b"CTFCrackToolsRC4";
    let mut cipher = Rc4::new(key.into());
    let mut buffer = ciphertext;
    cipher.apply_keystream(&mut buffer);

    String::from_utf8(buffer).map_err(|e| format!("UTF-8 error: {}", e))
}

// ==================== DES ====================

use des::Des;
type DesCbcEnc = Encryptor<Des>;
type DesCbcDec = Decryptor<Des>;

/// DES 默认密钥和 IV（8 字节）
const DES_KEY: &[u8; 8] = b"CTFCrack";
const DES_IV: &[u8; 8] = b"ToolsIV!";

/// DES-CBC 加密
pub fn des_encrypt(input: &str) -> String {
    let cipher = DesCbcEnc::new(DES_KEY.into(), DES_IV.into());
    let plaintext = input.as_bytes();

    let block_size = 8;
    let padded_len = ((plaintext.len() / block_size) + 1) * block_size;
    let mut buffer = vec![0u8; padded_len];
    buffer[..plaintext.len()].copy_from_slice(plaintext);

    let ciphertext = cipher
        .encrypt_padded_mut::<Pkcs7>(&mut buffer, plaintext.len())
        .expect("DES encryption failed");

    hex::encode(ciphertext)
}

/// DES-CBC 解密
pub fn des_decrypt(input: &str) -> Result<String, String> {
    let ciphertext = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;

    if ciphertext.is_empty() {
        return Err("Empty ciphertext".to_string());
    }

    let cipher = DesCbcDec::new(DES_KEY.into(), DES_IV.into());
    let mut buffer = ciphertext.clone();

    let plaintext = cipher
        .decrypt_padded_mut::<Pkcs7>(&mut buffer)
        .map_err(|e| format!("DES decryption failed: {:?}", e))?;

    String::from_utf8(plaintext.to_vec()).map_err(|e| format!("UTF-8 error: {}", e))
}

// ==================== Triple DES ====================

use des::TdesEde3;
type TdesCbcEnc = Encryptor<TdesEde3>;
type TdesCbcDec = Decryptor<TdesEde3>;

/// 3DES 默认密钥（24 字节）和 IV（8 字节）
const TDES_KEY: &[u8; 24] = b"CTFCrackToolsTripleDES!!";
const TDES_IV: &[u8; 8] = b"3DESIV!!";

/// 3DES-CBC 加密
pub fn triple_des_encrypt(input: &str) -> String {
    let cipher = TdesCbcEnc::new(TDES_KEY.into(), TDES_IV.into());
    let plaintext = input.as_bytes();

    let block_size = 8;
    let padded_len = ((plaintext.len() / block_size) + 1) * block_size;
    let mut buffer = vec![0u8; padded_len];
    buffer[..plaintext.len()].copy_from_slice(plaintext);

    let ciphertext = cipher
        .encrypt_padded_mut::<Pkcs7>(&mut buffer, plaintext.len())
        .expect("3DES encryption failed");

    hex::encode(ciphertext)
}

/// 3DES-CBC 解密
pub fn triple_des_decrypt(input: &str) -> Result<String, String> {
    let ciphertext = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;

    if ciphertext.is_empty() {
        return Err("Empty ciphertext".to_string());
    }

    let cipher = TdesCbcDec::new(TDES_KEY.into(), TDES_IV.into());
    let mut buffer = ciphertext.clone();

    let plaintext = cipher
        .decrypt_padded_mut::<Pkcs7>(&mut buffer)
        .map_err(|e| format!("3DES decryption failed: {:?}", e))?;

    String::from_utf8(plaintext.to_vec()).map_err(|e| format!("UTF-8 error: {}", e))
}

// ==================== Blowfish ====================

use blowfish::Blowfish;
type BlowfishCbcEnc = Encryptor<Blowfish>;
type BlowfishCbcDec = Decryptor<Blowfish>;

/// Blowfish 默认密钥（16 字节）和 IV（8 字节）
const BLOWFISH_KEY: &[u8; 16] = b"CTFCrackBlowfish";
const BLOWFISH_IV: &[u8; 8] = b"BlowIV!!";

/// Blowfish-CBC 加密
pub fn blowfish_encrypt(input: &str) -> String {
    let cipher =
        BlowfishCbcEnc::new_from_slices(BLOWFISH_KEY, BLOWFISH_IV).expect("Invalid key/IV length");
    let plaintext = input.as_bytes();

    let block_size = 8;
    let padded_len = ((plaintext.len() / block_size) + 1) * block_size;
    let mut buffer = vec![0u8; padded_len];
    buffer[..plaintext.len()].copy_from_slice(plaintext);

    let ciphertext = cipher
        .encrypt_padded_mut::<Pkcs7>(&mut buffer, plaintext.len())
        .expect("Blowfish encryption failed");

    hex::encode(ciphertext)
}

/// Blowfish-CBC 解密
pub fn blowfish_decrypt(input: &str) -> Result<String, String> {
    let ciphertext = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;

    if ciphertext.is_empty() {
        return Err("Empty ciphertext".to_string());
    }

    let cipher = BlowfishCbcDec::new_from_slices(BLOWFISH_KEY, BLOWFISH_IV)
        .map_err(|_| "Invalid key/IV length")?;
    let mut buffer = ciphertext.clone();

    let plaintext = cipher
        .decrypt_padded_mut::<Pkcs7>(&mut buffer)
        .map_err(|e| format!("Blowfish decryption failed: {:?}", e))?;

    String::from_utf8(plaintext.to_vec()).map_err(|e| format!("UTF-8 error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    // AES 测试
    #[test]
    fn test_aes_roundtrip() {
        let inputs = ["Hello", "CTFCrackTools", "Test123!"];
        for input in inputs {
            let encrypted = aes_encrypt(input);
            let decrypted = aes_decrypt(&encrypted).unwrap();
            assert_eq!(decrypted, input);
        }
    }

    #[test]
    fn test_aes_decrypt_invalid() {
        assert!(aes_decrypt("invalid").is_err());
        assert!(aes_decrypt("").is_err());
    }

    // RC4 测试
    #[test]
    fn test_rc4_roundtrip() {
        let inputs = ["Hello", "CTFCrackTools", "Stream cipher test"];
        for input in inputs {
            let encrypted = rc4_encrypt(input);
            let decrypted = rc4_decrypt(&encrypted).unwrap();
            assert_eq!(decrypted, input);
        }
    }

    // DES 测试
    #[test]
    fn test_des_roundtrip() {
        let inputs = ["Hello", "CTF", "DES Test!", "12345678"];
        for input in inputs {
            let encrypted = des_encrypt(input);
            let decrypted = des_decrypt(&encrypted).unwrap();
            assert_eq!(decrypted, input);
        }
    }

    #[test]
    fn test_des_decrypt_invalid() {
        assert!(des_decrypt("invalid").is_err());
        assert!(des_decrypt("").is_err());
    }

    // 3DES 测试
    #[test]
    fn test_triple_des_roundtrip() {
        let inputs = ["Hello", "CTF", "Triple DES!", "Security"];
        for input in inputs {
            let encrypted = triple_des_encrypt(input);
            let decrypted = triple_des_decrypt(&encrypted).unwrap();
            assert_eq!(decrypted, input);
        }
    }

    #[test]
    fn test_triple_des_decrypt_invalid() {
        assert!(triple_des_decrypt("invalid").is_err());
        assert!(triple_des_decrypt("").is_err());
    }

    // Blowfish 测试
    #[test]
    fn test_blowfish_roundtrip() {
        let inputs = ["Hello", "CTF", "Blowfish!", "Encrypt me"];
        for input in inputs {
            let encrypted = blowfish_encrypt(input);
            let decrypted = blowfish_decrypt(&encrypted).unwrap();
            assert_eq!(decrypted, input);
        }
    }

    #[test]
    fn test_blowfish_decrypt_invalid() {
        assert!(blowfish_decrypt("invalid").is_err());
        assert!(blowfish_decrypt("").is_err());
    }

    // 不同算法产生不同密文
    #[test]
    fn test_different_algorithms_produce_different_output() {
        let input = "TestInput";
        let aes = aes_encrypt(input);
        let des = des_encrypt(input);
        let tdes = triple_des_encrypt(input);
        let bf = blowfish_encrypt(input);
        let rc4 = rc4_encrypt(input);

        assert_ne!(aes, des);
        assert_ne!(aes, tdes);
        assert_ne!(aes, bf);
        assert_ne!(aes, rc4);
        assert_ne!(des, tdes);
        assert_ne!(des, bf);
    }
}
