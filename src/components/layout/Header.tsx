import { memo, useCallback } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";

export const Header = memo(() => {
  const { executeWorkflow, clear, isExecuting, nodes } = useWorkflowStore();

  const handleRun = useCallback(() => {
    executeWorkflow();
  }, [executeWorkflow]);

  const handleClear = useCallback(() => {
    clear();
  }, [clear]);

  return (
    <header className="h-14 bg-[hsl(var(--card))] flex items-center justify-between px-5">
      {/* Logo 和标题 */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[hsl(var(--primary))] to-[hsl(168_80%_35%)] flex items-center justify-center text-[hsl(var(--primary-foreground))] font-bold text-base shadow-lg shadow-[hsl(var(--primary)/0.25)]">
            X
          </div>
          <div>
            <h1 className="text-sm font-semibold tracking-tight">CTFCrackTools</h1>
            <p className="text-[10px] text-[hsl(var(--muted-foreground))] -mt-0.5">Node-based Toolkit</p>
          </div>
        </div>
        <div className="h-6 w-px bg-[hsl(var(--border))]" />
        <span className="text-[10px] font-medium text-[hsl(var(--muted-foreground))] px-2 py-1 rounded-md bg-[hsl(var(--secondary))]">
          v0.1.0
        </span>
      </div>

      {/* 操作按钮 */}
      <div className="flex items-center gap-2">
        <button
          onClick={handleRun}
          disabled={isExecuting || nodes.length === 0}
          className="h-9 px-4 text-sm font-medium rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-[hsl(var(--primary)/0.25)]"
        >
          {isExecuting ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <span>Running</span>
            </>
          ) : (
            <>
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
              <span>Run</span>
            </>
          )}
        </button>
        <button
          onClick={handleClear}
          disabled={isExecuting || nodes.length === 0}
          className="h-9 px-4 text-sm font-medium rounded-lg bg-[hsl(var(--secondary))] text-[hsl(var(--secondary-foreground))] hover:bg-[hsl(var(--accent))] disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
          </svg>
          <span>Clear</span>
        </button>
      </div>
    </header>
  );
});

Header.displayName = "Header";
