import { memo, useMemo } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

const QUICK_TOOLS = [
  { algorithm: "base64", label: "Base64", icon: "64" },
  { algorithm: "base32", label: "Base32", icon: "32" },
  { algorithm: "hex", label: "Hex", icon: "0x" },
  { algorithm: "url", label: "URL", icon: "%" },
];

interface ContextMenuProps {
  x: number;
  y: number;
  nodeId: string;
  onClose: () => void;
}

export const ContextMenu = memo(({ x, y, nodeId, onClose }: ContextMenuProps) => {
  const appendToNode = useWorkflowStore((s) => s.appendToNode);
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const t = isDark ? themes.dark : themes.light;

  const handleSelect = (algorithm: string, mode: "encode" | "decode") => {
    appendToNode(nodeId, algorithm, mode);
    onClose();
  };

  const menuStyle = useMemo(() => ({
    position: 'fixed' as const,
    zIndex: 50,
    backgroundColor: t.bg,
    borderRadius: '12px',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    padding: '8px',
    minWidth: '200px',
    border: `1px solid ${t.border}`,
    left: x,
    top: y,
  }), [t, x, y]);

  return (
    <>
      <div
        style={{ position: 'fixed', inset: 0, zIndex: 40 }}
        onClick={onClose}
      />
      <div style={menuStyle}>
        <MenuHeader isDark={isDark} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {QUICK_TOOLS.map((tool) => (
            <ToolMenuItem
              key={tool.algorithm}
              algorithm={tool.algorithm}
              label={tool.label}
              icon={tool.icon}
              onSelect={handleSelect}
              isDark={isDark}
            />
          ))}
        </div>
      </div>
    </>
  );
});

ContextMenu.displayName = "ContextMenu";

const MenuHeader = memo(({ isDark }: { isDark: boolean }) => {
  const t = isDark ? themes.dark : themes.light;
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '8px 12px',
      marginBottom: '4px',
    }}>
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke={t.primary}
        strokeWidth="2"
      >
        <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
        <polyline points="15 3 21 3 21 9" />
        <line x1="10" y1="14" x2="21" y2="3" />
      </svg>
      <span style={{ fontSize: '12px', fontWeight: 600, color: t.text }}>Quick Connect</span>
    </div>
  );
});

MenuHeader.displayName = "MenuHeader";

interface ToolMenuItemProps {
  algorithm: string;
  label: string;
  icon: string;
  onSelect: (algorithm: string, mode: "encode" | "decode") => void;
  isDark: boolean;
}

const ToolMenuItem = memo(({ algorithm, label, icon, onSelect, isDark }: ToolMenuItemProps) => {
  const t = isDark ? themes.dark : themes.light;

  const buttonBaseStyle = {
    flex: 1,
    height: '28px',
    fontSize: '11px',
    fontWeight: 500,
    borderRadius: '6px',
    border: 'none',
    backgroundColor: t.secondary,
    color: t.text,
    cursor: 'pointer',
    transition: 'background-color 0.15s, color 0.15s',
  };

  return (
    <div style={{ borderRadius: '8px', overflow: 'hidden' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '6px 12px',
        fontSize: '11px',
        fontWeight: 500,
        color: t.textMuted,
      }}>
        <div style={{
          width: '20px',
          height: '20px',
          borderRadius: '4px',
          backgroundColor: `${t.encodingColor}15`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <span style={{ fontSize: '8px', fontWeight: 700, color: t.encodingColor }}>{icon}</span>
        </div>
        {label}
      </div>
      <div style={{ display: 'flex', gap: '4px', padding: '0 8px 6px 8px' }}>
        <button
          onClick={() => onSelect(algorithm, "encode")}
          style={buttonBaseStyle}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = t.primary;
            e.currentTarget.style.color = t.primaryText;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = t.secondary;
            e.currentTarget.style.color = t.text;
          }}
        >
          Encode
        </button>
        <button
          onClick={() => onSelect(algorithm, "decode")}
          style={buttonBaseStyle}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = t.primary;
            e.currentTarget.style.color = t.primaryText;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = t.secondary;
            e.currentTarget.style.color = t.text;
          }}
        >
          Decode
        </button>
      </div>
    </div>
  );
});

ToolMenuItem.displayName = "ToolMenuItem";
