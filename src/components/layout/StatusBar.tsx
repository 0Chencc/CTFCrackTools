import { memo, useMemo } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

const getStyles = (isDark: boolean) => {
  const t = isDark ? themes.dark : themes.light;
  return {
    container: {
      height: '28px',
      backgroundColor: t.bg,
      borderTop: `1px solid ${t.border}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 12px',
      fontSize: '10px',
      color: t.text,
      transition: 'background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease',
    },
    section: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
    },
    item: {
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
    },
    dot: {
      width: '6px',
      height: '6px',
      borderRadius: '50%',
    },
  };
};

export const StatusBar = memo(() => {
  const { nodes, edges, isExecuting } = useWorkflowStore();
  const { theme } = useThemeStore();
  const isDark = theme === "dark";
  const styles = useMemo(() => getStyles(isDark), [isDark]);

  return (
    <footer style={styles.container}>
      <div style={styles.section}>
        <div style={styles.item}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ opacity: 0.6 }}>
            <rect x="3" y="3" width="18" height="18" rx="2" />
          </svg>
          <span>{nodes.length} nodes</span>
        </div>
        <div style={styles.item}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ opacity: 0.6 }}>
            <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
            <polyline points="15 3 21 3 21 9" />
            <line x1="10" y1="14" x2="21" y2="3" />
          </svg>
          <span>{edges.length} connections</span>
        </div>
      </div>

      <div style={styles.section}>
        <div style={{ ...styles.item, opacity: 0.6 }}>
          {theme === "dark" ? (
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
          ) : (
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="5" />
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
            </svg>
          )}
          <span>{theme === "dark" ? "Dark" : "Light"}</span>
        </div>

        <div style={styles.item}>
          <div style={{ ...styles.dot, backgroundColor: isExecuting ? '#f59e0b' : '#10b981' }} />
          <span>{isExecuting ? "Processing..." : "Ready"}</span>
        </div>
      </div>
    </footer>
  );
});

StatusBar.displayName = "StatusBar";
