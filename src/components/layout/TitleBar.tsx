import { memo, useCallback, useMemo } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { useThemeStore } from "@/stores/themeStore";
import { themes } from "@/lib/theme";

const getStyles = (isDark: boolean) => {
  const t = isDark ? themes.dark : themes.light;
  return {
    container: {
      height: '40px',
      backgroundColor: t.bg,
      borderBottom: `1px solid ${t.border}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      userSelect: 'none' as const,
      transition: 'background-color 0.15s ease, border-color 0.15s ease',
    },
    left: {
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      paddingLeft: '12px',
    },
    logo: {
      width: '24px',
      height: '24px',
      borderRadius: '6px',
      background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontSize: '10px',
      fontWeight: 'bold',
    },
    title: {
      fontSize: '12px',
      fontWeight: 600,
      color: t.text,
      transition: 'color 0.15s ease',
    },
    version: {
      fontSize: '10px',
      color: t.textMuted,
      padding: '2px 6px',
      borderRadius: '4px',
      backgroundColor: t.secondary,
      transition: 'background-color 0.15s ease, color 0.15s ease',
    },
    right: {
      display: 'flex',
      height: '100%',
      alignItems: 'center',
    },
    button: {
      width: '44px',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      border: 'none',
      background: 'transparent',
      cursor: 'pointer',
      color: t.textMuted,
    },
  };
};

export const TitleBar = memo(() => {
  const appWindow = getCurrentWindow();
  const { theme, toggleTheme } = useThemeStore();
  const isDark = theme === "dark";
  const styles = useMemo(() => getStyles(isDark), [isDark]);

  const handleMinimize = useCallback(() => {
    appWindow.minimize();
  }, [appWindow]);

  const handleMaximize = useCallback(() => {
    appWindow.toggleMaximize();
  }, [appWindow]);

  const handleClose = useCallback(() => {
    appWindow.close();
  }, [appWindow]);

  const handleDragStart = useCallback(() => {
    appWindow.startDragging();
  }, [appWindow]);

  return (
    <div style={styles.container} onMouseDown={handleDragStart}>
      {/* 左侧 - Logo 和标题 */}
      <div style={styles.left}>
        <div style={styles.logo}>X</div>
        <span style={styles.title}>CTFCrackTools</span>
        <span style={styles.version}>v0.1.0</span>
      </div>

      {/* 右侧 - 主题切换 + 窗口控制按钮 */}
      <div style={styles.right} onMouseDown={(e) => e.stopPropagation()}>
        {/* 主题切换 */}
        <button
          onClick={toggleTheme}
          style={styles.button}
          title={isDark ? "切换到亮色模式" : "切换到暗色模式"}
        >
          {isDark ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="2">
              <circle cx="12" cy="12" r="5" />
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" strokeWidth="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
          )}
        </button>

        {/* 最小化 */}
        <button onClick={handleMinimize} style={styles.button} title="最小化">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
          </svg>
        </button>

        {/* 最大化 */}
        <button onClick={handleMaximize} style={styles.button} title="最大化">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="4" y="4" width="16" height="16" rx="2" />
          </svg>
        </button>

        {/* 关闭 */}
        <button onClick={handleClose} style={styles.button} title="关闭">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
});

TitleBar.displayName = "TitleBar";
