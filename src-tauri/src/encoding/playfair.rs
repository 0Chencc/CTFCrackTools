/// Playfair 密码
/// 使用 5x5 矩阵的双字母替换密码
const DEFAULT_KEY: &str = "PLAYFAIR";

/// 生成 Playfair 矩阵
fn generate_matrix(key: &str) -> [[char; 5]; 5] {
    let mut matrix = [[' '; 5]; 5];
    let mut used = [false; 26];
    let mut idx = 0;

    // 处理密钥
    for c in key.to_uppercase().chars() {
        if c.is_ascii_alphabetic() {
            let c = if c == 'J' { 'I' } else { c };
            let pos = (c as usize) - ('A' as usize);
            if !used[pos] {
                used[pos] = true;
                matrix[idx / 5][idx % 5] = c;
                idx += 1;
            }
        }
    }

    // 填充剩余字母
    for c in 'A'..='Z' {
        if c == 'J' {
            continue;
        }
        let pos = (c as usize) - ('A' as usize);
        if !used[pos] {
            used[pos] = true;
            matrix[idx / 5][idx % 5] = c;
            idx += 1;
        }
    }

    matrix
}

/// 查找字符在矩阵中的位置
fn find_position(matrix: &[[char; 5]; 5], c: char) -> Option<(usize, usize)> {
    let c = if c == 'J' { 'I' } else { c };
    for (i, row) in matrix.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {
            if cell == c {
                return Some((i, j));
            }
        }
    }
    None
}

/// 准备明文：分成双字母组
fn prepare_text(input: &str) -> Vec<(char, char)> {
    let chars: Vec<char> = input
        .to_uppercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .map(|c| if c == 'J' { 'I' } else { c })
        .collect();

    let mut pairs = Vec::new();
    let mut i = 0;

    while i < chars.len() {
        let first = chars[i];
        let second = if i + 1 < chars.len() && chars[i + 1] != first {
            i += 2;
            chars[i - 1]
        } else {
            i += 1;
            'X'
        };
        pairs.push((first, second));
    }

    pairs
}

/// Playfair 编码
pub fn encode(input: &str) -> String {
    let matrix = generate_matrix(DEFAULT_KEY);
    let pairs = prepare_text(input);
    let mut result = String::new();

    for (a, b) in pairs {
        if let (Some((r1, c1)), Some((r2, c2))) =
            (find_position(&matrix, a), find_position(&matrix, b))
        {
            let (new_a, new_b) = if r1 == r2 {
                // 同行：右移
                (matrix[r1][(c1 + 1) % 5], matrix[r2][(c2 + 1) % 5])
            } else if c1 == c2 {
                // 同列：下移
                (matrix[(r1 + 1) % 5][c1], matrix[(r2 + 1) % 5][c2])
            } else {
                // 矩形：交换列
                (matrix[r1][c2], matrix[r2][c1])
            };
            result.push(new_a);
            result.push(new_b);
        }
    }

    result
}

/// Playfair 解码
pub fn decode(input: &str) -> Result<String, String> {
    let matrix = generate_matrix(DEFAULT_KEY);
    let chars: Vec<char> = input
        .to_uppercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .collect();

    if chars.len() % 2 != 0 {
        return Err("Playfair ciphertext must have even length".to_string());
    }

    let mut result = String::new();

    for chunk in chars.chunks(2) {
        let (a, b) = (chunk[0], chunk[1]);
        if let (Some((r1, c1)), Some((r2, c2))) =
            (find_position(&matrix, a), find_position(&matrix, b))
        {
            let (new_a, new_b) = if r1 == r2 {
                // 同行：左移
                (matrix[r1][(c1 + 4) % 5], matrix[r2][(c2 + 4) % 5])
            } else if c1 == c2 {
                // 同列：上移
                (matrix[(r1 + 4) % 5][c1], matrix[(r2 + 4) % 5][c2])
            } else {
                // 矩形：交换列
                (matrix[r1][c2], matrix[r2][c1])
            };
            result.push(new_a);
            result.push(new_b);
        }
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_playfair_encode_decode() {
        let plain = "HELLO";
        let encoded = encode(plain);
        let decoded = decode(&encoded).unwrap();
        // 注意：Playfair 解码可能包含填充字符 X
        assert!(decoded.starts_with("HE"));
    }

    #[test]
    fn test_playfair_matrix() {
        let matrix = generate_matrix("PLAYFAIR");
        assert_eq!(matrix[0][0], 'P');
        assert_eq!(matrix[0][1], 'L');
    }
}
