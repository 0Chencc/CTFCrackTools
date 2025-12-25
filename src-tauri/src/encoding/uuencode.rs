//! UUEncode encoding/decoding

fn encode_char(val: u8) -> char {
    if val == 0 {
        '`'
    } else {
        (val + 32) as char
    }
}

fn decode_char(c: char) -> u8 {
    let val = c as u8;
    if val == 96 {
        0
    } else {
        val.wrapping_sub(32) & 0x3f
    }
}

pub fn encode(input: &str) -> String {
    let bytes = input.as_bytes();
    if bytes.is_empty() {
        return String::new();
    }

    let mut result = String::new();

    // Process 45 bytes per line (produces 60 characters)
    for line_chunk in bytes.chunks(45) {
        // Length character
        result.push(encode_char(line_chunk.len() as u8));

        // Process 3 bytes at a time
        for chunk in line_chunk.chunks(3) {
            let mut vals = [0u8; 3];
            for (i, &b) in chunk.iter().enumerate() {
                vals[i] = b;
            }

            let b0 = vals[0];
            let b1 = vals[1];
            let b2 = vals[2];

            result.push(encode_char(b0 >> 2));
            result.push(encode_char(((b0 & 0x03) << 4) | (b1 >> 4)));
            result.push(encode_char(((b1 & 0x0f) << 2) | (b2 >> 6)));
            result.push(encode_char(b2 & 0x3f));
        }

        result.push('\n');
    }

    result
}

pub fn decode(input: &str) -> Result<String, String> {
    let mut result = Vec::new();

    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }

        let chars: Vec<char> = line.chars().collect();
        if chars.is_empty() {
            continue;
        }

        // First character is the length
        let expected_len = decode_char(chars[0]) as usize;
        if expected_len == 0 {
            continue;
        }

        // Process encoded characters
        let encoded = &chars[1..];
        let mut decoded_bytes = Vec::new();

        for chunk in encoded.chunks(4) {
            if chunk.len() < 4 {
                break;
            }

            let c0 = decode_char(chunk[0]);
            let c1 = decode_char(chunk[1]);
            let c2 = decode_char(chunk[2]);
            let c3 = decode_char(chunk[3]);

            decoded_bytes.push((c0 << 2) | (c1 >> 4));
            decoded_bytes.push((c1 << 4) | (c2 >> 2));
            decoded_bytes.push((c2 << 6) | c3);
        }

        // Truncate to expected length
        decoded_bytes.truncate(expected_len);
        result.extend(decoded_bytes);
    }

    String::from_utf8(result).map_err(|e| format!("Invalid UTF-8: {}", e))
}
