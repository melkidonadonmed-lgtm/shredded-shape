# `@xyflow/react` Dagre Auto-Layout, Camera Sync & Windows Path Hygiene

Deterministic hierarchical layout (`TB` / `LR`), predictive log-to-node camera sync, and Windows-safe watcher normalization for `complex-zero` infinite canvases.

## 1. Pure Dagre Layout Helper (`src/lib/dagreLayout.ts`)
Install `@dagrejs/dagre` (or `dagre` + `@types/dagre`), read `node.measured?.width` / `height` when available, and convert Dagre's center anchor to React Flow's top-left corner:
```typescript
import dagre from "@dagrejs/dagre";
import { Position, type Edge, type Node } from "@xyflow/react";

const FALLBACK_W = 180;
const FALLBACK_H = 60;

export interface LayoutOptions {
  direction?: "TB" | "LR" | "BT" | "RL";
  nodeSep?: number;
  rankSep?: number;
}

export function getLayoutedElements(
  nodes: Node[],
  edges: Edge[],
  options: LayoutOptions = {},
): { nodes: Node[]; edges: Edge[] } {
  const { direction = "TB", nodeSep = 60, rankSep = 100 } = options;
  const g = new dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction, nodesep: nodeSep, ranksep: rankSep, align: "DL" });

  for (const n of nodes) {
    g.setNode(n.id, { width: n.measured?.width ?? FALLBACK_W, height: n.measured?.height ?? FALLBACK_H });
  }
  for (const e of edges) g.setEdge(e.source, e.target);
  dagre.layout(g);

  const isHorizontal = direction === "LR" || direction === "RL";
  const layouted = nodes.map((n) => {
    const pos = g.node(n.id);
    const w = n.measured?.width ?? FALLBACK_W;
    const h = n.measured?.height ?? FALLBACK_H;
    return {
      ...n,
      targetPosition: isHorizontal ? Position.Left : Position.Top,
      sourcePosition: isHorizontal ? Position.Right : Position.Bottom,
      position: { x: pos.x - w / 2, y: pos.y - h / 2 },
    };
  });
  return { nodes: layouted, edges };
}
```
- **Worker Offload (`> 300` Nodes):** Move `dagre.layout()` inside a Web Worker once graph size exceeds 300–500 nodes so panning/zooming stays locked at 60fps alongside `onlyRenderVisibleElements={true}`.

## 2. `<Panel>` Controls, `fitView()` & Predictive `setCenter()` Log Sync
```tsx
"use client";
import { useCallback } from "react";
import { Panel, useReactFlow } from "@xyflow/react";
import { getLayoutedElements } from "@/lib/dagreLayout";

export function useGraphCameraControls(nodes: Node[], edges: Edge[], setNodes: (n: Node[]) => void, setEdges: (e: Edge[]) => void) {
  const { fitView, setCenter } = useReactFlow();
  const applyLayout = useCallback((direction: "TB" | "LR") => {
    const next = getLayoutedElements(nodes, edges, { direction });
    setNodes([...next.nodes]);
    setEdges([...next.edges]);
    window.requestAnimationFrame(() => fitView({ duration: 600, padding: 0.2 }));
  }, [nodes, edges, setNodes, setEdges, fitView]);

  const focusNodeFromLog = useCallback((x: number, y: number) => {
    setCenter(x, y, { zoom: 1.2, duration: 800 });
  }, [setCenter]);

  return { applyLayout, focusNodeFromLog };
}
```
- **Fitts-Safe Layout Controls (`>= 44x44px` / `48x48px` Coarse):** Render `<Panel position="top-left">` buttons with `min-block-size: 44px` (`48px` coarse), `gap: 0.5rem`, `oklch()` matte surface, `:focus-visible`, and `touch-action: manipulation` (never `36px` cramped tool buttons).

## 3. Hoisted `nodeTypes`, Expanded Handles & Windows Path Hygiene
- **Hoist `nodeTypes` / `edgeTypes`:** Declare outside the React component (or wrap in `useMemo(..., [])`); inline `<ReactFlow nodeTypes={{ ... }} />` or unmemoized local objects trigger `XYFLOW_UNHOISTED_NODE_TYPES` and full DOM remounts.
- **Expanded `<Handle>` Hitbox:** Keep visual connectors at `8px` and expand interactive hit area via `.react-flow__handle::after { content: ""; position: absolute; inset: -8px; }` (`24x24px`+) so drag-to-connect works cleanly without overlapping adjacent buttons.
- **Windows `\` -> `/` Normalization:** In `chokidar`/Node watchers, always normalize `path.relative(root, file).replace(/\\/g, "/")` before emitting WebSocket node flash events so Windows backslashes never silently miss browser node IDs (`WINDOWS_PATH_SEPARATOR_UNNORMALIZED`).
