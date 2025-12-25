//! Base85 (Ascii85) encoding/decoding

const ALPHABET: &[u8] =
    b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~";

pub fn encode(input: &str) -> String {
    let bytes = input.as_bytes();
    if bytes.is_empty() {
        return String::new();
    }

    let mut result = Vec::new();

    // Process 4 bytes at a time
    for chunk in bytes.chunks(4) {
        let mut value: u32 = 0;
        for (i, &byte) in chunk.iter().enumerate() {
            value |= (byte as u32) << (24 - i * 8);
        }

        // Pad if chunk is less than 4 bytes
        if chunk.len() < 4 {
            value >>= (4 - chunk.len()) * 8;
            value <<= (4 - chunk.len()) * 8;
        }

        // Special case: all zeros
        if value == 0 && chunk.len() == 4 {
            result.push(b'z');
        } else {
            // Convert to base85
            let mut encoded = [0u8; 5];
            for i in (0..5).rev() {
                encoded[i] = ALPHABET[(value % 85) as usize];
                value /= 85;
            }

            // Only output needed characters
            let output_len = chunk.len() + 1;
            result.extend_from_slice(&encoded[..output_len]);
        }
    }

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

    let mut result = Vec::new();
    let bytes: Vec<u8> = input.bytes().collect();
    let mut i = 0;

    while i < bytes.len() {
        // Handle 'z' shortcut for all zeros
        if bytes[i] == b'z' {
            result.extend_from_slice(&[0, 0, 0, 0]);
            i += 1;
            continue;
        }

        // Read up to 5 characters
        let chunk_end = (i + 5).min(bytes.len());
        let chunk = &bytes[i..chunk_end];
        let chunk_len = chunk.len();

        let mut value: u64 = 0;
        for &c in chunk {
            let c_idx = c as usize;
            if c_idx >= 128 || table[c_idx] == 255 {
                return Err(format!("Invalid Base85 character: {}", c as char));
            }
            value = value * 85 + table[c_idx] as u64;
        }

        // Pad with 'u' (84) for short chunks
        for _ in chunk_len..5 {
            value = value * 85 + 84;
        }

        // Extract bytes
        let output_len = chunk_len - 1;
        let decoded = [
            ((value >> 24) & 0xff) as u8,
            ((value >> 16) & 0xff) as u8,
            ((value >> 8) & 0xff) as u8,
            (value & 0xff) as u8,
        ];
        result.extend_from_slice(&decoded[..output_len]);

        i = chunk_end;
    }

    String::from_utf8(result).map_err(|e| format!("Invalid UTF-8: {}", e))
}
