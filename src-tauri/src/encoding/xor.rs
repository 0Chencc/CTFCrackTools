/// XOR 编码（默认密钥 "key"）
pub fn encode(input: &str) -> String {
    encode_with_key(input, "key")
}

/// XOR 解码（默认密钥 "key"）
pub fn decode(input: &str) -> Result<String, String> {
    // XOR 解码输入是十六进制字符串
    let bytes = hex::decode(input).map_err(|e| format!("Invalid hex: {}", e))?;
    let key = b"key";
    let result: Vec<u8> = bytes
        .iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect();
    String::from_utf8(result).map_err(|e| format!("UTF-8 error: {}", e))
}

/// 带自定义密钥的 XOR 编码
pub fn encode_with_key(input: &str, key: &str) -> String {
    let key_bytes = key.as_bytes();
    let result: Vec<u8> = input
        .bytes()
        .enumerate()
        .map(|(i, b)| b ^ key_bytes[i % key_bytes.len()])
        .collect();
    hex::encode(result)
}
