/// Unicode 编码转换
/// 支持 UTF-8 十六进制、Unicode 转义序列等格式
/// 编码为 Unicode 转义序列 (\uXXXX 格式)
pub fn encode(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            let code = c as u32;
            if code > 127 {
                // 非 ASCII 字符使用 \uXXXX 格式
                if code > 0xFFFF {
                    // 超出 BMP 的字符使用代理对
                    let high = ((code - 0x10000) >> 10) + 0xD800;
                    let low = ((code - 0x10000) & 0x3FF) + 0xDC00;
                    format!("\\u{:04X}\\u{:04X}", high, low)
                } else {
                    format!("\\u{:04X}", code)
                }
            } else if c.is_ascii_control() || c == '\\' {
                // 控制字符和反斜杠也转义
                format!("\\u{:04X}", code)
            } else {
                c.to_string()
            }
        })
        .collect()
}

/// 解码 Unicode 转义序列
pub fn decode(input: &str) -> Result<String, String> {
    let mut result = String::new();
    let mut chars = input.chars().peekable();

    while let Some(c) = chars.next() {
        if c == '\\' {
            match chars.peek() {
                Some('u') | Some('U') => {
                    chars.next(); // 消费 'u'
                    let mut hex = String::new();
                    for _ in 0..4 {
                        if let Some(&h) = chars.peek() {
                            if h.is_ascii_hexdigit() {
                                hex.push(chars.next().unwrap());
                            } else {
                                break;
                            }
                        }
                    }
                    if hex.len() == 4 {
                        if let Ok(code) = u32::from_str_radix(&hex, 16) {
                            // 检查是否是代理对的高位
                            if (0xD800..=0xDBFF).contains(&code) {
                                // 尝试读取低位代理
                                if chars.next() == Some('\\') && chars.next() == Some('u') {
                                    let mut low_hex = String::new();
                                    for _ in 0..4 {
                                        if let Some(&h) = chars.peek() {
                                            if h.is_ascii_hexdigit() {
                                                low_hex.push(chars.next().unwrap());
                                            } else {
                                                break;
                                            }
                                        }
                                    }
                                    if low_hex.len() == 4 {
                                        if let Ok(low_code) = u32::from_str_radix(&low_hex, 16) {
                                            if (0xDC00..=0xDFFF).contains(&low_code) {
                                                let full_code = 0x10000
                                                    + ((code - 0xD800) << 10)
                                                    + (low_code - 0xDC00);
                                                if let Some(ch) = char::from_u32(full_code) {
                                                    result.push(ch);
                                                    continue;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            if let Some(ch) = char::from_u32(code) {
                                result.push(ch);
                            } else {
                                return Err(format!("Invalid Unicode code point: {}", code));
                            }
                        } else {
                            return Err(format!("Invalid hex: {}", hex));
                        }
                    } else {
                        result.push('\\');
                        result.push('u');
                        result.push_str(&hex);
                    }
                }
                Some('x') | Some('X') => {
                    chars.next(); // 消费 'x'
                    let mut hex = String::new();
                    for _ in 0..2 {
                        if let Some(&h) = chars.peek() {
                            if h.is_ascii_hexdigit() {
                                hex.push(chars.next().unwrap());
                            } else {
                                break;
                            }
                        }
                    }
                    if hex.len() == 2 {
                        if let Ok(code) = u8::from_str_radix(&hex, 16) {
                            result.push(code as char);
                        }
                    } else {
                        result.push('\\');
                        result.push('x');
                        result.push_str(&hex);
                    }
                }
                Some('n') => {
                    chars.next();
                    result.push('\n');
                }
                Some('r') => {
                    chars.next();
                    result.push('\r');
                }
                Some('t') => {
                    chars.next();
                    result.push('\t');
                }
                Some('\\') => {
                    chars.next();
                    result.push('\\');
                }
                _ => {
                    result.push(c);
                }
            }
        } else {
            result.push(c);
        }
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unicode_encode() {
        assert_eq!(encode("Hello"), "Hello");
        assert_eq!(encode("你好"), "\\u4F60\\u597D");
    }

    #[test]
    fn test_unicode_decode() {
        assert_eq!(decode("\\u4F60\\u597D").unwrap(), "你好");
        assert_eq!(decode("Hello\\u0020World").unwrap(), "Hello World");
    }
}
