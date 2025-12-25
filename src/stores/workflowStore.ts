import { create } from "zustand";
import {
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  type Connection,
  type NodeChange,
  type EdgeChange,
} from "reactflow";
import { invoke } from "@tauri-apps/api/core";
import { save, open } from "@tauri-apps/plugin-dialog";
import { readTextFile, writeTextFile } from "@tauri-apps/plugin-fs";
import type { CustomNode, CustomEdge, BaseNodeData } from "@/types/node";

// 节点间距常量
const NODE_GAP_X = 240;
const NODE_GAP_Y = 0;
const START_X = 80;
const START_Y = 150;

// ID 生成器
let nodeIdCounter = 0;
const generateNodeId = () => `node_${Date.now()}_${nodeIdCounter++}`;
const generateEdgeId = () => `edge_${Date.now()}_${nodeIdCounter++}`;

// 工作流文件格式
interface WorkflowFile {
  version: string;
  name: string;
  createdAt: string;
  nodes: CustomNode[];
  edges: CustomEdge[];
}

// 后端返回类型
interface BackendNode {
  id: string;
  type: string;
  data: BaseNodeData;
}

interface ExecutionResult {
  nodes: BackendNode[];
  success: boolean;
  error: string | null;
}

// 创建节点辅助函数
function createInputNode(): CustomNode {
  return {
    id: generateNodeId(),
    type: "input",
    position: { x: START_X, y: START_Y },
    data: { label: "Input", category: "input", status: "idle", value: "" },
  };
}

function createEncodingNode(algorithm: string, mode: "encode" | "decode", x: number, y: number): CustomNode {
  return {
    id: generateNodeId(),
    type: "encoding",
    position: { x, y },
    data: {
      label: `${algorithm.charAt(0).toUpperCase() + algorithm.slice(1)} ${mode.charAt(0).toUpperCase() + mode.slice(1)}`,
      category: "encoding",
      status: "idle",
      algorithm,
      mode,
    },
  };
}

function createOutputNode(x: number, y: number): CustomNode {
  return {
    id: generateNodeId(),
    type: "output",
    position: { x, y },
    data: { label: "Output", category: "output", status: "idle", value: "" },
  };
}

function createEdge(source: string, target: string): CustomEdge {
  return { id: generateEdgeId(), source, target };
}

// 工作流执行逻辑
async function runWorkflowExecution(nodes: CustomNode[], edges: CustomEdge[]): Promise<ExecutionResult> {
  const backendNodes = nodes.map((node) => ({
    id: node.id,
    type: node.type || "default",
    data: node.data,
  }));
  const backendEdges = edges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
  }));
  return invoke<ExecutionResult>("execute_workflow", { nodes: backendNodes, edges: backendEdges });
}

// 文件保存逻辑
async function saveWorkflowToFile(nodes: CustomNode[], edges: CustomEdge[]): Promise<void> {
  const filePath = await save({
    filters: [{ name: "CTFCrackTools Workflow", extensions: ["ctfw"] }],
    defaultPath: "workflow.ctfw",
  });
  if (filePath) {
    const data: WorkflowFile = {
      version: "1.0",
      name: "Untitled Workflow",
      createdAt: new Date().toISOString(),
      nodes,
      edges,
    };
    await writeTextFile(filePath, JSON.stringify(data, null, 2));
  }
}

// 文件加载逻辑
async function loadWorkflowFromFile(): Promise<WorkflowFile | null> {
  const filePath = await open({
    filters: [{ name: "CTFCrackTools Workflow", extensions: ["ctfw"] }],
    multiple: false,
  });
  if (filePath && typeof filePath === "string") {
    const content = await readTextFile(filePath);
    const data: WorkflowFile = JSON.parse(content);
    if (data.version && data.nodes && data.edges) {
      return data;
    }
  }
  return null;
}

interface WorkflowState {
  nodes: CustomNode[];
  edges: CustomEdge[];
  selectedNodeId: string | null;
  isExecuting: boolean;
  setNodes: (nodes: CustomNode[]) => void;
  addNode: (node: CustomNode) => void;
  updateNode: (id: string, data: Partial<BaseNodeData>) => void;
  removeNode: (id: string) => void;
  deleteNode: (id: string) => void;
  onNodesChange: (changes: NodeChange[]) => void;
  setEdges: (edges: CustomEdge[]) => void;
  onEdgesChange: (changes: EdgeChange[]) => void;
  onConnect: (connection: Connection) => void;
  setSelectedNodeId: (id: string | null) => void;
  getSelectedNode: () => CustomNode | null;
  createQuickWorkflow: (algorithm: string, mode: "encode" | "decode") => void;
  appendToNode: (targetNodeId: string, algorithm: string, mode: "encode" | "decode") => void;
  appendOutputNode: (targetNodeId: string) => void;
  executeWorkflow: () => Promise<void>;
  saveWorkflow: () => Promise<void>;
  loadWorkflow: () => Promise<void>;
  clear: () => void;
}

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  nodes: [],
  edges: [],
  selectedNodeId: null,
  isExecuting: false,

  setNodes: (nodes) => set({ nodes }),
  addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })),
  updateNode: (id, data) =>
    set((state) => ({
      nodes: state.nodes.map((n) => (n.id === id ? { ...n, data: { ...n.data, ...data } as BaseNodeData } : n)) as CustomNode[],
    })),
  removeNode: (id) => set((s) => ({ nodes: s.nodes.filter((n) => n.id !== id), edges: s.edges.filter((e) => e.source !== id && e.target !== id) })),
  deleteNode: (id) => set((s) => ({ nodes: s.nodes.filter((n) => n.id !== id), edges: s.edges.filter((e) => e.source !== id && e.target !== id), selectedNodeId: s.selectedNodeId === id ? null : s.selectedNodeId })),
  onNodesChange: (changes) => set((state) => ({ nodes: applyNodeChanges(changes, state.nodes) as CustomNode[] })),
  setEdges: (edges) => set({ edges }),
  onEdgesChange: (changes) => set((state) => ({ edges: applyEdgeChanges(changes, state.edges) })),
  onConnect: (connection) => set((state) => ({ edges: addEdge(connection, state.edges) })),
  setSelectedNodeId: (id) => set({ selectedNodeId: id }),
  getSelectedNode: () => get().nodes.find((n) => n.id === get().selectedNodeId) || null,

  createQuickWorkflow: (algorithm, mode) => {
    const inputNode = createInputNode();
    const encodingNode = createEncodingNode(algorithm, mode, START_X + NODE_GAP_X, START_Y);
    set({ nodes: [inputNode, encodingNode], edges: [createEdge(inputNode.id, encodingNode.id)], selectedNodeId: encodingNode.id });
  },

  appendToNode: (targetNodeId, algorithm, mode) => {
    const { nodes, edges } = get(); const target = nodes.find((n) => n.id === targetNodeId); if (!target) return;
    const newNode = createEncodingNode(algorithm, mode, target.position.x + NODE_GAP_X, target.position.y + NODE_GAP_Y);
    const downstream = edges.filter((e) => e.source === targetNodeId).map((e) => ({ ...e, id: generateEdgeId(), source: newNode.id }));
    set({ nodes: [...nodes, newNode], edges: [...edges.filter((e) => e.source !== targetNodeId), createEdge(targetNodeId, newNode.id), ...downstream], selectedNodeId: newNode.id });
    setTimeout(() => get().executeWorkflow(), 100);
  },
  appendOutputNode: (targetNodeId) => {
    const { nodes, edges } = get(); const target = nodes.find((n) => n.id === targetNodeId); if (!target) return;
    const newNode = createOutputNode(target.position.x + NODE_GAP_X, target.position.y + NODE_GAP_Y);
    set({ nodes: [...nodes, newNode], edges: [...edges, createEdge(targetNodeId, newNode.id)], selectedNodeId: newNode.id });
    setTimeout(() => get().executeWorkflow(), 100);
  },

  executeWorkflow: async () => {
    const { nodes, edges } = get();
    if (nodes.length === 0) return;
    set({ isExecuting: true, nodes: nodes.map((n) => ({ ...n, data: { ...n.data, status: "running" as const } })) });
    try {
      const result = await runWorkflowExecution(nodes, edges);
      set({
        isExecuting: false,
        nodes: get().nodes.map((n) => {
          const r = result.nodes.find((rn) => rn.id === n.id);
          return r ? { ...n, data: { ...n.data, ...r.data } } : { ...n, data: { ...n.data, status: "idle" as const } };
        }),
      });
    } catch (error) {
      set({
        isExecuting: false,
        nodes: get().nodes.map((n) => ({ ...n, data: { ...n.data, status: "error" as const, error: String(error) } })),
      });
    }
  },

  saveWorkflow: async () => {
    const { nodes, edges } = get();
    if (nodes.length === 0) return;
    try {
      await saveWorkflowToFile(nodes, edges);
    } catch (e) {
      console.error("Failed to save:", e);
    }
  },

  loadWorkflow: async () => {
    try {
      const data = await loadWorkflowFromFile();
      if (data) {
        set({ nodes: data.nodes, edges: data.edges, selectedNodeId: null, isExecuting: false });
        setTimeout(() => get().executeWorkflow(), 100);
      }
    } catch (e) {
      console.error("Failed to load:", e);
    }
  },

  clear: () => set({ nodes: [], edges: [], selectedNodeId: null, isExecuting: false }),
}));
