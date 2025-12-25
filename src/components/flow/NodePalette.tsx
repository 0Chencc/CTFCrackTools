import { memo, useCallback, useState, useMemo } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { ALGORITHM_GROUPS } from "@/lib/algorithms";
import { ToolGroup } from "./ToolGroup";
import { themes } from "@/lib/theme";

interface NodePaletteProps {
  onDragStart: (
    event: React.DragEvent,
    nodeType: string,
    nodeData: Record<string, unknown>
  ) => void;
}

export const NodePalette = memo(({ onDragStart }: NodePaletteProps) => {
  const { nodes, selectedNodeId, createQuickWorkflow, appendToNode, appendOutputNode } =
    useWorkflowStore();
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const t = isDark ? themes.dark : themes.light;

  const [expandedGroups, setExpandedGroups] = useState<Record<string, boolean>>({
    Encoding: true,
    Cipher: false,
    Crypto: false,
    Hash: false,
    Text: false,
  });

  const toggleGroup = useCallback((groupName: string) => {
    setExpandedGroups((prev) => ({
      ...prev,
      [groupName]: !prev[groupName],
    }));
  }, []);

  const handleToolClick = useCallback(
    (algorithm: string, mode: "encode" | "decode") => {
      if (nodes.length === 0) {
        createQuickWorkflow(algorithm, mode);
        return;
      }
      if (selectedNodeId) {
        appendToNode(selectedNodeId, algorithm, mode);
        return;
      }
      const lastNode = nodes[nodes.length - 1];
      if (lastNode) {
        appendToNode(lastNode.id, algorithm, mode);
      }
    },
    [nodes, selectedNodeId, createQuickWorkflow, appendToNode]
  );

  const handleAddOutput = useCallback(() => {
    if (nodes.length === 0) return;
    const targetId = selectedNodeId || nodes[nodes.length - 1]?.id;
    if (targetId) {
      appendOutputNode(targetId);
    }
  }, [nodes, selectedNodeId, appendOutputNode]);

  const containerStyle = useMemo(() => ({
    width: '208px',
    height: '100%',
    backgroundColor: t.bg,
    display: 'flex',
    flexDirection: 'column' as const,
    borderRight: `1px solid ${t.border}`,
    transition: 'background-color 0.15s ease, border-color 0.15s ease',
  }), [t]);

  return (
    <div style={containerStyle}>
      {/* Header */}
      <PaletteHeader nodeCount={nodes.length} hasSelection={!!selectedNodeId} isDark={isDark} />

      {/* Tool Groups */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {ALGORITHM_GROUPS.map((group) => (
          <ToolGroup
            key={group.name}
            group={group}
            isExpanded={expandedGroups[group.name] ?? false}
            onToggle={() => toggleGroup(group.name)}
            onToolClick={handleToolClick}
            onDragStart={onDragStart}
            isDark={isDark}
          />
        ))}
      </div>

      {/* Output Node Button */}
      <OutputButton disabled={nodes.length === 0} onClick={handleAddOutput} isDark={isDark} />

      {/* Keyboard Hints */}
      <KeyboardHints isDark={isDark} />
    </div>
  );
});

NodePalette.displayName = "NodePalette";

// Sub-components
const PaletteHeader = memo(
  ({ nodeCount, hasSelection, isDark }: { nodeCount: number; hasSelection: boolean; isDark: boolean }) => {
    const t = isDark ? themes.dark : themes.light;
    return (
      <div style={{
        padding: '10px 12px',
        borderBottom: `1px solid ${t.border}`,
        transition: 'border-color 0.15s ease',
      }}>
        <h2 style={{
          fontSize: '10px',
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: t.textMuted,
          transition: 'color 0.15s ease',
        }}>
          Tools
        </h2>
        <p style={{
          fontSize: '10px',
          color: t.textMuted,
          opacity: 0.6,
          marginTop: '2px',
          transition: 'color 0.15s ease',
        }}>
          {nodeCount === 0
            ? "Click to start"
            : hasSelection
              ? "Append after selected"
              : "Append to chain"}
        </p>
      </div>
    );
  }
);

PaletteHeader.displayName = "PaletteHeader";

const OutputButton = memo(
  ({ disabled, onClick, isDark }: { disabled: boolean; onClick: () => void; isDark: boolean }) => {
    const t = isDark ? themes.dark : themes.light;
    return (
      <div style={{
        padding: '8px',
        borderTop: `1px solid ${t.border}`,
        transition: 'border-color 0.15s ease',
      }}>
        <button
          onClick={onClick}
          disabled={disabled}
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 12px',
            borderRadius: '8px',
            backgroundColor: `${t.outputColor}15`,
            border: 'none',
            cursor: disabled ? 'not-allowed' : 'pointer',
            opacity: disabled ? 0.4 : 1,
            transition: 'background-color 0.15s ease',
          }}
        >
          <div style={{
            width: '20px',
            height: '20px',
            borderRadius: '4px',
            backgroundColor: `${t.outputColor}30`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              stroke={t.outputColor}
              strokeWidth="2.5"
            >
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
          </div>
          <span style={{ fontSize: '11px', fontWeight: 500, color: t.outputColor }}>
            Add Output
          </span>
        </button>
      </div>
    );
  }
);

OutputButton.displayName = "OutputButton";

const KeyboardHints = memo(({ isDark }: { isDark: boolean }) => {
  const t = isDark ? themes.dark : themes.light;
  const kbdStyle = {
    padding: '2px 4px',
    borderRadius: '3px',
    backgroundColor: isDark ? '#334155' : '#e2e8f0',
    fontSize: '8px',
    transition: 'background-color 0.15s ease',
  };
  return (
    <div style={{
      padding: '6px 8px',
      borderTop: `1px solid ${t.border}`,
      backgroundColor: isDark ? 'rgba(15,23,42,0.5)' : 'rgba(248,250,252,0.5)',
      transition: 'background-color 0.15s ease, border-color 0.15s ease',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '9px', color: t.textMuted, marginBottom: '4px' }}>
        <kbd style={kbdStyle}>Ctrl+S</kbd>
        <span>Save</span>
        <kbd style={{ ...kbdStyle, marginLeft: '8px' }}>Ctrl+O</kbd>
        <span>Open</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '9px', color: t.textMuted }}>
        <kbd style={kbdStyle}>Del</kbd>
        <span>Delete</span>
        <kbd style={{ ...kbdStyle, marginLeft: '8px' }}>F5</kbd>
        <span>Run</span>
      </div>
    </div>
  );
});

KeyboardHints.displayName = "KeyboardHints";
