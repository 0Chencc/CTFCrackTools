import { memo, useCallback, useState, useMemo } from "react";
import { Handle, Position, type NodeProps } from "reactflow";
import type { BaseNodeData } from "@/types/node";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

// 节点样式生成
function getContainerStyle(t: typeof themes.dark, selected: boolean) {
  return {
    position: "relative" as const,
    width: "200px",
    borderRadius: "8px",
    overflow: "hidden",
    backgroundColor: t.cardBg,
    boxShadow: selected
      ? `0 0 0 2px ${t.outputColor}, 0 10px 15px -3px ${t.outputColor}33`
      : `0 0 0 1px ${t.border}, 0 1px 3px rgba(0,0,0,0.1)`,
    transition: "background-color 0.15s ease, box-shadow 0.15s ease",
  };
}

function getHandleStyle(t: typeof themes.dark) {
  return {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    backgroundColor: t.outputColor,
    border: `2px solid ${t.cardBg}`,
  };
}

// 删除按钮组件
const DeleteButton = memo(({ onClick }: { onClick: (e: React.MouseEvent) => void }) => (
  <button onClick={onClick} className="node-delete-btn" style={{
    position: "absolute", top: "6px", right: "6px", zIndex: 10, width: "20px", height: "20px",
    borderRadius: "4px", display: "flex", alignItems: "center", justifyContent: "center",
    backgroundColor: "rgba(239, 68, 68, 0.8)", color: "white", border: "none", cursor: "pointer",
  }}>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
      <path d="M18 6L6 18M6 6l12 12" />
    </svg>
  </button>
));
DeleteButton.displayName = "DeleteButton";

// 节点头部组件
const NodeHeader = memo(({ t, isSuccess }: { t: typeof themes.dark; isSuccess: boolean }) => (
  <div style={{ display: "flex", alignItems: "center", gap: "8px", padding: "8px 10px", backgroundColor: `${t.outputColor}15`, borderBottom: `1px solid ${t.border}50` }}>
    <div style={{ width: "20px", height: "20px", borderRadius: "4px", backgroundColor: `${t.outputColor}30`, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={t.outputColor} strokeWidth="2.5">
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
        <polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><polyline points="10 9 9 9 8 9" />
      </svg>
    </div>
    <span style={{ fontSize: "12px", fontWeight: 500, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", color: t.text }}>OUTPUT</span>
    {isSuccess && <div style={{ width: "6px", height: "6px", borderRadius: "50%", backgroundColor: "#22c55e" }} />}
  </div>
));
NodeHeader.displayName = "NodeHeader";

// 内容区域组件
const ContentArea = memo(({ t, isDark, isSuccess, value, copied, onCopy }: {
  t: typeof themes.dark; isDark: boolean; isSuccess: boolean; value: string; copied: boolean; onCopy: () => void;
}) => (
  <div style={{ padding: "8px" }}>
    <div style={{ borderRadius: "4px", overflow: "hidden", backgroundColor: isSuccess ? (isDark ? "rgba(34, 197, 94, 0.1)" : "rgba(34, 197, 94, 0.08)") : t.bg }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "4px 8px", borderBottom: `1px solid ${t.border}30` }}>
        <span style={{ fontSize: "10px", color: t.textMuted }}>{value.length} chars</span>
        {value && (
          <button onClick={onCopy} className="nodrag" style={{ fontSize: "10px", padding: "2px 6px", borderRadius: "4px", border: "none", backgroundColor: "transparent", color: copied ? "#22c55e" : t.textMuted, cursor: "pointer" }}>
            {copied ? "✓ Copied" : "Copy"}
          </button>
        )}
      </div>
      <div style={{ padding: "8px", minHeight: "60px", maxHeight: "100px", overflowY: "auto" }}>
        {value ? (
          <pre style={{ fontSize: "10px", fontFamily: "monospace", whiteSpace: "pre-wrap", wordBreak: "break-all", lineHeight: 1.4, margin: 0, color: isSuccess ? "#4ade80" : t.text }}>{value}</pre>
        ) : (
          <p style={{ fontSize: "10px", color: `${t.textMuted}80`, fontStyle: "italic", margin: 0 }}>Waiting for input...</p>
        )}
      </div>
    </div>
  </div>
));
ContentArea.displayName = "ContentArea";

export const OutputNode = memo(({ id, data, selected }: NodeProps<BaseNodeData>) => {
  const deleteNode = useWorkflowStore((s) => s.deleteNode);
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const t = isDark ? themes.dark : themes.light;
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(() => {
    if (data.value) { navigator.clipboard.writeText(data.value); setCopied(true); setTimeout(() => setCopied(false), 1500); }
  }, [data.value]);

  const handleDelete = useCallback((e: React.MouseEvent) => { e.stopPropagation(); deleteNode(id); }, [id, deleteNode]);

  const containerStyle = useMemo(() => getContainerStyle(t, selected), [t, selected]);
  const handleStyle = useMemo(() => getHandleStyle(t), [t]);

  return (
    <div style={containerStyle} className="group">
      <Handle type="target" position={Position.Left} style={{ ...handleStyle, left: "-4px" }} />
      <DeleteButton onClick={handleDelete} />
      <NodeHeader t={t} isSuccess={data.status === "success"} />
      <ContentArea t={t} isDark={isDark} isSuccess={data.status === "success"} value={data.value || ""} copied={copied} onCopy={handleCopy} />
    </div>
  );
});

OutputNode.displayName = "OutputNode";
