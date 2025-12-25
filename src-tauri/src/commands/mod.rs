use serde::{Deserialize, Serialize};

use crate::crypto;
use crate::encoding;
use crate::hash;
use crate::text;

/// 工作流节点定义
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowNode {
    pub id: String,
    #[serde(rename = "type")]
    pub node_type: String,
    pub data: NodeData,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NodeData {
    pub label: String,
    pub category: String,
    pub status: String,
    #[serde(default)]
    pub value: Option<String>,
    #[serde(default)]
    pub mode: Option<String>,
    #[serde(default)]
    pub algorithm: Option<String>,
    #[serde(default)]
    pub result: Option<String>,
    #[serde(default)]
    pub error: Option<String>,
}

/// 工作流边定义
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowEdge {
    pub id: String,
    pub source: String,
    pub target: String,
}

/// 执行结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionResult {
    pub nodes: Vec<WorkflowNode>,
    pub success: bool,
    pub error: Option<String>,
}

/// Base64 编码命令
#[tauri::command]
pub fn base64_encode(input: &str) -> String {
    encoding::base64::encode(input)
}

/// Base64 解码命令
#[tauri::command]
pub fn base64_decode(input: &str) -> Result<String, String> {
    encoding::base64::decode(input)
}

/// 执行单个算法操作
fn execute_algorithm(input: &str, algorithm: &str, mode: &str) -> Result<String, String> {
    match (algorithm, mode) {
        // 基础编码
        ("base64", "encode") => Ok(encoding::base64::encode(input)),
        ("base64", "decode") => encoding::base64::decode(input),
        ("base32", "encode") => Ok(encoding::base32::encode(input)),
        ("base32", "decode") => encoding::base32::decode(input),
        ("hex", "encode") => Ok(encoding::hex::hex_encode(input)),
        ("hex", "decode") => encoding::hex::hex_decode(input),
        ("url", "encode") => Ok(encoding::url::encode(input)),
        ("url", "decode") => encoding::url::decode(input),
        // 额外编码
        ("rot13", "encode") => Ok(encoding::rot13::encode(input)),
        ("rot13", "decode") => encoding::rot13::decode(input),
        ("caesar", "encode") => Ok(encoding::caesar::encode(input)),
        ("caesar", "decode") => encoding::caesar::decode(input),
        ("xor", "encode") => Ok(encoding::xor::encode(input)),
        ("xor", "decode") => encoding::xor::decode(input),
        ("ascii", "encode") => Ok(encoding::ascii::encode(input)),
        ("ascii", "decode") => encoding::ascii::decode(input),
        ("binary", "encode") => Ok(encoding::binary::encode(input)),
        ("binary", "decode") => encoding::binary::decode(input),
        // 扩展编码
        ("base58", "encode") => Ok(encoding::base58::encode(input)),
        ("base58", "decode") => encoding::base58::decode(input),
        ("base85", "encode") => Ok(encoding::base85::encode(input)),
        ("base85", "decode") => encoding::base85::decode(input),
        ("morse", "encode") => Ok(encoding::morse::encode(input)),
        ("morse", "decode") => encoding::morse::decode(input),
        ("uuencode", "encode") => Ok(encoding::uuencode::encode(input)),
        ("uuencode", "decode") => encoding::uuencode::decode(input),
        // 扩展密码
        ("vigenere", "encode") => Ok(encoding::vigenere::encode(input)),
        ("vigenere", "decode") => encoding::vigenere::decode(input),
        ("atbash", "encode") => Ok(encoding::atbash::encode(input)),
        ("atbash", "decode") => encoding::atbash::decode(input),
        ("railfence", "encode") => Ok(encoding::railfence::encode(input)),
        ("railfence", "decode") => encoding::railfence::decode(input),
        ("bacon", "encode") => Ok(encoding::bacon::encode(input)),
        ("bacon", "decode") => encoding::bacon::decode(input),
        // 新增编码
        ("rot47", "encode") => Ok(encoding::rot47::encode(input)),
        ("rot47", "decode") => encoding::rot47::decode(input),
        ("unicode", "encode") => Ok(encoding::unicode::encode(input)),
        ("unicode", "decode") => encoding::unicode::decode(input),
        ("html_entity", "encode") => Ok(encoding::html_entity::encode(input)),
        ("html_entity", "decode") => encoding::html_entity::decode(input),
        ("jwt", "decode") => encoding::jwt::decode(input),
        ("jwt", "encode") => Ok("JWT encoding not supported (requires key)".to_string()),
        ("brainfuck", "encode") => Ok(encoding::brainfuck::encode(input)),
        ("brainfuck", "decode") => encoding::brainfuck::decode(input),
        // 新增古典密码
        ("playfair", "encode") => Ok(encoding::playfair::encode(input)),
        ("playfair", "decode") => encoding::playfair::decode(input),
        ("polybius", "encode") => Ok(encoding::polybius::encode(input)),
        ("polybius", "decode") => encoding::polybius::decode(input),
        ("affine", "encode") => Ok(encoding::affine::encode(input)),
        ("affine", "decode") => encoding::affine::decode(input),
        ("beaufort", "encode") => Ok(encoding::beaufort::encode(input)),
        ("beaufort", "decode") => encoding::beaufort::decode(input),
        // 哈希算法 (mode 无关)
        ("md5", _) => Ok(hash::md5_hash(input)),
        ("sha1", _) => Ok(hash::sha1_hash(input)),
        ("sha256", _) => Ok(hash::sha256_hash(input)),
        ("sha512", _) => Ok(hash::sha512_hash(input)),
        // HMAC 和 KDF
        ("hmac_sha256", _) => Ok(hash::hmac_sha256(input)),
        ("pbkdf2", _) => Ok(hash::pbkdf2_derive(input)),
        // 加密算法
        ("aes", "encode") => Ok(crypto::aes_encrypt(input)),
        ("aes", "decode") => crypto::aes_decrypt(input),
        ("rc4", "encode") => Ok(crypto::rc4_encrypt(input)),
        ("rc4", "decode") => crypto::rc4_decrypt(input),
        ("des", "encode") => Ok(crypto::des_encrypt(input)),
        ("des", "decode") => crypto::des_decrypt(input),
        ("3des", "encode") => Ok(crypto::triple_des_encrypt(input)),
        ("3des", "decode") => crypto::triple_des_decrypt(input),
        ("blowfish", "encode") => Ok(crypto::blowfish_encrypt(input)),
        ("blowfish", "decode") => crypto::blowfish_decrypt(input),
        // 文本处理 (mode 无关)
        ("uppercase", _) => Ok(text::uppercase(input)),
        ("lowercase", _) => Ok(text::lowercase(input)),
        ("reverse", _) => Ok(text::reverse(input)),
        ("trim", _) => Ok(text::trim(input)),
        ("remove_spaces", _) => Ok(text::remove_spaces(input)),
        ("capitalize", _) => Ok(text::capitalize(input)),
        ("swap_case", _) => Ok(text::swap_case(input)),
        ("length", _) => Ok(text::length(input)),
        _ => Err(format!("Unsupported: {} {}", algorithm, mode)),
    }
}

/// 执行工作流
#[tauri::command]
pub fn execute_workflow(nodes: Vec<WorkflowNode>, edges: Vec<WorkflowEdge>) -> ExecutionResult {
    use std::collections::HashMap;

    let mut node_map: HashMap<String, WorkflowNode> =
        nodes.into_iter().map(|n| (n.id.clone(), n)).collect();

    // 构建连接图: target -> source (每个节点的输入来源)
    let connection_map: HashMap<String, String> = edges
        .iter()
        .map(|e| (e.target.clone(), e.source.clone()))
        .collect();

    // 构建反向图: source -> [targets] (每个节点的输出目标)
    let mut downstream_map: HashMap<String, Vec<String>> = HashMap::new();
    for edge in &edges {
        downstream_map
            .entry(edge.source.clone())
            .or_default()
            .push(edge.target.clone());
    }

    // 拓扑排序：确保按依赖顺序执行节点
    let sorted_nodes = topological_sort(&node_map, &connection_map);

    // 按拓扑顺序执行节点
    for node_id in sorted_nodes {
        let node = match node_map.get(&node_id) {
            Some(n) => n.clone(),
            None => continue,
        };

        // 只处理编码节点
        if node.data.category != "encoding" {
            continue;
        }

        // 获取输入值：优先从源节点的 result 获取，否则从 value 获取
        let input_value = if let Some(source_id) = connection_map.get(&node_id) {
            node_map
                .get(source_id)
                .and_then(|n| {
                    // 优先使用 result（编码节点的输出），其次使用 value（输入节点的值）
                    n.data.result.clone().or_else(|| n.data.value.clone())
                })
                .unwrap_or_default()
        } else {
            String::new()
        };

        let mode = node
            .data
            .mode
            .clone()
            .unwrap_or_else(|| "decode".to_string());
        let algorithm = node
            .data
            .algorithm
            .clone()
            .unwrap_or_else(|| "base64".to_string());

        let result = execute_algorithm(&input_value, &algorithm, &mode);

        if let Some(node_mut) = node_map.get_mut(&node_id) {
            match result {
                Ok(value) => {
                    node_mut.data.result = Some(value.clone());
                    node_mut.data.status = "success".to_string();
                    node_mut.data.error = None;
                }
                Err(e) => {
                    node_mut.data.error = Some(e);
                    node_mut.data.status = "error".to_string();
                    node_mut.data.result = None;
                }
            }
        }
    }

    // 最后传播结果到输出节点
    propagate_all_outputs(&mut node_map, &connection_map);

    ExecutionResult {
        nodes: node_map.into_values().collect(),
        success: true,
        error: None,
    }
}

/// 拓扑排序：返回按依赖顺序排列的节点 ID
fn topological_sort(
    node_map: &std::collections::HashMap<String, WorkflowNode>,
    connection_map: &std::collections::HashMap<String, String>,
) -> Vec<String> {
    use std::collections::{HashMap, VecDeque};

    // 计算每个节点的入度
    let mut in_degree: HashMap<String, usize> = node_map.keys().map(|id| (id.clone(), 0)).collect();
    for target in connection_map.keys() {
        if let Some(degree) = in_degree.get_mut(target) {
            *degree += 1;
        }
    }

    // 构建反向图
    let mut downstream: HashMap<String, Vec<String>> = HashMap::new();
    for (target, source) in connection_map {
        downstream
            .entry(source.clone())
            .or_default()
            .push(target.clone());
    }

    // BFS 拓扑排序
    let mut queue: VecDeque<String> = in_degree
        .iter()
        .filter(|(_, &deg)| deg == 0)
        .map(|(id, _)| id.clone())
        .collect();

    let mut result = Vec::new();

    while let Some(node_id) = queue.pop_front() {
        result.push(node_id.clone());

        if let Some(targets) = downstream.get(&node_id) {
            for target in targets {
                if let Some(degree) = in_degree.get_mut(target) {
                    *degree -= 1;
                    if *degree == 0 {
                        queue.push_back(target.clone());
                    }
                }
            }
        }
    }

    result
}

/// 将所有编码节点的结果传播到输出节点
fn propagate_all_outputs(
    node_map: &mut std::collections::HashMap<String, WorkflowNode>,
    connection_map: &std::collections::HashMap<String, String>,
) {
    // 找出所有输出节点及其源
    let output_updates: Vec<(String, String)> = node_map
        .iter()
        .filter(|(_, n)| n.data.category == "output")
        .filter_map(|(id, _)| {
            connection_map.get(id).and_then(|source_id| {
                node_map
                    .get(source_id)
                    .and_then(|source| {
                        source
                            .data
                            .result
                            .clone()
                            .or_else(|| source.data.value.clone())
                    })
                    .map(|value| (id.clone(), value))
            })
        })
        .collect();

    // 更新输出节点
    for (node_id, value) in output_updates {
        if let Some(node) = node_map.get_mut(&node_id) {
            node.data.value = Some(value);
            node.data.status = "success".to_string();
        }
    }
}
