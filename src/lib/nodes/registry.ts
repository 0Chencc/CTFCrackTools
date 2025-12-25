import type { NodeTypes } from "reactflow";
import { InputNode } from "@/components/nodes/InputNode";
import { EncodingNode } from "@/components/nodes/EncodingNode";
import { OutputNode } from "@/components/nodes/OutputNode";

export const nodeTypes: NodeTypes = {
  input: InputNode,
  encoding: EncodingNode,
  output: OutputNode,
};

export interface NodeTemplate {
  type: string;
  label: string;
  category: string;
  defaultData: Record<string, unknown>;
}

export const nodeTemplates: NodeTemplate[] = [
  {
    type: "input",
    label: "Text Input",
    category: "input",
    defaultData: {
      label: "Input",
      category: "input",
      status: "idle",
      value: "",
    },
  },
  {
    type: "encoding",
    label: "Base64",
    category: "encoding",
    defaultData: {
      label: "Base64",
      category: "encoding",
      status: "idle",
      mode: "decode",
      algorithm: "base64",
    },
  },
  {
    type: "output",
    label: "Output",
    category: "output",
    defaultData: {
      label: "Output",
      category: "output",
      status: "idle",
      value: "",
    },
  },
];
