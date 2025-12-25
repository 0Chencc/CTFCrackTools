/// Polybius 方阵密码
/// 使用 5x5 矩阵将字母编码为两位数字
const SQUARE: [[char; 5]; 5] = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'], // I/J 合并
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z'],
];

/// 编码：将字母转为坐标
pub fn encode(input: &str) -> String {
    let mut result = String::new();

    for c in input.to_uppercase().chars() {
        if c.is_ascii_alphabetic() {
            let c = if c == 'J' { 'I' } else { c };
            for (i, row) in SQUARE.iter().enumerate() {
                for (j, &cell) in row.iter().enumerate() {
                    if cell == c {
                        result.push_str(&format!("{}{}", i + 1, j + 1));
                        break;
                    }
                }
            }
        } else if c == ' ' {
            result.push(' ');
        }
    }

    result
}

/// 解码：将坐标转为字母
pub fn decode(input: &str) -> Result<String, String> {
    let mut result = String::new();
    let digits: Vec<char> = input.chars().filter(|c| c.is_ascii_digit()).collect();

    if digits.len() % 2 != 0 {
        return Err("Polybius input must have even number of digits".to_string());
    }

    for chunk in digits.chunks(2) {
        let row = chunk[0].to_digit(10).ok_or("Invalid digit")? as usize;
        let col = chunk[1].to_digit(10).ok_or("Invalid digit")? as usize;

        if !(1..=5).contains(&row) || !(1..=5).contains(&col) {
            return Err(format!("Invalid coordinates: {}{}", row, col));
        }

        result.push(SQUARE[row - 1][col - 1]);
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_polybius_encode() {
        assert_eq!(encode("HELLO"), "2315313134");
        assert_eq!(encode("ABC"), "111213");
    }

    #[test]
    fn test_polybius_decode() {
        assert_eq!(decode("2315313134").unwrap(), "HELLO");
        assert_eq!(decode("111213").unwrap(), "ABC");
    }

    #[test]
    fn test_polybius_roundtrip() {
        let original = "CRYPTOGRAPHY";
        let encoded = encode(original);
        let decoded = decode(&encoded).unwrap();
        // J 会被转为 I
        assert_eq!(decoded, original);
    }
}
