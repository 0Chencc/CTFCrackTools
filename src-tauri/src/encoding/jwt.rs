/// JWT (JSON Web Token) 解码器
/// 解析 JWT 的 Header 和 Payload 部分
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};

/// 编码 JWT（仅用于显示格式化的 JSON）
#[allow(dead_code)]
pub fn encode(input: &str) -> String {
    // JWT 编码需要私钥签名，这里只做格式化
    // 尝试将输入作为 JSON 格式化
    if let Ok(json) = serde_json::from_str::<serde_json::Value>(input) {
        serde_json::to_string_pretty(&json).unwrap_or_else(|_| input.to_string())
    } else {
        input.to_string()
    }
}

/// 解码 JWT，返回格式化的 Header 和 Payload
pub fn decode(input: &str) -> Result<String, String> {
    let parts: Vec<&str> = input.trim().split('.').collect();

    if parts.len() < 2 {
        return Err("Invalid JWT format: expected at least 2 parts separated by '.'".to_string());
    }

    let mut result = String::new();

    // 解码 Header
    result.push_str("=== HEADER ===\n");
    match decode_base64_json(parts[0]) {
        Ok(header) => result.push_str(&header),
        Err(e) => result.push_str(&format!("Error decoding header: {}", e)),
    }

    // 解码 Payload
    result.push_str("\n\n=== PAYLOAD ===\n");
    match decode_base64_json(parts[1]) {
        Ok(payload) => result.push_str(&payload),
        Err(e) => result.push_str(&format!("Error decoding payload: {}", e)),
    }

    // 如果有签名部分，显示签名信息
    if parts.len() >= 3 {
        result.push_str("\n\n=== SIGNATURE ===\n");
        result.push_str(&format!("(Base64): {}", parts[2]));

        // 尝试解析 header 获取算法
        if let Ok(header_json) = decode_base64_json(parts[0]) {
            if let Ok(header) = serde_json::from_str::<serde_json::Value>(&header_json) {
                if let Some(alg) = header.get("alg").and_then(|v| v.as_str()) {
                    result.push_str(&format!("\n(Algorithm): {}", alg));
                }
            }
        }
    }

    Ok(result)
}

fn decode_base64_json(input: &str) -> Result<String, String> {
    // JWT 使用 URL-safe Base64 without padding
    let decoded = URL_SAFE_NO_PAD
        .decode(input)
        .or_else(|_| {
            // 尝试添加 padding
            let padded = match input.len() % 4 {
                2 => format!("{}==", input),
                3 => format!("{}=", input),
                _ => input.to_string(),
            };
            URL_SAFE_NO_PAD.decode(&padded)
        })
        .map_err(|e| format!("Base64 decode error: {}", e))?;

    let json_str = String::from_utf8(decoded).map_err(|e| format!("UTF-8 decode error: {}", e))?;

    // 格式化 JSON
    let json: serde_json::Value =
        serde_json::from_str(&json_str).map_err(|e| format!("JSON parse error: {}", e))?;

    serde_json::to_string_pretty(&json).map_err(|e| format!("JSON format error: {}", e))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jwt_decode() {
        // 示例 JWT (未签名)
        let jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.signature";
        let result = decode(jwt).unwrap();
        assert!(result.contains("HS256"));
        assert!(result.contains("John Doe"));
    }
}
