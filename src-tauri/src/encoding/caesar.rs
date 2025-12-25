/// Caesar 密码编码（默认位移 3）
pub fn encode(input: &str) -> String {
    encode_with_shift(input, 3)
}

/// Caesar 密码解码（默认位移 3）
pub fn decode(input: &str) -> Result<String, String> {
    Ok(encode_with_shift(input, -3))
}

/// 带自定义位移的 Caesar 编码
pub fn encode_with_shift(input: &str, shift: i32) -> String {
    let shift = shift.rem_euclid(26); // 标准化位移
    input
        .chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let offset = ((c as u8 - base) as i32 + shift) % 26;
                (base + offset as u8) as char
            } else {
                c
            }
        })
        .collect()
}
