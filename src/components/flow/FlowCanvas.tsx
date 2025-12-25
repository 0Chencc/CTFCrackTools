import { useCallback, useRef, useState, useMemo } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  BackgroundVariant,
  type ReactFlowInstance,
  type Node,
} from "reactflow";
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

interface ContextMenuState {
  x: number;
  y: number;
  nodeId: string;
}

export function FlowCanvas() {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const reactFlowInstance = useRef<ReactFlowInstance | null>(null);
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const t = isDark ? themes.dark : themes.light;

  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    setSelectedNodeId,
  } = useWorkflowStore();

  // Keyboard shortcuts
  const closeContextMenu = useCallback(() => setContextMenu(null), []);
  useKeyboardShortcuts({ onEscape: closeContextMenu });

  const onInit = useCallback((instance: ReactFlowInstance) => {
    reactFlowInstance.current = instance;
  }, []);

  const onSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: Node[] }) => {
      setSelectedNodeId(selectedNodes.length === 1 ? selectedNodes[0].id : null);
    },
    [setSelectedNodeId]
  );

  const onNodeContextMenu = useCallback((event: React.MouseEvent, node: Node) => {
    event.preventDefault();
    setContextMenu({ x: event.clientX, y: event.clientY, nodeId: node.id });
  }, []);

  const onDragStart = useCallback(
    (event: React.DragEvent, nodeType: string, nodeData: Record<string, unknown>) => {
      event.dataTransfer.setData("application/reactflow-type", nodeType);
      event.dataTransfer.setData("application/reactflow-data", JSON.stringify(nodeData));
      event.dataTransfer.effectAllowed = "move";
    },
    []
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const type = event.dataTransfer.getData("application/reactflow-type");
      const dataStr = event.dataTransfer.getData("application/reactflow-data");

      if (!type || !dataStr || !reactFlowInstance.current) return;

      const data = JSON.parse(dataStr);
      const position = reactFlowInstance.current.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: CustomNode = { id: getNodeId(), type, position, data };
      addNode(newNode);
    },
    [addNode]
  );

  const miniMapNodeColor = useCallback((node: Node) => {
    switch (node.data?.category) {
      case "input":
        return t.inputColor;
      case "encoding":
        return t.encodingColor;
      case "output":
        return t.outputColor;
      default:
        return t.mutedColor;
    }
  }, [t]);

  const defaultEdgeOptions = useMemo(
    () => ({ animated: true, style: { strokeWidth: 2 } }),
    []
  );

  const containerStyle = useMemo(() => ({
    display: 'flex',
    height: '100%',
    width: '100%',
  }), []);

  const wrapperStyle = useMemo(() => ({
    flex: 1,
    height: '100%',
    position: 'relative' as const,
  }), []);

  const controlsStyle = useMemo(() => ({
    backgroundColor: t.cardBg,
    border: `1px solid ${t.border}`,
    borderRadius: '8px',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  }), [t]);

  const miniMapStyle = useMemo(() => ({
    backgroundColor: t.cardBg,
    border: `1px solid ${t.border}`,
    borderRadius: '8px',
  }), [t]);

  return (
    <div style={containerStyle}>
      <NodePalette onDragStart={onDragStart} />

      <div ref={reactFlowWrapper} style={wrapperStyle}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onInit={onInit}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onSelectionChange={onSelectionChange}
          onNodeContextMenu={onNodeContextMenu}
          onPaneClick={closeContextMenu}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[15, 15]}
          defaultEdgeOptions={defaultEdgeOptions}
        >
          <Background
            variant={BackgroundVariant.Dots}
            gap={20}
            size={1}
            color={t.dotColor}
          />
          <Controls
            showZoom
            showFitView
            showInteractive
            style={controlsStyle}
          />
          <MiniMap
            nodeColor={miniMapNodeColor}
            maskColor={t.maskColor}
            style={miniMapStyle}
          />
        </ReactFlow>

        {contextMenu && (
          <ContextMenu
            x={contextMenu.x}
            y={contextMenu.y}
            nodeId={contextMenu.nodeId}
            onClose={closeContextMenu}
          />
        )}
      </div>
    </div>
  );
}
