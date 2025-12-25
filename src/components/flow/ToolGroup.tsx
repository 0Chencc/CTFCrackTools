import { memo } from "react";
import { isSingleOperation, getButtonLabel, type AlgorithmGroup } from "@/lib/algorithms";
import { themes } from "@/lib/theme";

interface ToolGroupProps {
  group: AlgorithmGroup;
  isExpanded: boolean;
  onToggle: () => void;
  onToolClick: (algorithm: string, mode: "encode" | "decode") => void;
  onDragStart: (
    event: React.DragEvent,
    nodeType: string,
    nodeData: Record<string, unknown>
  ) => void;
  isDark?: boolean;
}

export const ToolGroup = memo(
  ({ group, isExpanded, onToggle, onToolClick, onDragStart, isDark = true }: ToolGroupProps) => {
    const t = isDark ? themes.dark : themes.light;

    return (
      <div style={{
        borderBottom: `1px solid ${t.border}50`,
        transition: 'border-color 0.15s ease',
      }}>
        {/* Group Header */}
        <button
          onClick={onToggle}
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 12px',
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: t.text,
            transition: 'color 0.15s ease',
          }}
        >
          <svg
            style={{
              width: '12px',
              height: '12px',
              color: t.textMuted,
              transform: isExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
              transition: 'transform 0.15s ease, color 0.15s ease',
            }}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M9 18l6-6-6-6" />
          </svg>
          <span style={{ fontSize: '11px', fontWeight: 500 }}>{group.name}</span>
          <span style={{ marginLeft: 'auto', fontSize: '9px', color: t.textMuted }}>
            {group.algorithms.length}
          </span>
        </button>

        {/* Tools List */}
        {isExpanded && (
          <div style={{ padding: '0 8px 8px 8px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {group.algorithms.map((tool) => (
              <ToolItem
                key={tool.value}
                algorithm={tool.value}
                label={tool.label}
                icon={tool.icon}
                onToolClick={onToolClick}
                onDragStart={onDragStart}
                isDark={isDark}
              />
            ))}
          </div>
        )}
      </div>
    );
  }
);

ToolGroup.displayName = "ToolGroup";

// Tool Item Component
interface ToolItemProps {
  algorithm: string;
  label: string;
  icon: string;
  onToolClick: (algorithm: string, mode: "encode" | "decode") => void;
  onDragStart: (
    event: React.DragEvent,
    nodeType: string,
    nodeData: Record<string, unknown>
  ) => void;
  isDark?: boolean;
}

const ToolItem = memo(
  ({ algorithm, label, icon, onToolClick, onDragStart, isDark = true }: ToolItemProps) => {
    const t = isDark ? themes.dark : themes.light;
    const singleOp = isSingleOperation(algorithm);
    const buttonLabel = getButtonLabel(algorithm);

    const createDragData = (mode: "encode" | "decode") => ({
      label,
      category: "encoding",
      status: "idle",
      algorithm,
      mode,
    });

    const buttonStyle = {
      height: '20px',
      fontSize: '9px',
      fontWeight: 500,
      borderRadius: '4px',
      backgroundColor: t.cardBg,
      color: t.text,
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'background-color 0.15s ease, color 0.15s ease',
    };

    return (
      <div style={{
        borderRadius: '6px',
        backgroundColor: t.bg,
        padding: '6px',
        transition: 'background-color 0.15s ease',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px', padding: '0 2px' }}>
          <div style={{
            width: '16px',
            height: '16px',
            borderRadius: '4px',
            backgroundColor: `${t.encodingColor}25`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <span style={{ fontSize: '8px', fontWeight: 'bold', color: t.encodingColor }}>
              {icon}
            </span>
          </div>
          <span style={{ fontSize: '10px', fontWeight: 500, color: t.text }}>{label}</span>
        </div>

        <div style={{
          display: 'grid',
          gap: '4px',
          gridTemplateColumns: singleOp ? '1fr' : '1fr 1fr',
        }}>
          <button
            onClick={() => onToolClick(algorithm, "encode")}
            onDragStart={(e) => onDragStart(e, "encoding", createDragData("encode"))}
            draggable
            style={buttonStyle}
          >
            {buttonLabel}
          </button>
          {!singleOp && (
            <button
              onClick={() => onToolClick(algorithm, "decode")}
              onDragStart={(e) => onDragStart(e, "encoding", createDragData("decode"))}
              draggable
              style={buttonStyle}
            >
              Dec
            </button>
          )}
        </div>
      </div>
    );
  }
);

ToolItem.displayName = "ToolItem";
