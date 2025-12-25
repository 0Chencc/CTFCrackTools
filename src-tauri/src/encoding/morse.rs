//! Morse code encoding/decoding
use std::collections::HashMap;

fn get_morse_table() -> HashMap<char, &'static str> {
    let mut table = HashMap::new();
    // Letters
    table.insert('A', ".-");
    table.insert('B', "-...");
    table.insert('C', "-.-.");
    table.insert('D', "-..");
    table.insert('E', ".");
    table.insert('F', "..-.");
    table.insert('G', "--.");
    table.insert('H', "....");
    table.insert('I', "..");
    table.insert('J', ".---");
    table.insert('K', "-.-");
    table.insert('L', ".-..");
    table.insert('M', "--");
    table.insert('N', "-.");
    table.insert('O', "---");
    table.insert('P', ".--.");
    table.insert('Q', "--.-");
    table.insert('R', ".-.");
    table.insert('S', "...");
    table.insert('T', "-");
    table.insert('U', "..-");
    table.insert('V', "...-");
    table.insert('W', ".--");
    table.insert('X', "-..-");
    table.insert('Y', "-.--");
    table.insert('Z', "--..");
    // Numbers
    table.insert('0', "-----");
    table.insert('1', ".----");
    table.insert('2', "..---");
    table.insert('3', "...--");
    table.insert('4', "....-");
    table.insert('5', ".....");
    table.insert('6', "-....");
    table.insert('7', "--...");
    table.insert('8', "---..");
    table.insert('9', "----.");
    // Punctuation
    table.insert('.', ".-.-.-");
    table.insert(',', "--..--");
    table.insert('?', "..--..");
    table.insert('\'', ".----.");
    table.insert('!', "-.-.--");
    table.insert('/', "-..-.");
    table.insert('(', "-.--.");
    table.insert(')', "-.--.-");
    table.insert('&', ".-...");
    table.insert(':', "---...");
    table.insert(';', "-.-.-.");
    table.insert('=', "-...-");
    table.insert('+', ".-.-.");
    table.insert('-', "-....-");
    table.insert('_', "..--.-");
    table.insert('"', ".-..-.");
    table.insert('$', "...-..-");
    table.insert('@', ".--.-.");
    table
}

fn get_reverse_morse_table() -> HashMap<&'static str, char> {
    get_morse_table().into_iter().map(|(k, v)| (v, k)).collect()
}

pub fn encode(input: &str) -> String {
    let table = get_morse_table();
    let mut result = Vec::new();

    for word in input.split_whitespace() {
        let mut word_codes = Vec::new();
        for c in word.to_uppercase().chars() {
            if let Some(&code) = table.get(&c) {
                word_codes.push(code);
            }
        }
        if !word_codes.is_empty() {
            result.push(word_codes.join(" "));
        }
    }

    result.join(" / ")
}

pub fn decode(input: &str) -> Result<String, String> {
    let table = get_reverse_morse_table();
    let mut result = String::new();

    // Split by word separator (/)
    for word in input.split('/') {
        let word = word.trim();
        if word.is_empty() {
            continue;
        }

        if !result.is_empty() {
            result.push(' ');
        }

        // Split by character separator (space)
        for code in word.split_whitespace() {
            if let Some(&c) = table.get(code) {
                result.push(c);
            } else {
                return Err(format!("Unknown Morse code: {}", code));
            }
        }
    }

    Ok(result)
}
