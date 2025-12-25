import { useCallback, useRef, useState, useMemo } from "react";
import ReactFlow, { Background, Controls, MiniMap, BackgroundVariant, type ReactFlowInstance, type Node } from "reactflow";
import "reactflow/dist/style.css";
import { nodeTypes } from "@/lib/nodes/registry";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { NodePalette } from "./NodePalette";
import { ContextMenu } from "./ContextMenu";
import type { CustomNode } from "@/types/node";
import { themes } from "@/lib/theme";

let nodeId = 0;
const getNodeId = () => `node_${nodeId++}`;

interface ContextMenuState { x: number; y: number; nodeId: string; }

// 拖放处理 hook
function useDragDrop(addNode: (node: CustomNode) => void, reactFlowInstance: React.RefObject<ReactFlowInstance | null>) {
  const onDragStart = useCallback((event: React.DragEvent, nodeType: string, nodeData: Record<string, unknown>) => {
    event.dataTransfer.setData("application/reactflow-type", nodeType);
    event.dataTransfer.setData("application/reactflow-data", JSON.stringify(nodeData));
    event.dataTransfer.effectAllowed = "move";
  }, []);
  const onDragOver = useCallback((event: React.DragEvent) => { event.preventDefault(); event.dataTransfer.dropEffect = "move"; }, []);
  const onDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    const type = event.dataTransfer.getData("application/reactflow-type");
    const dataStr = event.dataTransfer.getData("application/reactflow-data");
    if (!type || !dataStr || !reactFlowInstance.current) return;
    const position = reactFlowInstance.current.screenToFlowPosition({ x: event.clientX, y: event.clientY });
    addNode({ id: getNodeId(), type, position, data: JSON.parse(dataStr) });
  }, [addNode, reactFlowInstance]);
  return { onDragStart, onDragOver, onDrop };
}

// 样式 hook
function useFlowStyles() {
  const { theme } = useThemeStore();
  const t = theme === "dark" ? themes.dark : themes.light;
  const containerStyle = useMemo(() => ({ display: "flex", height: "100%", width: "100%" }), []);
  const wrapperStyle = useMemo(() => ({ flex: 1, height: "100%", position: "relative" as const }), []);
  const controlsStyle = useMemo(() => ({ backgroundColor: t.cardBg, border: `1px solid ${t.border}`, borderRadius: "8px", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.1)" }), [t]);
  const miniMapStyle = useMemo(() => ({ backgroundColor: t.cardBg, border: `1px solid ${t.border}`, borderRadius: "8px" }), [t]);
  const miniMapNodeColor = useCallback((node: Node) => {
    const colors: Record<string, string> = { input: t.inputColor, encoding: t.encodingColor, output: t.outputColor };
    return colors[node.data?.category] || t.mutedColor;
  }, [t]);
  return { t, containerStyle, wrapperStyle, controlsStyle, miniMapStyle, miniMapNodeColor };
}

export function FlowCanvas() {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const reactFlowInstance = useRef<ReactFlowInstance | null>(null);
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, setSelectedNodeId } = useWorkflowStore();
  const { t, containerStyle, wrapperStyle, controlsStyle, miniMapStyle, miniMapNodeColor } = useFlowStyles();
  const { onDragStart, onDragOver, onDrop } = useDragDrop(addNode, reactFlowInstance);

  const closeContextMenu = useCallback(() => setContextMenu(null), []);
  useKeyboardShortcuts({ onEscape: closeContextMenu });
  const onInit = useCallback((instance: ReactFlowInstance) => { reactFlowInstance.current = instance; }, []);
  const onSelectionChange = useCallback(({ nodes: sel }: { nodes: Node[] }) => { setSelectedNodeId(sel.length === 1 ? sel[0].id : null); }, [setSelectedNodeId]);
  const onNodeContextMenu = useCallback((event: React.MouseEvent, node: Node) => { event.preventDefault(); setContextMenu({ x: event.clientX, y: event.clientY, nodeId: node.id }); }, []);
  const defaultEdgeOptions = useMemo(() => ({ animated: true, style: { strokeWidth: 2 } }), []);

  return (
    <div style={containerStyle}>
      <NodePalette onDragStart={onDragStart} />
      <div ref={reactFlowWrapper} style={wrapperStyle}>
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} onInit={onInit} onDrop={onDrop} onDragOver={onDragOver} onSelectionChange={onSelectionChange} onNodeContextMenu={onNodeContextMenu} onPaneClick={closeContextMenu} nodeTypes={nodeTypes} fitView snapToGrid snapGrid={[15, 15]} defaultEdgeOptions={defaultEdgeOptions}>
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} color={t.dotColor} />
          <Controls showZoom showFitView showInteractive style={controlsStyle} />
          <MiniMap nodeColor={miniMapNodeColor} maskColor={t.maskColor} style={miniMapStyle} />
        </ReactFlow>
        {contextMenu && <ContextMenu x={contextMenu.x} y={contextMenu.y} nodeId={contextMenu.nodeId} onClose={closeContextMenu} />}
      </div>
    </div>
  );
}
