//! Bacon cipher encoding/decoding
//! Uses 5-bit binary representation: A=aaaaa, B=aaaab, etc.

use std::collections::HashMap;

fn get_bacon_table() -> HashMap<char, &'static str> {
    let mut table = HashMap::new();
    table.insert('A', "aaaaa");
    table.insert('B', "aaaab");
    table.insert('C', "aaaba");
    table.insert('D', "aaabb");
    table.insert('E', "aabaa");
    table.insert('F', "aabab");
    table.insert('G', "aabba");
    table.insert('H', "aabbb");
    table.insert('I', "abaaa"); // I and J share
    table.insert('J', "abaaa");
    table.insert('K', "abaab");
    table.insert('L', "ababa");
    table.insert('M', "ababb");
    table.insert('N', "abbaa");
    table.insert('O', "abbab");
    table.insert('P', "abbba");
    table.insert('Q', "abbbb");
    table.insert('R', "baaaa");
    table.insert('S', "baaab");
    table.insert('T', "baaba");
    table.insert('U', "baabb"); // U and V share
    table.insert('V', "baabb");
    table.insert('W', "babaa");
    table.insert('X', "babab");
    table.insert('Y', "babba");
    table.insert('Z', "babbb");
    table
}

fn get_reverse_bacon_table() -> HashMap<&'static str, char> {
    let mut table = HashMap::new();
    table.insert("aaaaa", 'A');
    table.insert("aaaab", 'B');
    table.insert("aaaba", 'C');
    table.insert("aaabb", 'D');
    table.insert("aabaa", 'E');
    table.insert("aabab", 'F');
    table.insert("aabba", 'G');
    table.insert("aabbb", 'H');
    table.insert("abaaa", 'I');
    table.insert("abaab", 'K');
    table.insert("ababa", 'L');
    table.insert("ababb", 'M');
    table.insert("abbaa", 'N');
    table.insert("abbab", 'O');
    table.insert("abbba", 'P');
    table.insert("abbbb", 'Q');
    table.insert("baaaa", 'R');
    table.insert("baaab", 'S');
    table.insert("baaba", 'T');
    table.insert("baabb", 'U');
    table.insert("babaa", 'W');
    table.insert("babab", 'X');
    table.insert("babba", 'Y');
    table.insert("babbb", 'Z');
    table
}

pub fn encode(input: &str) -> String {
    let table = get_bacon_table();
    let mut result = Vec::new();

    for c in input.to_uppercase().chars() {
        if let Some(&code) = table.get(&c) {
            result.push(code);
        } else if c.is_whitespace() {
            result.push(" ");
        }
    }

    result.join("")
}

pub fn decode(input: &str) -> Result<String, String> {
    let table = get_reverse_bacon_table();
    let mut result = String::new();

    // Normalize input: treat uppercase as 'B', lowercase as 'A'
    // Or if input is already a/b, use as-is
    let normalized: String = input
        .chars()
        .filter_map(|c| {
            if c == 'a' || c == 'A' {
                Some('a')
            } else if c == 'b' || c == 'B' {
                Some('b')
            } else if c.is_whitespace() {
                Some(' ')
            } else {
                None
            }
        })
        .collect();

    // Split by spaces and decode each group
    for word in normalized.split_whitespace() {
        for chunk in word.as_bytes().chunks(5) {
            if chunk.len() == 5 {
                let code = std::str::from_utf8(chunk).unwrap_or("");
                if let Some(&c) = table.get(code) {
                    result.push(c);
                }
            }
        }
        // Add space between words if needed
        if !result.is_empty() && !result.ends_with(' ') {
            // Don't add extra spaces
        }
    }

    if result.is_empty() {
        // Try decoding without word splitting
        let no_space: String = normalized.chars().filter(|c| !c.is_whitespace()).collect();
        for chunk in no_space.as_bytes().chunks(5) {
            if chunk.len() == 5 {
                let code = std::str::from_utf8(chunk).unwrap_or("");
                if let Some(&c) = table.get(code) {
                    result.push(c);
                }
            }
        }
    }

    Ok(result)
}
