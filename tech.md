# CTFCrackTools X 技术文档

## 项目愿景

**对标竞品**: CyberChef (GCHQ)

**核心差异化优势**:

| 维度 | CyberChef | CTFCrackTools X |
|------|-----------|-----------------|
| 运行方式 | 浏览器 Web 应用 | **本地桌面应用** |
| 操作模式 | 线性配方 (Recipe) | **节点化工作流** |
| 智能能力 | 无 | **本地 AI 辅助** |
| 体积 | 需联网 | **<10MB 离线可用** |
| 隐私安全 | 数据经过网络 | **完全本地处理** |

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        CTFCrackTools X                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    React Frontend                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │  React Flow │  │  Shadcn/UI  │  │  AI Chat Panel  │  │   │
│  │  │  (节点编辑器) │  │  (极简组件)  │  │  (智能助手)     │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                      Tauri IPC Bridge                           │
│                              │                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Rust Backend                         │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐    │   │
│  │  │  Crypto   │  │  Encoding │  │  Ollama Engine    │    │   │
│  │  │  Engine   │  │  Engine   │  │  (Local LLM)      │    │   │
│  │  └───────────┘  └───────────┘  └───────────────────┘    │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐    │   │
│  │  │  Node     │  │  Workflow │  │  Plugin System    │    │   │
│  │  │  Registry │  │  Engine   │  │  (WASM/Python)    │    │   │
│  │  └───────────┘  └───────────┘  └───────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 技术栈

| 层次 | 技术选型 | 版本 | 作用 |
|------|----------|------|------|
| 框架核心 | Rust + Tauri | v2.0 | 极小体积 (<10MB)、内存安全 |
| 前端 UI | React + TypeScript | React 18+ | 现代化界面、类型安全 |
| 构建工具 | Vite | 5.x | 极速开发体验、热更新 |
| 核心交互 | React Flow (XYFlow) | 12.x | 拖拽式节点编辑器 |
| UI 组件 | Shadcn/UI + Tailwind | - | 极简风界面 |
| AI 引擎 | Ollama (Rust bindings) | - | 本地 LLM 智能辅助 |

---

## 一、节点系统设计

### 1.1 节点类型分类

```
节点类型
├── 输入节点 (Input)
│   ├── TextInput        # 文本输入
│   ├── FileInput        # 文件输入
│   ├── HexInput         # 十六进制输入
│   └── ClipboardInput   # 剪贴板输入
│
├── 编码节点 (Encoding)
│   ├── Base64
│   ├── Base32
│   ├── Hex
│   ├── URL
│   ├── Unicode
│   ├── HTML Entity
│   └── Morse
│
├── 密码节点 (Crypto)
│   ├── Caesar
│   ├── ROT13
│   ├── Vigenere
│   ├── Fence (Rail Fence)
│   ├── Bacon
│   ├── Atbash
│   ├── AES
│   ├── DES
│   ├── RSA
│   └── XOR
│
├── 哈希节点 (Hash)
│   ├── MD5
│   ├── SHA1/256/512
│   ├── CRC32
│   └── HMAC
│
├── 工具节点 (Utils)
│   ├── Radix Convert    # 进制转换
│   ├── Reverse          # 字符串反转
│   ├── Split/Join       # 分割/合并
│   ├── Regex Match      # 正则匹配
│   ├── Find/Replace     # 查找替换
│   └── Length/Count     # 长度统计
│
├── AI 节点 (AI)
│   ├── AutoDetect       # 自动检测编码/加密类型
│   ├── SmartDecrypt     # 智能解密建议
│   ├── CodeExplain      # 代码/密文解释
│   └── CTFHint          # CTF 提示助手
│
└── 输出节点 (Output)
    ├── TextOutput       # 文本输出
    ├── FileOutput       # 文件输出
    ├── HexView          # 十六进制视图
    └── DiffView         # 差异对比视图
```

### 1.2 节点数据结构

```typescript
// src/types/node.ts
interface NodeData {
  id: string;
  type: NodeType;
  label: string;
  category: 'input' | 'encoding' | 'crypto' | 'hash' | 'utils' | 'ai' | 'output';

  // 节点配置
  config: Record<string, any>;

  // 输入输出端口
  inputs: Port[];
  outputs: Port[];

  // 运行状态
  status: 'idle' | 'running' | 'success' | 'error';
  result?: string;
  error?: string;
}

interface Port {
  id: string;
  name: string;
  type: 'string' | 'bytes' | 'number' | 'any';
  connected: boolean;
}

interface Edge {
  id: string;
  source: string;
  sourceHandle: string;
  target: string;
  targetHandle: string;
}

interface Workflow {
  id: string;
  name: string;
  nodes: NodeData[];
  edges: Edge[];
  createdAt: Date;
  updatedAt: Date;
}
```

### 1.3 节点执行引擎 (Rust)

```rust
// src-tauri/src/workflow/engine.rs
use std::collections::HashMap;
use petgraph::graph::DiGraph;
use petgraph::algo::toposort;

pub struct WorkflowEngine {
    nodes: HashMap<String, Box<dyn Node>>,
    graph: DiGraph<String, ()>,
}

impl WorkflowEngine {
    /// 拓扑排序后顺序执行节点
    pub fn execute(&self, workflow: &Workflow) -> Result<ExecutionResult, WorkflowError> {
        // 1. 构建依赖图
        let graph = self.build_graph(workflow)?;

        // 2. 拓扑排序确定执行顺序
        let order = toposort(&graph, None)
            .map_err(|_| WorkflowError::CyclicDependency)?;

        // 3. 按顺序执行每个节点
        let mut context = ExecutionContext::new();
        for node_id in order {
            let node = self.get_node(&node_id)?;
            let inputs = self.collect_inputs(&node_id, &context)?;
            let output = node.execute(inputs)?;
            context.set_output(&node_id, output);
        }

        Ok(context.into_result())
    }
}

pub trait Node: Send + Sync {
    fn id(&self) -> &str;
    fn execute(&self, input: NodeInput) -> Result<NodeOutput, NodeError>;
}
```

---

## 二、AI 智能化设计

### 2.1 Ollama 集成架构

```rust
// src-tauri/src/ai/ollama.rs
use reqwest::Client;
use serde::{Deserialize, Serialize};

pub struct OllamaClient {
    client: Client,
    base_url: String,
    model: String,
}

#[derive(Serialize)]
struct GenerateRequest {
    model: String,
    prompt: String,
    stream: bool,
    options: GenerateOptions,
}

#[derive(Deserialize)]
struct GenerateResponse {
    response: String,
    done: bool,
}

impl OllamaClient {
    pub fn new(base_url: &str, model: &str) -> Self {
        Self {
            client: Client::new(),
            base_url: base_url.to_string(),
            model: model.to_string(),
        }
    }

    /// 发送生成请求
    pub async fn generate(&self, prompt: &str) -> Result<String, AiError> {
        let request = GenerateRequest {
            model: self.model.clone(),
            prompt: prompt.to_string(),
            stream: false,
            options: GenerateOptions::default(),
        };

        let response = self.client
            .post(format!("{}/api/generate", self.base_url))
            .json(&request)
            .send()
            .await?
            .json::<GenerateResponse>()
            .await?;

        Ok(response.response)
    }

    /// 流式生成 (用于实时显示)
    pub async fn generate_stream(
        &self,
        prompt: &str,
        callback: impl Fn(&str),
    ) -> Result<String, AiError> {
        // 流式处理实现
    }
}
```

### 2.2 AI 功能模块

```rust
// src-tauri/src/ai/features.rs

/// 自动检测编码/加密类型
pub async fn auto_detect(input: &str, ollama: &OllamaClient) -> Result<DetectionResult, AiError> {
    let prompt = format!(
        r#"分析以下文本可能使用的编码或加密方式，给出最可能的 3 种类型及置信度：

文本: {}

请用 JSON 格式回复：
{{"detections": [{{"type": "类型名", "confidence": 0.95, "reason": "原因"}}]}}
"#,
        input
    );

    let response = ollama.generate(&prompt).await?;
    parse_detection_response(&response)
}

/// 智能解密建议
pub async fn smart_decrypt(
    input: &str,
    detected_type: &str,
    ollama: &OllamaClient,
) -> Result<DecryptSuggestion, AiError> {
    let prompt = format!(
        r#"这是一段 {} 编码/加密的文本: {}

请提供解密步骤和可能的密钥提示。"#,
        detected_type, input
    );

    ollama.generate(&prompt).await
}

/// CTF 提示助手
pub async fn ctf_hint(
    challenge_desc: &str,
    current_data: &str,
    ollama: &OllamaClient,
) -> Result<String, AiError> {
    let prompt = format!(
        r#"CTF 挑战描述: {}

当前数据: {}

请给出解题思路提示（不要直接给出答案）。"#,
        challenge_desc, current_data
    );

    ollama.generate(&prompt).await
}
```

### 2.3 推荐的本地模型

| 模型 | 大小 | 用途 | 推荐场景 |
|------|------|------|----------|
| qwen2.5:0.5b | ~400MB | 轻量快速 | 编码检测、简单分析 |
| qwen2.5:1.5b | ~1GB | 平衡选择 | 日常使用推荐 |
| qwen2.5:7b | ~4GB | 深度分析 | 复杂密码分析 |
| codellama:7b | ~4GB | 代码专长 | 代码混淆分析 |
| deepseek-coder:6.7b | ~4GB | 代码专长 | 代码逆向分析 |

---

## 三、前端架构

### 3.1 目录结构

```
src/
├── main.tsx                      # 入口
├── App.tsx                       # 主应用
│
├── components/
│   ├── ui/                       # Shadcn/UI 组件
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   │
│   ├── flow/                     # React Flow 相关
│   │   ├── FlowCanvas.tsx        # 画布组件
│   │   ├── NodePalette.tsx       # 节点面板
│   │   ├── MiniMap.tsx           # 小地图
│   │   └── Controls.tsx          # 控制栏
│   │
│   ├── nodes/                    # 节点组件
│   │   ├── BaseNode.tsx          # 基础节点
│   │   ├── InputNode.tsx
│   │   ├── EncodingNode.tsx
│   │   ├── CryptoNode.tsx
│   │   ├── AiNode.tsx
│   │   └── OutputNode.tsx
│   │
│   ├── ai/                       # AI 相关组件
│   │   ├── AiChatPanel.tsx       # AI 对话面板
│   │   ├── AiSuggestion.tsx      # AI 建议卡片
│   │   └── ModelSelector.tsx     # 模型选择器
│   │
│   └── layout/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── StatusBar.tsx
│
├── hooks/
│   ├── useWorkflow.ts            # 工作流 Hook
│   ├── useNodeExecution.ts       # 节点执行 Hook
│   ├── useAi.ts                  # AI 交互 Hook
│   └── useOllama.ts              # Ollama 连接 Hook
│
├── stores/
│   ├── workflowStore.ts          # 工作流状态
│   ├── settingsStore.ts          # 设置状态
│   └── aiStore.ts                # AI 状态
│
├── lib/
│   ├── tauri.ts                  # Tauri 命令封装
│   ├── nodes/                    # 节点定义
│   │   ├── registry.ts           # 节点注册表
│   │   ├── encodingNodes.ts
│   │   ├── cryptoNodes.ts
│   │   └── aiNodes.ts
│   └── utils/
│       └── workflow.ts           # 工作流工具
│
├── types/
│   ├── node.ts                   # 节点类型
│   ├── workflow.ts               # 工作流类型
│   └── ai.ts                     # AI 类型
│
└── styles/
    └── globals.css               # 全局样式
```

### 3.2 节点编辑器实现

```tsx
// src/components/flow/FlowCanvas.tsx
import { useCallback } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Node,
  Edge,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { nodeTypes } from '@/lib/nodes/registry';
import { useWorkflowStore } from '@/stores/workflowStore';
import { NodePalette } from './NodePalette';

export function FlowCanvas() {
  const { nodes, edges, setNodes, setEdges, executeWorkflow } = useWorkflowStore();

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');

      // 创建新节点
      const newNode = createNode(type, position);
      setNodes((nds) => nds.concat(newNode));
    },
    [setNodes]
  );

  return (
    <div className="flex h-full">
      {/* 左侧节点面板 */}
      <NodePalette />

      {/* 中间画布 */}
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDrop={onDrop}
          onDragOver={(e) => e.preventDefault()}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      {/* 右侧 AI 面板 */}
      <AiChatPanel />
    </div>
  );
}
```

### 3.3 自定义节点示例

```tsx
// src/components/nodes/EncodingNode.tsx
import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';

interface EncodingNodeData {
  label: string;
  mode: 'encode' | 'decode';
  algorithm: string;
  status: 'idle' | 'running' | 'success' | 'error';
  result?: string;
}

export const EncodingNode = memo(({ data, selected }: NodeProps<EncodingNodeData>) => {
  return (
    <Card className={`w-64 ${selected ? 'ring-2 ring-primary' : ''}`}>
      <CardHeader className="p-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm">{data.label}</CardTitle>
          <Badge variant={data.status === 'success' ? 'default' : 'secondary'}>
            {data.mode}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="p-3 pt-0">
        <Select defaultValue={data.algorithm}>
          <SelectTrigger className="h-8">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="base64">Base64</SelectItem>
            <SelectItem value="base32">Base32</SelectItem>
            <SelectItem value="hex">Hex</SelectItem>
            <SelectItem value="url">URL</SelectItem>
          </SelectContent>
        </Select>

        {data.result && (
          <div className="mt-2 p-2 bg-muted rounded text-xs font-mono truncate">
            {data.result}
          </div>
        )}
      </CardContent>

      {/* 输入端口 */}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-primary"
      />

      {/* 输出端口 */}
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-primary"
      />
    </Card>
  );
});
```

---

## 四、Rust 后端架构

### 4.1 目录结构

```
src-tauri/
├── Cargo.toml
├── tauri.conf.json
│
└── src/
    ├── main.rs                   # 入口
    ├── lib.rs                    # 库导出
    │
    ├── commands/                 # Tauri 命令
    │   ├── mod.rs
    │   ├── workflow.rs           # 工作流命令
    │   ├── encoding.rs           # 编码命令
    │   ├── crypto.rs             # 加密命令
    │   └── ai.rs                 # AI 命令
    │
    ├── workflow/                 # 工作流引擎
    │   ├── mod.rs
    │   ├── engine.rs             # 执行引擎
    │   ├── node.rs               # 节点 trait
    │   └── context.rs            # 执行上下文
    │
    ├── nodes/                    # 节点实现
    │   ├── mod.rs
    │   ├── encoding/
    │   │   ├── mod.rs
    │   │   ├── base64.rs
    │   │   ├── base32.rs
    │   │   ├── hex.rs
    │   │   ├── url.rs
    │   │   ├── unicode.rs
    │   │   ├── html.rs
    │   │   └── morse.rs
    │   ├── crypto/
    │   │   ├── mod.rs
    │   │   ├── caesar.rs
    │   │   ├── rot13.rs
    │   │   ├── vigenere.rs
    │   │   ├── fence.rs
    │   │   ├── bacon.rs
    │   │   ├── aes.rs
    │   │   └── xor.rs
    │   ├── hash/
    │   │   ├── mod.rs
    │   │   ├── md5.rs
    │   │   └── sha.rs
    │   └── utils/
    │       ├── mod.rs
    │       ├── radix.rs
    │       └── text.rs
    │
    ├── ai/                       # AI 模块
    │   ├── mod.rs
    │   ├── ollama.rs             # Ollama 客户端
    │   ├── features.rs           # AI 功能
    │   └── prompts.rs            # 提示词模板
    │
    └── error.rs                  # 错误处理
```

### 4.2 依赖配置

```toml
# src-tauri/Cargo.toml
[package]
name = "ctfcracktools-x"
version = "1.0.0"
edition = "2021"

[dependencies]
# Tauri
tauri = { version = "2", features = ["devtools"] }
tauri-plugin-store = "2"
tauri-plugin-dialog = "2"
tauri-plugin-fs = "2"

# 序列化
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# 异步
tokio = { version = "1", features = ["full"] }

# HTTP (Ollama 通信)
reqwest = { version = "0.12", features = ["json", "stream"] }

# 编码
base64 = "0.22"
data-encoding = "2"
percent-encoding = "2"
hex = "0.4"

# 加密
aes = "0.8"
des = "0.8"
rsa = "0.9"
md-5 = "0.10"
sha1 = "0.10"
sha2 = "0.10"

# 图算法 (工作流)
petgraph = "0.6"

# 错误处理
thiserror = "1"
anyhow = "1"

# 日志
tracing = "0.1"
tracing-subscriber = "0.3"

[build-dependencies]
tauri-build = { version = "2", features = [] }

[profile.release]
lto = true
codegen-units = 1
panic = "abort"
strip = true
```

---

## 五、UI 设计规范

### 5.1 配色方案

```css
/* 暗色主题 (默认) */
:root {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --card: 240 10% 3.9%;
  --card-foreground: 0 0% 98%;
  --primary: 142.1 76.2% 36.3%;       /* 绿色 - 代表解密成功 */
  --primary-foreground: 355.7 100% 97.3%;
  --secondary: 240 3.7% 15.9%;
  --accent: 12 6.5% 15.1%;
  --muted: 240 5.9% 10%;
  --destructive: 0 62.8% 30.6%;       /* 红色 - 代表错误 */
}

/* 节点颜色分类 */
.node-input { border-color: hsl(200, 80%, 50%); }     /* 蓝色 */
.node-encoding { border-color: hsl(120, 60%, 40%); }  /* 绿色 */
.node-crypto { border-color: hsl(280, 60%, 50%); }    /* 紫色 */
.node-hash { border-color: hsl(30, 80%, 50%); }       /* 橙色 */
.node-ai { border-color: hsl(340, 80%, 50%); }        /* 粉色 */
.node-output { border-color: hsl(60, 70%, 45%); }     /* 黄色 */
```

### 5.2 界面布局

```
┌──────────────────────────────────────────────────────────────────┐
│  Logo   [工作流名称]         [运行] [保存] [导出]    [设置] [AI] │
├──────────┬───────────────────────────────────────────┬───────────┤
│          │                                           │           │
│  节点    │                                           │   AI      │
│  面板    │              节点画布                      │   助手    │
│          │           (React Flow)                    │   面板    │
│  ────    │                                           │           │
│  输入    │                                           │  ┌─────┐  │
│  编码    │                                           │  │对话 │  │
│  加密    │                                           │  │历史 │  │
│  哈希    │                                           │  └─────┘  │
│  工具    │                                           │           │
│  AI      │                                           │  [输入框] │
│  输出    │                                           │           │
│          │                                           │           │
├──────────┴───────────────────────────────────────────┴───────────┤
│  状态栏: [节点数: 5] [连接: 4] [执行时间: 12ms] [Ollama: 已连接]  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 六、性能指标

| 指标 | 目标值 |
|------|--------|
| 应用体积 | < 10MB |
| 启动时间 | < 500ms |
| 内存占用 (空闲) | < 50MB |
| 内存占用 (运行) | < 150MB |
| 节点执行延迟 | < 10ms (单节点) |
| AI 响应 (首 token) | < 500ms (本地) |

---

## 七、与 CyberChef 功能对比

| 功能 | CyberChef | CTFCrackTools X |
|------|-----------|-----------------|
| Base64/32/16 | ✅ | ✅ |
| URL 编码 | ✅ | ✅ |
| 凯撒密码 | ✅ | ✅ |
| ROT13 | ✅ | ✅ |
| AES/DES | ✅ | ✅ |
| 正则匹配 | ✅ | ✅ |
| 文件操作 | ✅ | ✅ |
| **节点化工作流** | ❌ | ✅ |
| **可视化执行** | ❌ | ✅ |
| **本地 AI 辅助** | ❌ | ✅ |
| **自动类型检测** | 部分 | ✅ (AI) |
| **CTF 提示助手** | ❌ | ✅ |
| **完全离线** | ❌ | ✅ |
| **原生性能** | ❌ (JS) | ✅ (Rust) |

---

*文档更新时间: 2025-12-21*
*目标版本: CTFCrackTools X 1.0*
*技术栈: Rust + Tauri 2.0 + React Flow + Ollama*
