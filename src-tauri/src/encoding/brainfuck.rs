/// Brainfuck 解释器
/// 支持标准 Brainfuck 语法: > < + - . , [ ]
const MEMORY_SIZE: usize = 30000;
const MAX_ITERATIONS: usize = 1000000;

/// 将文本编码为 Brainfuck 代码
pub fn encode(input: &str) -> String {
    let mut result = String::new();
    let mut current: u8 = 0;

    for c in input.bytes() {
        let diff = c.wrapping_sub(current) as i16;
        let neg_diff = current.wrapping_sub(c) as i16;

        if diff.abs() <= neg_diff.abs() {
            // 正向移动更短
            if diff >= 0 {
                result.push_str(&"+".repeat(diff as usize));
            } else {
                result.push_str(&"-".repeat((-diff) as usize));
            }
        } else {
            // 负向移动更短
            result.push_str(&"-".repeat(neg_diff as usize));
        }

        result.push('.');
        current = c;
    }

    result
}

/// 执行 Brainfuck 代码并返回输出
pub fn decode(input: &str) -> Result<String, String> {
    // 过滤出有效的 Brainfuck 指令
    let code: Vec<char> = input
        .chars()
        .filter(|c| matches!(c, '>' | '<' | '+' | '-' | '.' | ',' | '[' | ']'))
        .collect();

    // 预处理：建立括号匹配表
    let brackets = build_bracket_map(&code)?;

    // 初始化内存和指针
    let mut memory = vec![0u8; MEMORY_SIZE];
    let mut ptr: usize = 0;
    let mut pc: usize = 0;
    let mut output = String::new();
    let mut iterations: usize = 0;

    while pc < code.len() {
        iterations += 1;
        if iterations > MAX_ITERATIONS {
            return Err(format!(
                "Execution limit exceeded ({} iterations). Possible infinite loop.",
                MAX_ITERATIONS
            ));
        }

        match code[pc] {
            '>' => {
                ptr = (ptr + 1) % MEMORY_SIZE;
            }
            '<' => {
                ptr = if ptr == 0 { MEMORY_SIZE - 1 } else { ptr - 1 };
            }
            '+' => {
                memory[ptr] = memory[ptr].wrapping_add(1);
            }
            '-' => {
                memory[ptr] = memory[ptr].wrapping_sub(1);
            }
            '.' => {
                output.push(memory[ptr] as char);
            }
            ',' => {
                // 输入操作：在这个上下文中跳过
                // 可以扩展为从额外参数读取
            }
            '[' => {
                if memory[ptr] == 0 {
                    pc = brackets[&pc];
                }
            }
            ']' => {
                if memory[ptr] != 0 {
                    pc = brackets[&pc];
                }
            }
            _ => {}
        }
        pc += 1;
    }

    Ok(output)
}

fn build_bracket_map(code: &[char]) -> Result<std::collections::HashMap<usize, usize>, String> {
    let mut map = std::collections::HashMap::new();
    let mut stack = Vec::new();

    for (i, &c) in code.iter().enumerate() {
        match c {
            '[' => {
                stack.push(i);
            }
            ']' => {
                if let Some(j) = stack.pop() {
                    map.insert(i, j);
                    map.insert(j, i);
                } else {
                    return Err(format!("Unmatched ']' at position {}", i));
                }
            }
            _ => {}
        }
    }

    if !stack.is_empty() {
        return Err(format!("Unmatched '[' at position {}", stack[0]));
    }

    Ok(map)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_brainfuck_hello() {
        // 一个简单的 "Hi" 程序
        let code = "+++++++++[>++++++++>+++++++++++>+++>+<<<<-]>.>++.+++++++..+++.>+++++.<<+++++++++++++++.>.+++.------.--------.>+.";
        let result = decode(code);
        assert!(result.is_ok());
    }

    #[test]
    fn test_brainfuck_simple() {
        // 输出 'A' (65)
        let code = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.";
        let result = decode(code).unwrap();
        assert_eq!(result, "C"); // 67 个 +
    }

    #[test]
    fn test_brainfuck_encode() {
        let encoded = encode("A");
        let decoded = decode(&encoded).unwrap();
        assert_eq!(decoded, "A");
    }
}
