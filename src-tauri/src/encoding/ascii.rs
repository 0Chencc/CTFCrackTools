/// ASCII 编码 - 将文本转换为 ASCII 码（空格分隔）
pub fn encode(input: &str) -> String {
    input
        .bytes()
        .map(|b| b.to_string())
        .collect::<Vec<_>>()
        .join(" ")
}

/// ASCII 解码 - 将 ASCII 码转换为文本
pub fn decode(input: &str) -> Result<String, String> {
    let bytes: Result<Vec<u8>, _> = input
        .split_whitespace()
        .map(|s| {
            s.parse::<u8>()
                .map_err(|_| format!("Invalid ASCII value: {}", s))
        })
        .collect();

    let bytes = bytes?;
    String::from_utf8(bytes).map_err(|e| format!("UTF-8 error: {}", e))
}
