/// ROT47 编码 - 扩展的 ROT13，覆盖 ASCII 可打印字符 (33-126)
/// 将字符向前移动 47 位
pub fn encode(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            let code = c as u32;
            if (33..=126).contains(&code) {
                // ASCII 可打印字符范围 33-126 (94 个字符)
                // 移动 47 位
                let shifted = ((code - 33 + 47) % 94) + 33;
                char::from_u32(shifted).unwrap_or(c)
            } else {
                c
            }
        })
        .collect()
}

pub fn decode(input: &str) -> Result<String, String> {
    // ROT47 是对称的，编码和解码相同
    Ok(encode(input))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rot47_encode() {
        assert_eq!(encode("Hello World!"), "w6==@ (@C=5P");
        assert_eq!(encode("The Quick Brown Fox"), "%96 \"F:4< qC@H? u@I");
    }

    #[test]
    fn test_rot47_decode() {
        assert_eq!(decode("w6==@ (@C=5P").unwrap(), "Hello World!");
    }

    #[test]
    fn test_rot47_symmetric() {
        let original = "Test123!@#";
        let encoded = encode(original);
        let decoded = decode(&encoded).unwrap();
        assert_eq!(decoded, original);
    }
}
