import type { Node, Edge } from "reactflow";

export type NodeCategory =
  | "input"
  | "encoding"
  | "crypto"
  | "hash"
  | "utils"
  | "ai"
  | "output";

export type NodeStatus = "idle" | "running" | "success" | "error";

export interface BaseNodeData {
  label: string;
  category: NodeCategory;
  status: NodeStatus;
  result?: string;
  error?: string;
  // 通用字段
  value?: string;
  mode?: "encode" | "decode";
  algorithm?: string;
}

export type CustomNode = Node<BaseNodeData>;
export type CustomEdge = Edge;

export interface Workflow {
  id: string;
  name: string;
  nodes: CustomNode[];
  edges: CustomEdge[];
  createdAt: Date;
  updatedAt: Date;
}
