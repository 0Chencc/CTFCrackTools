import { useCallback, useState } from "react";
import { useWorkflowStore } from "@/stores/workflowStore";

/**
 * Hook for encoding node operations
 */
export function useEncodingNode(nodeId: string) {
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const deleteNode = useWorkflowStore((state) => state.deleteNode);
  const executeWorkflow = useWorkflowStore((state) => state.executeWorkflow);
  const [copied, setCopied] = useState(false);

  const handleModeChange = useCallback(
    (mode: "encode" | "decode") => {
      updateNode(nodeId, { mode });
      setTimeout(() => executeWorkflow(), 50);
    },
    [nodeId, updateNode, executeWorkflow]
  );

  const handleAlgorithmChange = useCallback(
    (algorithm: string) => {
      updateNode(nodeId, { algorithm });
      setTimeout(() => executeWorkflow(), 50);
    },
    [nodeId, updateNode, executeWorkflow]
  );

  const handleCopy = useCallback((result: string | undefined) => {
    if (result) {
      navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  }, []);

  const handleDelete = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      deleteNode(nodeId);
    },
    [nodeId, deleteNode]
  );

  return {
    copied,
    handleModeChange,
    handleAlgorithmChange,
    handleCopy,
    handleDelete,
  };
}
