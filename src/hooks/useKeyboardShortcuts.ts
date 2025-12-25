import { useEffect, useCallback } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";

interface UseKeyboardShortcutsOptions {
  onEscape?: () => void;
}

/**
 * Hook for handling keyboard shortcuts in the workflow editor
 */
export function useKeyboardShortcuts(options: UseKeyboardShortcutsOptions = {}) {
  const {
    nodes,
    selectedNodeId,
    deleteNode,
    executeWorkflow,
    saveWorkflow,
    loadWorkflow,
    setSelectedNodeId,
  } = useWorkflowStore();

  const handleGlobalShortcuts = useCallback(
    (e: KeyboardEvent): boolean => {
      if (e.ctrlKey && e.key === "s") {
        e.preventDefault();
        saveWorkflow();
        return true;
      }
      if (e.ctrlKey && e.key === "o") {
        e.preventDefault();
        loadWorkflow();
        return true;
      }
      if ((e.ctrlKey && e.key === "Enter") || e.key === "F5") {
        e.preventDefault();
        executeWorkflow();
        return true;
      }
      return false;
    },
    [saveWorkflow, loadWorkflow, executeWorkflow]
  );

  const handleEditorShortcuts = useCallback(
    (e: KeyboardEvent): boolean => {
      if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
        // 不允许删除 Input 节点
        const selectedNode = nodes.find((n) => n.id === selectedNodeId);
        if (selectedNode?.type === "input") {
          return false;
        }
        e.preventDefault();
        deleteNode(selectedNodeId);
        return true;
      }
      if (e.key === "Escape") {
        e.preventDefault();
        setSelectedNodeId(null);
        options.onEscape?.();
        return true;
      }
      return false;
    },
    [nodes, selectedNodeId, deleteNode, setSelectedNodeId, options]
  );

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Global shortcuts work everywhere
      if (handleGlobalShortcuts(e)) return;

      // Editor shortcuts only work outside input fields
      const target = e.target as HTMLElement;
      const isInputFocused =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      if (!isInputFocused) {
        handleEditorShortcuts(e);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleGlobalShortcuts, handleEditorShortcuts]);
}
