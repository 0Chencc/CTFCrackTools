//! Rail Fence cipher encoding/decoding
//! Default rails: 3

const DEFAULT_RAILS: usize = 3;

pub fn encode(input: &str) -> String {
    encode_with_rails(input, DEFAULT_RAILS)
}

pub fn encode_with_rails(input: &str, rails: usize) -> String {
    if rails <= 1 || input.is_empty() {
        return input.to_string();
    }

    let chars: Vec<char> = input.chars().collect();
    let mut fence: Vec<Vec<char>> = vec![Vec::new(); rails];

    let mut rail = 0;
    let mut direction = 1i32; // 1 = down, -1 = up

    for &c in &chars {
        fence[rail].push(c);

        // Change direction at top or bottom
        if rail == 0 {
            direction = 1;
        } else if rail == rails - 1 {
            direction = -1;
        }

        rail = (rail as i32 + direction) as usize;
    }

    // Read off the fence
    fence.into_iter().flatten().collect()
}

pub fn decode(input: &str) -> Result<String, String> {
    decode_with_rails(input, DEFAULT_RAILS)
}

pub fn decode_with_rails(input: &str, rails: usize) -> Result<String, String> {
    if rails <= 1 || input.is_empty() {
        return Ok(input.to_string());
    }

    let chars: Vec<char> = input.chars().collect();
    let len = chars.len();

    // Calculate the length of each rail
    let mut rail_lengths = vec![0usize; rails];
    let mut rail = 0;
    let mut direction = 1i32;

    for _ in 0..len {
        rail_lengths[rail] += 1;

        if rail == 0 {
            direction = 1;
        } else if rail == rails - 1 {
            direction = -1;
        }

        rail = (rail as i32 + direction) as usize;
    }

    // Split input into rails
    let mut fence: Vec<Vec<char>> = Vec::new();
    let mut pos = 0;
    for &length in &rail_lengths {
        fence.push(chars[pos..pos + length].to_vec());
        pos += length;
    }

    // Read off in zigzag pattern
    let mut result = String::new();
    let mut indices = vec![0usize; rails];
    let mut rail = 0;
    let mut direction = 1i32;

    for _ in 0..len {
        if indices[rail] < fence[rail].len() {
            result.push(fence[rail][indices[rail]]);
            indices[rail] += 1;
        }

        if rail == 0 {
            direction = 1;
        } else if rail == rails - 1 {
            direction = -1;
        }

        rail = (rail as i32 + direction) as usize;
    }

    Ok(result)
}
