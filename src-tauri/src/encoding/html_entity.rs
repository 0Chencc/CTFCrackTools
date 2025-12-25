/// HTML Entity 编码/解码
/// 支持命名实体和数字实体
use std::collections::HashMap;

lazy_static::lazy_static! {
    static ref NAMED_ENTITIES: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        // 常用 HTML 实体
        m.insert("&lt;", "<");
        m.insert("&gt;", ">");
        m.insert("&amp;", "&");
        m.insert("&quot;", "\"");
        m.insert("&apos;", "'");
        m.insert("&nbsp;", "\u{00A0}");
        m.insert("&copy;", "©");
        m.insert("&reg;", "®");
        m.insert("&trade;", "™");
        m.insert("&euro;", "€");
        m.insert("&pound;", "£");
        m.insert("&yen;", "¥");
        m.insert("&cent;", "¢");
        m.insert("&sect;", "§");
        m.insert("&deg;", "°");
        m.insert("&plusmn;", "±");
        m.insert("&times;", "×");
        m.insert("&divide;", "÷");
        m.insert("&frac14;", "¼");
        m.insert("&frac12;", "½");
        m.insert("&frac34;", "¾");
        m.insert("&hellip;", "…");
        m.insert("&mdash;", "—");
        m.insert("&ndash;", "–");
        m.insert("&lsquo;", "\u{2018}"); // '
        m.insert("&rsquo;", "\u{2019}"); // '
        m.insert("&ldquo;", "\u{201C}"); // "
        m.insert("&rdquo;", "\u{201D}"); // "
        m.insert("&bull;", "•");
        m.insert("&middot;", "·");
        m.insert("&laquo;", "«");
        m.insert("&raquo;", "»");
        m
    };

    static ref REVERSE_ENTITIES: HashMap<char, &'static str> = {
        let mut m = HashMap::new();
        m.insert('<', "&lt;");
        m.insert('>', "&gt;");
        m.insert('&', "&amp;");
        m.insert('"', "&quot;");
        m.insert('\'', "&apos;");
        m
    };
}

/// 编码为 HTML Entity（数字格式 &#xxx;）
pub fn encode(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            if let Some(&entity) = REVERSE_ENTITIES.get(&c) {
                entity.to_string()
            } else if c.is_ascii() && !c.is_ascii_control() {
                c.to_string()
            } else {
                format!("&#{};", c as u32)
            }
        })
        .collect()
}

/// 解码 HTML Entity
pub fn decode(input: &str) -> Result<String, String> {
    let mut result = String::new();
    let mut chars = input.chars().peekable();

    while let Some(c) = chars.next() {
        if c == '&' {
            let mut entity = String::from("&");

            // 收集实体内容直到 ';' 或非法字符
            while let Some(&next) = chars.peek() {
                if next == ';' {
                    entity.push(chars.next().unwrap());
                    break;
                } else if next.is_alphanumeric() || next == '#' {
                    entity.push(chars.next().unwrap());
                } else {
                    break;
                }
            }

            if entity.ends_with(';') {
                // 尝试解析实体
                if let Some(decoded) = decode_entity(&entity) {
                    result.push_str(&decoded);
                } else {
                    result.push_str(&entity);
                }
            } else {
                result.push_str(&entity);
            }
        } else {
            result.push(c);
        }
    }

    Ok(result)
}

fn decode_entity(entity: &str) -> Option<String> {
    // 尝试命名实体
    if let Some(&value) = NAMED_ENTITIES.get(entity) {
        return Some(value.to_string());
    }

    // 尝试数字实体
    if entity.starts_with("&#") && entity.ends_with(';') {
        let inner = &entity[2..entity.len() - 1];

        let code = if inner.starts_with('x') || inner.starts_with('X') {
            // 十六进制 &#xXXXX;
            u32::from_str_radix(&inner[1..], 16).ok()
        } else {
            // 十进制 &#XXXX;
            inner.parse::<u32>().ok()
        };

        if let Some(code) = code {
            if let Some(c) = char::from_u32(code) {
                return Some(c.to_string());
            }
        }
    }

    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_html_encode() {
        assert_eq!(encode("<script>"), "&lt;script&gt;");
        assert_eq!(encode("a & b"), "a &amp; b");
    }

    #[test]
    fn test_html_decode() {
        assert_eq!(decode("&lt;script&gt;").unwrap(), "<script>");
        assert_eq!(decode("&#60;&#62;").unwrap(), "<>");
        assert_eq!(decode("&#x3C;&#x3E;").unwrap(), "<>");
        assert_eq!(decode("&copy; 2024").unwrap(), "© 2024");
    }
}
