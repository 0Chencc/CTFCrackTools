import { memo, useCallback, useRef, useEffect, useMemo } from "react";
import { Handle, Position, type NodeProps } from "reactflow";
import type { BaseNodeData } from "@/types/node";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

export const InputNode = memo(({ id, data, selected }: NodeProps<BaseNodeData>) => {
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const executeWorkflow = useWorkflowStore((state) => state.executeWorkflow);
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const t = isDark ? themes.dark : themes.light;
  const debounceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;
      updateNode(id, { value: newValue });

      // 防抖自动执行
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
      debounceTimer.current = setTimeout(() => {
        executeWorkflow();
      }, 300);
    },
    [id, updateNode, executeWorkflow]
  );

  // 清理定时器
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  const containerStyle = useMemo(() => ({
    position: 'relative' as const,
    width: '200px',
    borderRadius: '8px',
    overflow: 'hidden',
    backgroundColor: t.cardBg,
    boxShadow: selected
      ? `0 0 0 2px ${t.inputColor}, 0 10px 15px -3px ${t.inputColor}33`
      : `0 0 0 1px ${t.border}, 0 1px 3px rgba(0,0,0,0.1)`,
    transition: 'background-color 0.15s ease, box-shadow 0.15s ease',
  }), [t, selected]);

  const handleStyle = {
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    backgroundColor: t.inputColor,
    border: `2px solid ${t.cardBg}`,
  };

  return (
    <div style={containerStyle}>
      {/* 节点头部 */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '8px 10px',
        backgroundColor: `${t.inputColor}15`,
        borderBottom: `1px solid ${t.border}50`,
      }}>
        <div style={{
          width: '20px',
          height: '20px',
          borderRadius: '4px',
          backgroundColor: `${t.inputColor}30`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={t.inputColor} strokeWidth="2.5">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
        </div>
        <span style={{ fontSize: '12px', fontWeight: 500, color: t.text }}>Input</span>
        <span style={{ marginLeft: 'auto', fontSize: '10px', color: t.textMuted }}>
          {(data.value || "").length}
        </span>
      </div>

      {/* 节点内容 */}
      <div style={{
        padding: '8px',
        backgroundColor: t.cardBg,
        transition: 'background-color 0.15s ease',
      }}>
        <textarea
          value={data.value || ""}
          onChange={handleChange}
          placeholder="Enter text..."
          className="nodrag"
          style={{
            width: '100%',
            height: '64px',
            padding: '8px',
            fontSize: '12px',
            borderRadius: '4px',
            border: `1px solid ${t.border}50`,
            backgroundColor: t.bg,
            color: t.text,
            resize: 'none',
            outline: 'none',
            fontFamily: 'inherit',
          }}
        />
      </div>

      {/* 输出端口 */}
      <Handle
        type="source"
        position={Position.Right}
        style={{ ...handleStyle, right: '-4px' }}
      />
    </div>
  );
});

InputNode.displayName = "InputNode";
