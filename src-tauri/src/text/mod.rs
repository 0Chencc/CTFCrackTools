/// 转换为大写
pub fn uppercase(input: &str) -> String {
    input.to_uppercase()
}

/// 转换为小写
pub fn lowercase(input: &str) -> String {
    input.to_lowercase()
}

/// 反转字符串
pub fn reverse(input: &str) -> String {
    input.chars().rev().collect()
}

/// 移除空格
pub fn remove_spaces(input: &str) -> String {
    input.chars().filter(|c| !c.is_whitespace()).collect()
}

/// 字符串长度统计
pub fn length(input: &str) -> String {
    format!(
        "Length: {} chars, {} bytes",
        input.chars().count(),
        input.len()
    )
}

/// 首字母大写
pub fn capitalize(input: &str) -> String {
    input
        .split_whitespace()
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                None => String::new(),
                Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

/// 交换大小写
pub fn swap_case(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            if c.is_uppercase() {
                c.to_lowercase().collect::<String>()
            } else if c.is_lowercase() {
                c.to_uppercase().collect::<String>()
            } else {
                c.to_string()
            }
        })
        .collect()
}

/// 去除首尾空格
pub fn trim(input: &str) -> String {
    input.trim().to_string()
}
