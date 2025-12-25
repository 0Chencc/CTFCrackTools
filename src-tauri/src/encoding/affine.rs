/// 仿射密码 (Affine Cipher)
/// 加密公式: E(x) = (ax + b) mod 26
/// 解密公式: D(y) = a^(-1)(y - b) mod 26
/// 默认参数: a = 5, b = 8
const DEFAULT_A: i32 = 5;
const DEFAULT_B: i32 = 8;

/// 计算模逆元 (扩展欧几里得算法)
fn mod_inverse(a: i32, m: i32) -> Option<i32> {
    let mut mn = (m, a);
    let mut xy = (0, 1);

    while mn.1 != 0 {
        let q = mn.0 / mn.1;
        mn = (mn.1, mn.0 - q * mn.1);
        xy = (xy.1, xy.0 - q * xy.1);
    }

    if mn.0 != 1 {
        return None; // a 和 m 不互质
    }

    Some(((xy.0 % m) + m) % m)
}

/// 检查 a 和 26 是否互质
#[allow(dead_code)]
fn is_valid_a(a: i32) -> bool {
    mod_inverse(a, 26).is_some()
}

/// 仿射加密
pub fn encode(input: &str) -> String {
    let a = DEFAULT_A;
    let b = DEFAULT_B;

    input
        .chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { 'A' } else { 'a' };
                let x = (c as i32) - (base as i32);
                let y = ((a * x + b) % 26 + 26) % 26;
                ((y as u8) + (base as u8)) as char
            } else {
                c
            }
        })
        .collect()
}

/// 仿射解密
pub fn decode(input: &str) -> Result<String, String> {
    let a = DEFAULT_A;
    let b = DEFAULT_B;

    let a_inv = mod_inverse(a, 26)
        .ok_or_else(|| format!("No modular inverse for a={} (must be coprime with 26)", a))?;

    Ok(input
        .chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { 'A' } else { 'a' };
                let y = (c as i32) - (base as i32);
                let x = ((a_inv * (y - b)) % 26 + 26) % 26;
                ((x as u8) + (base as u8)) as char
            } else {
                c
            }
        })
        .collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mod_inverse() {
        assert_eq!(mod_inverse(5, 26), Some(21));
        assert_eq!(mod_inverse(7, 26), Some(15));
        assert_eq!(mod_inverse(13, 26), None); // 不互质
    }

    #[test]
    fn test_affine_encode() {
        assert_eq!(encode("HELLO"), "RCLLA");
    }

    #[test]
    fn test_affine_decode() {
        assert_eq!(decode("RCLLA").unwrap(), "HELLO");
    }

    #[test]
    fn test_affine_roundtrip() {
        let original = "The Quick Brown Fox";
        let encoded = encode(original);
        let decoded = decode(&encoded).unwrap();
        assert_eq!(decoded, original);
    }
}
