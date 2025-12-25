//! Base58 encoding/decoding (Bitcoin alphabet)
//! Alphabet: 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz

const ALPHABET: &[u8] = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

pub fn encode(input: &str) -> String {
    let bytes = input.as_bytes();
    if bytes.is_empty() {
        return String::new();
    }

    // Count leading zeros
    let mut zeros = 0;
    for &b in bytes {
        if b == 0 {
            zeros += 1;
        } else {
            break;
        }
    }

    // Convert to base58
    let mut result = Vec::new();
    let mut num: Vec<u8> = bytes.to_vec();

    while !(num.is_empty() || (num.len() == 1 && num[0] == 0)) {
        let mut remainder = 0u32;
        let mut new_num = Vec::new();

        for &byte in &num {
            let current = (remainder << 8) + byte as u32;
            let div = current / 58;
            remainder = current % 58;
            if !new_num.is_empty() || div > 0 {
                new_num.push(div as u8);
            }
        }

        result.push(ALPHABET[remainder as usize]);
        num = new_num;
    }

    // Add leading '1's for leading zeros
    result.resize(result.len() + zeros, b'1');

    result.reverse();
    String::from_utf8(result).unwrap_or_default()
}

pub fn decode(input: &str) -> Result<String, String> {
    let input = input.trim();
    if input.is_empty() {
        return Ok(String::new());
    }

    // Build reverse lookup table
    let mut table = [255u8; 128];
    for (i, &c) in ALPHABET.iter().enumerate() {
        table[c as usize] = i as u8;
    }

    // Count leading '1's
    let mut zeros = 0;
    for c in input.chars() {
        if c == '1' {
            zeros += 1;
        } else {
            break;
        }
    }

    // Convert from base58
    let mut result: Vec<u8> = Vec::new();

    for c in input.chars() {
        let c_byte = c as usize;
        if c_byte >= 128 || table[c_byte] == 255 {
            return Err(format!("Invalid Base58 character: {}", c));
        }
        let val = table[c_byte] as u32;

        let mut carry = val;
        for byte in result.iter_mut().rev() {
            carry += (*byte as u32) * 58;
            *byte = (carry & 0xff) as u8;
            carry >>= 8;
        }

        while carry > 0 {
            result.insert(0, (carry & 0xff) as u8);
            carry >>= 8;
        }
    }

    // Add leading zeros
    let mut final_result = vec![0u8; zeros];
    final_result.extend(result);

    String::from_utf8(final_result).map_err(|e| format!("Invalid UTF-8: {}", e))
}
