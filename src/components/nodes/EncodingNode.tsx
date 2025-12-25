import { memo, useMemo } from "react";
import { Handle, Position, type NodeProps } from "reactflow";
import type { BaseNodeData } from "@/types/node";
import { useEncodingNode } from "@/hooks/useEncodingNode";
import { useThemeStore } from "@/stores/themeStore";
import { ALGORITHM_GROUPS } from "@/lib/algorithms";
import { themes } from "@/lib/theme";

export const EncodingNode = memo(
  ({ id, data, selected }: NodeProps<BaseNodeData>) => {
    const { copied, handleModeChange, handleAlgorithmChange, handleCopy, handleDelete } =
      useEncodingNode(id);
    const { theme } = useThemeStore();
    const isDark = theme === "dark";
    const t = isDark ? themes.dark : themes.light;

    const isSuccess = data.status === "success";
    const isError = data.status === "error";
    const isRunning = data.status === "running";

    const containerStyle = useMemo(() => ({
      position: 'relative' as const,
      width: '200px',
      borderRadius: '8px',
      overflow: 'hidden',
      backgroundColor: t.cardBg,
      boxShadow: selected
        ? `0 0 0 2px ${t.encodingColor}, 0 10px 15px -3px ${t.encodingColor}33`
        : `0 0 0 1px ${t.border}, 0 1px 3px rgba(0,0,0,0.1)`,
      transition: 'background-color 0.15s ease, box-shadow 0.15s ease',
    }), [t, selected]);

    const handleStyle = {
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: t.encodingColor,
      border: `2px solid ${t.cardBg}`,
    };

    return (
      <div style={containerStyle} className="group">
        <Handle
          type="target"
          position={Position.Left}
          style={{ ...handleStyle, left: '-4px' }}
        />

        <DeleteButton onClick={handleDelete} />

        <NodeHeader
          algorithm={data.algorithm}
          isRunning={isRunning}
          isSuccess={isSuccess}
          isError={isError}
          isDark={isDark}
        />

        <div style={{
          padding: '8px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          backgroundColor: t.cardBg,
          transition: 'background-color 0.15s ease',
        }}>
          <ModeToggle mode={data.mode} onChange={handleModeChange} isDark={isDark} />

          <AlgorithmSelect
            value={data.algorithm || "base64"}
            onChange={(e) => handleAlgorithmChange(e.target.value)}
            isDark={isDark}
          />

          <ResultDisplay
            result={data.result}
            error={data.error}
            isSuccess={isSuccess}
            isError={isError}
            copied={copied}
            onCopy={() => handleCopy(data.result)}
            isDark={isDark}
          />
        </div>

        <Handle
          type="source"
          position={Position.Right}
          style={{ ...handleStyle, right: '-4px' }}
        />
      </div>
    );
  }
);

EncodingNode.displayName = "EncodingNode";

// Sub-components
const DeleteButton = memo(({ onClick }: { onClick: (e: React.MouseEvent) => void }) => (
  <button
    onClick={onClick}
    className="node-delete-btn"
    style={{
      position: 'absolute',
      top: '6px',
      right: '6px',
      zIndex: 10,
      width: '20px',
      height: '20px',
      borderRadius: '4px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'rgba(239, 68, 68, 0.8)',
      color: 'white',
      border: 'none',
      cursor: 'pointer',
    }}
  >
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
      <path d="M18 6L6 18M6 6l12 12" />
    </svg>
  </button>
));

DeleteButton.displayName = "DeleteButton";

interface NodeHeaderProps {
  algorithm?: string;
  isRunning: boolean;
  isSuccess: boolean;
  isError: boolean;
  isDark: boolean;
}

const NodeHeader = memo(({ algorithm, isRunning, isSuccess, isError, isDark }: NodeHeaderProps) => {
  const t = isDark ? themes.dark : themes.light;
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '8px 10px',
      backgroundColor: `${t.encodingColor}15`,
      borderBottom: `1px solid ${t.border}50`,
    }}>
      <div style={{
        width: '20px',
        height: '20px',
        borderRadius: '4px',
        backgroundColor: `${t.encodingColor}30`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        {isRunning ? (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" style={{ color: t.encodingColor, animation: 'spin 1s linear infinite' }}>
            <circle style={{ opacity: 0.25 }} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
            <path style={{ opacity: 0.75 }} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={t.encodingColor} strokeWidth="2.5">
            <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
          </svg>
        )}
      </div>
      <span style={{ fontSize: '12px', fontWeight: 500, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: t.text }}>
        {algorithm?.toUpperCase() || "BASE64"}
      </span>
      {isSuccess && <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#22c55e' }} />}
      {isError && <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#ef4444' }} />}
    </div>
  );
});

NodeHeader.displayName = "NodeHeader";

interface ModeToggleProps {
  mode?: string;
  onChange: (mode: "encode" | "decode") => void;
  isDark: boolean;
}

const ModeToggle = memo(({ mode, onChange, isDark }: ModeToggleProps) => {
  const t = isDark ? themes.dark : themes.light;

  const buttonStyle = (active: boolean) => ({
    flex: 1,
    height: '24px',
    fontSize: '10px',
    fontWeight: 500,
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: active ? t.primary : 'transparent',
    color: active ? t.primaryText : t.textMuted,
  });

  return (
    <div style={{
      display: 'flex',
      padding: '2px',
      borderRadius: '6px',
      backgroundColor: t.bg,
    }}>
      <button
        onClick={() => onChange("encode")}
        className="nodrag"
        style={buttonStyle(mode === "encode")}
      >
        Encode
      </button>
      <button
        onClick={() => onChange("decode")}
        className="nodrag"
        style={buttonStyle(mode === "decode")}
      >
        Decode
      </button>
    </div>
  );
});

ModeToggle.displayName = "ModeToggle";

interface AlgorithmSelectProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  isDark: boolean;
}

const AlgorithmSelect = memo(({ value, onChange, isDark }: AlgorithmSelectProps) => {
  const t = isDark ? themes.dark : themes.light;
  return (
    <select
      value={value}
      onChange={onChange}
      className="nodrag"
      style={{
        width: '100%',
        height: '28px',
        padding: '0 8px',
        fontSize: '11px',
        borderRadius: '4px',
        border: `1px solid ${t.border}50`,
        backgroundColor: t.bg,
        color: t.text,
        cursor: 'pointer',
        outline: 'none',
      }}
    >
      {ALGORITHM_GROUPS.map((group) => (
        <optgroup key={group.name} label={group.name}>
          {group.algorithms.map((alg) => (
            <option key={alg.value} value={alg.value}>
              {alg.label}
            </option>
          ))}
        </optgroup>
      ))}
    </select>
  );
});

AlgorithmSelect.displayName = "AlgorithmSelect";

interface ResultDisplayProps {
  result?: string;
  error?: string;
  isSuccess: boolean;
  isError: boolean;
  copied: boolean;
  onCopy: () => void;
  isDark: boolean;
}

const ResultDisplay = memo(
  ({ result, error, isSuccess, isError, copied, onCopy, isDark }: ResultDisplayProps) => {
    const t = isDark ? themes.dark : themes.light;

    const containerBg = isSuccess
      ? (isDark ? 'rgba(34, 197, 94, 0.1)' : 'rgba(34, 197, 94, 0.08)')
      : isError
        ? (isDark ? 'rgba(239, 68, 68, 0.1)' : 'rgba(239, 68, 68, 0.08)')
        : t.bg;

    return (
      <div style={{
        borderRadius: '4px',
        overflow: 'hidden',
        backgroundColor: containerBg,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '4px 8px',
          borderBottom: `1px solid ${t.border}30`,
        }}>
          <span style={{ fontSize: '10px', color: t.textMuted }}>Output</span>
          {result && (
            <button
              onClick={onCopy}
              className="nodrag"
              style={{
                fontSize: '10px',
                padding: '2px 6px',
                borderRadius: '4px',
                border: 'none',
                backgroundColor: 'transparent',
                color: copied ? '#22c55e' : t.textMuted,
                cursor: 'pointer',
              }}
            >
              {copied ? "✓" : "Copy"}
            </button>
          )}
        </div>
        <div style={{ padding: '8px', minHeight: '36px', maxHeight: '60px', overflowY: 'auto' }}>
          {result ? (
            <pre style={{
              fontSize: '10px',
              fontFamily: 'monospace',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-all',
              lineHeight: 1.4,
              margin: 0,
              color: isSuccess ? '#4ade80' : t.text,
            }}>
              {result}
            </pre>
          ) : error ? (
            <p style={{ fontSize: '10px', color: '#f87171', margin: 0 }}>{error}</p>
          ) : (
            <p style={{ fontSize: '10px', color: `${t.textMuted}80`, fontStyle: 'italic', margin: 0 }}>No output</p>
          )}
        </div>
      </div>
    );
  }
);

ResultDisplay.displayName = "ResultDisplay";
