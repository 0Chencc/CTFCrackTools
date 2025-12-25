/// Binary 编码 - 将文本转换为二进制（空格分隔）
pub fn encode(input: &str) -> String {
    input
        .bytes()
        .map(|b| format!("{:08b}", b))
        .collect::<Vec<_>>()
        .join(" ")
}

/// Binary 解码 - 将二进制转换为文本
pub fn decode(input: &str) -> Result<String, String> {
    let bytes: Result<Vec<u8>, _> = input
        .split_whitespace()
        .map(|s| u8::from_str_radix(s, 2).map_err(|_| format!("Invalid binary: {}", s)))
        .collect();

    let bytes = bytes?;
    String::from_utf8(bytes).map_err(|e| format!("UTF-8 error: {}", e))
}
