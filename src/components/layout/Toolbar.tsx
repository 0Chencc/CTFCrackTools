import { memo, useCallback, useMemo } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

const getStyles = (isDark: boolean) => {
  const t = isDark ? themes.dark : themes.light;
  return {
    container: {
      height: '44px',
      backgroundColor: t.bg,
      borderBottom: `1px solid ${t.border}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 16px',
      transition: 'background-color 0.15s ease, border-color 0.15s ease',
    },
    left: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
    },
    info: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontSize: '12px',
      color: t.textMuted,
      transition: 'color 0.15s ease',
    },
    badge: {
      fontSize: '10px',
      padding: '2px 8px',
      borderRadius: '12px',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      color: '#3b82f6',
    },
    right: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
    },
    button: {
      height: '32px',
      padding: '0 12px',
      fontSize: '12px',
      fontWeight: 500,
      borderRadius: '6px',
      backgroundColor: t.buttonBg,
      color: t.buttonText,
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      transition: 'background-color 0.15s ease, color 0.15s ease',
    },
    buttonDisabled: {
      height: '32px',
      padding: '0 12px',
      fontSize: '12px',
      fontWeight: 500,
      borderRadius: '6px',
      backgroundColor: t.buttonBg,
      color: t.buttonText,
      border: 'none',
      cursor: 'not-allowed',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      opacity: 0.4,
      transition: 'background-color 0.15s ease, color 0.15s ease',
    },
    runButton: {
      height: '32px',
      padding: '0 16px',
      fontSize: '12px',
      fontWeight: 500,
      borderRadius: '6px',
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
    },
    divider: {
      width: '1px',
      height: '24px',
      backgroundColor: t.border,
      transition: 'background-color 0.15s ease',
    },
  };
};

export const Toolbar = memo(() => {
  const { executeWorkflow, clear, saveWorkflow, loadWorkflow, isExecuting, nodes } = useWorkflowStore();
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const styles = useMemo(() => getStyles(isDark), [isDark]);

  const handleRun = useCallback(() => {
    executeWorkflow();
  }, [executeWorkflow]);

  const handleClear = useCallback(() => {
    clear();
  }, [clear]);

  const handleSave = useCallback(() => {
    saveWorkflow();
  }, [saveWorkflow]);

  const handleLoad = useCallback(() => {
    loadWorkflow();
  }, [loadWorkflow]);

  const btnStyle = (disabled: boolean) => disabled ? styles.buttonDisabled : styles.button;

  return (
    <div style={styles.container}>
      {/* 左侧 - 工作流信息 */}
      <div style={styles.left}>
        <div style={styles.info}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
          </svg>
          <span>Workflow Editor</span>
        </div>
        {nodes.length > 0 && (
          <span style={styles.badge}>
            {nodes.length} node{nodes.length > 1 ? "s" : ""}
          </span>
        )}
      </div>

      {/* 右侧 - 操作按钮 */}
      <div style={styles.right}>
        <button onClick={handleLoad} disabled={isExecuting} style={btnStyle(isExecuting)} title="Open">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 002-2v-4M17 8l-5-5-5 5M12 3v12" />
          </svg>
          <span>Open</span>
        </button>

        <button onClick={handleSave} disabled={isExecuting || nodes.length === 0} style={btnStyle(isExecuting || nodes.length === 0)} title="Save">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" />
            <path d="M17 21v-8H7v8M7 3v5h8" />
          </svg>
          <span>Save</span>
        </button>

        <div style={styles.divider} />

        <button
          onClick={handleRun}
          disabled={isExecuting || nodes.length === 0}
          style={isExecuting || nodes.length === 0 ? { ...styles.runButton, opacity: 0.4, cursor: 'not-allowed' } : styles.runButton}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z" />
          </svg>
          <span>{isExecuting ? "Running" : "Run"}</span>
        </button>

        <button onClick={handleClear} disabled={isExecuting || nodes.length === 0} style={btnStyle(isExecuting || nodes.length === 0)}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
          </svg>
          <span>Clear</span>
        </button>
      </div>
    </div>
  );
});

Toolbar.displayName = "Toolbar";
