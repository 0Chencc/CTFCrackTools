import { useEffect, useMemo } from "react";
import { useThemeStore } from "@/stores/themeStore";
import { TitleBar } from "@/components/layout/TitleBar";
import { Toolbar } from "@/components/layout/Toolbar";
import { StatusBar } from "@/components/layout/StatusBar";
import { FlowCanvas } from "@/components/flow/FlowCanvas";

function App() {
  const { theme } = useThemeStore();
  const isDark = theme === "dark";

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
  }, [isDark]);

  const containerStyle = useMemo(() => ({
    display: 'flex',
    flexDirection: 'column' as const,
    height: '100vh',
    width: '100vw',
    backgroundColor: isDark ? '#0f172a' : '#f8fafc',
    color: isDark ? 'white' : '#1e293b',
    overflow: 'hidden',
    transition: 'background-color 0.15s ease, color 0.15s ease',
  }), [isDark]);

  // 完整布局
  return (
    <div style={containerStyle}>
      <TitleBar />
      <Toolbar />
      <main style={{ flex: 1, overflow: 'hidden' }}>
        <FlowCanvas />
      </main>
      <StatusBar />
    </div>
  );
}

export default App;
