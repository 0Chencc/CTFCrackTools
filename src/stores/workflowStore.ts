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

// 工作流文件格式
interface WorkflowFile {
  version: string;
  name: string;
  createdAt: string;
  nodes: CustomNode[];
  edges: CustomEdge[];
}

// Rust 后端返回的类型
interface BackendNode {
  id: string;
  type: string;
  data: BaseNodeData;
  position?: { x: number; y: number };
}

interface ExecutionResult {
  nodes: BackendNode[];
  success: boolean;
  error: string | null;
}

// 节点间距常量 - 匹配紧凑节点尺寸
const NODE_GAP_X = 240;
const NODE_GAP_Y = 0;
const START_X = 80;
const START_Y = 150;

// 生成唯一 ID
let nodeIdCounter = 0;
const generateNodeId = () => `node_${Date.now()}_${nodeIdCounter++}`;
const generateEdgeId = () => `edge_${Date.now()}_${nodeIdCounter++}`;

interface WorkflowState {
  nodes: CustomNode[];
  edges: CustomEdge[];
  selectedNodeId: string | null;
  isExecuting: boolean;

  // 节点操作
  setNodes: (nodes: CustomNode[]) => void;
  addNode: (node: CustomNode) => void;
  updateNode: (id: string, data: Partial<BaseNodeData>) => void;
  removeNode: (id: string) => void;
  deleteNode: (id: string) => void;
  onNodesChange: (changes: NodeChange[]) => void;

  // 边操作
  setEdges: (edges: CustomEdge[]) => void;
  onEdgesChange: (changes: EdgeChange[]) => void;
  onConnect: (connection: Connection) => void;

  // 选择
  setSelectedNodeId: (id: string | null) => void;
  getSelectedNode: () => CustomNode | null;

  // 智能创建 - 一键工作流
  createQuickWorkflow: (algorithm: string, mode: "encode" | "decode") => void;

  // 智能追加 - 在选中节点后追加
  appendToNode: (targetNodeId: string, algorithm: string, mode: "encode" | "decode") => void;

  // 追加输出节点
  appendOutputNode: (targetNodeId: string) => void;

  // 执行
  executeWorkflow: () => Promise<void>;

  // 保存/加载
  saveWorkflow: () => Promise<void>;
  loadWorkflow: () => Promise<void>;

  // 清空
  clear: () => void;
}

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  nodes: [],
  edges: [],
  selectedNodeId: null,
  isExecuting: false,

  setNodes: (nodes) => set({ nodes }),

  addNode: (node) =>
    set((state) => ({
      nodes: [...state.nodes, node],
    })),

  updateNode: (id, data) =>
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === id
          ? { ...node, data: { ...node.data, ...data } as BaseNodeData }
          : node
      ) as CustomNode[],
    })),

  removeNode: (id) =>
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== id),
      edges: state.edges.filter(
        (edge) => edge.source !== id && edge.target !== id
      ),
    })),

  deleteNode: (id) =>
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== id),
      edges: state.edges.filter(
        (edge) => edge.source !== id && edge.target !== id
      ),
      selectedNodeId: state.selectedNodeId === id ? null : state.selectedNodeId,
    })),

  onNodesChange: (changes) =>
    set((state) => ({
      nodes: applyNodeChanges(changes, state.nodes) as CustomNode[],
    })),

  setEdges: (edges) => set({ edges }),

  onEdgesChange: (changes) =>
    set((state) => ({
      edges: applyEdgeChanges(changes, state.edges),
    })),

  onConnect: (connection) =>
    set((state) => ({
      edges: addEdge(connection, state.edges),
    })),

  setSelectedNodeId: (id) => set({ selectedNodeId: id }),

  getSelectedNode: () => {
    const { nodes, selectedNodeId } = get();
    return nodes.find((n) => n.id === selectedNodeId) || null;
  },

  // 一键创建完整工作流：Input -> Encoding (自动执行)
  createQuickWorkflow: (algorithm, mode) => {
    const inputNode: CustomNode = {
      id: generateNodeId(),
      type: "input",
      position: { x: START_X, y: START_Y },
      data: {
        label: "Input",
        category: "input",
        status: "idle",
        value: "",
      },
    };

    const encodingNode: CustomNode = {
      id: generateNodeId(),
      type: "encoding",
      position: { x: START_X + NODE_GAP_X, y: START_Y },
      data: {
        label: `${algorithm.charAt(0).toUpperCase() + algorithm.slice(1)} ${mode.charAt(0).toUpperCase() + mode.slice(1)}`,
        category: "encoding",
        status: "idle",
        algorithm,
        mode,
      },
    };

    const edge: CustomEdge = {
      id: generateEdgeId(),
      source: inputNode.id,
      target: encodingNode.id,
    };

    set({
      nodes: [inputNode, encodingNode],
      edges: [edge],
      selectedNodeId: encodingNode.id, // 选中链条末端，确保后续追加顺序正确
    });
  },

  // 在指定节点后追加新的编码节点
  appendToNode: (targetNodeId, algorithm, mode) => {
    const { nodes, edges } = get();
    const targetNode = nodes.find((n) => n.id === targetNodeId);

    if (!targetNode) return;

    // 计算新节点位置（在目标节点右侧）
    const newX = targetNode.position.x + NODE_GAP_X;
    const newY = targetNode.position.y + NODE_GAP_Y;

    const newNode: CustomNode = {
      id: generateNodeId(),
      type: "encoding",
      position: { x: newX, y: newY },
      data: {
        label: `${algorithm.charAt(0).toUpperCase() + algorithm.slice(1)} ${mode.charAt(0).toUpperCase() + mode.slice(1)}`,
        category: "encoding",
        status: "idle",
        algorithm,
        mode,
      },
    };

    const newEdge: CustomEdge = {
      id: generateEdgeId(),
      source: targetNodeId,
      target: newNode.id,
    };

    // 如果目标节点已有下游连接，需要重新连接
    const existingDownstreamEdges = edges.filter((e) => e.source === targetNodeId);
    const updatedEdges = edges.filter((e) => e.source !== targetNodeId);

    // 将原有下游连接移到新节点
    const reconnectedEdges = existingDownstreamEdges.map((e) => ({
      ...e,
      id: generateEdgeId(),
      source: newNode.id,
    }));

    set({
      nodes: [...nodes, newNode],
      edges: [...updatedEdges, newEdge, ...reconnectedEdges],
      selectedNodeId: newNode.id,
    });

    // 自动执行工作流
    setTimeout(() => get().executeWorkflow(), 100);
  },

  // 追加输出节点
  appendOutputNode: (targetNodeId) => {
    const { nodes, edges } = get();
    const targetNode = nodes.find((n) => n.id === targetNodeId);

    if (!targetNode) return;

    // 计算新节点位置（在目标节点右侧）
    const newX = targetNode.position.x + NODE_GAP_X;
    const newY = targetNode.position.y + NODE_GAP_Y;

    const newNode: CustomNode = {
      id: generateNodeId(),
      type: "output",
      position: { x: newX, y: newY },
      data: {
        label: "Output",
        category: "output",
        status: "idle",
        value: "",
      },
    };

    const newEdge: CustomEdge = {
      id: generateEdgeId(),
      source: targetNodeId,
      target: newNode.id,
    };

    set({
      nodes: [...nodes, newNode],
      edges: [...edges, newEdge],
      selectedNodeId: newNode.id,
    });

    // 自动执行工作流
    setTimeout(() => get().executeWorkflow(), 100);
  },

  executeWorkflow: async () => {
    const { nodes, edges } = get();

    if (nodes.length === 0) return;

    // 设置所有节点为 running 状态
    set({
      isExecuting: true,
      nodes: nodes.map((node) => ({
        ...node,
        data: { ...node.data, status: "running" as const },
      })),
    });

    try {
      // 准备发送给后端的数据
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

      // 调用 Rust 后端
      const result = await invoke<ExecutionResult>("execute_workflow", {
        nodes: backendNodes,
        edges: backendEdges,
      });

      // 更新节点状态
      const currentNodes = get().nodes;
      const updatedNodes = currentNodes.map((node) => {
        const resultNode = result.nodes.find((n) => n.id === node.id);
        if (resultNode) {
          return {
            ...node,
            data: {
              ...node.data,
              ...resultNode.data,
            },
          };
        }
        return {
          ...node,
          data: { ...node.data, status: "idle" as const },
        };
      });

      set({ nodes: updatedNodes, isExecuting: false });
    } catch (error) {
      // 发生错误时重置状态
      const currentNodes = get().nodes;
      set({
        isExecuting: false,
        nodes: currentNodes.map((node) => ({
          ...node,
          data: {
            ...node.data,
            status: "error" as const,
            error: error instanceof Error ? error.message : String(error),
          },
        })),
      });
    }
  },

  saveWorkflow: async () => {
    const { nodes, edges } = get();

    if (nodes.length === 0) {
      return;
    }

    try {
      const filePath = await save({
        filters: [{ name: "CTFCrackTools Workflow", extensions: ["ctfw"] }],
        defaultPath: "workflow.ctfw",
      });

      if (filePath) {
        const workflowData: WorkflowFile = {
          version: "1.0",
          name: "Untitled Workflow",
          createdAt: new Date().toISOString(),
          nodes,
          edges,
        };

        await writeTextFile(filePath, JSON.stringify(workflowData, null, 2));
      }
    } catch (error) {
      console.error("Failed to save workflow:", error);
    }
  },

  loadWorkflow: async () => {
    try {
      const filePath = await open({
        filters: [{ name: "CTFCrackTools Workflow", extensions: ["ctfw"] }],
        multiple: false,
      });

      if (filePath && typeof filePath === "string") {
        const content = await readTextFile(filePath);
        const workflowData: WorkflowFile = JSON.parse(content);

        if (workflowData.version && workflowData.nodes && workflowData.edges) {
          set({
            nodes: workflowData.nodes,
            edges: workflowData.edges,
            selectedNodeId: null,
            isExecuting: false,
          });

          // 加载后自动执行
          setTimeout(() => get().executeWorkflow(), 100);
        }
      }
    } catch (error) {
      console.error("Failed to load workflow:", error);
    }
  },

  clear: () => set({ nodes: [], edges: [], selectedNodeId: null, isExecuting: false }),
}));
