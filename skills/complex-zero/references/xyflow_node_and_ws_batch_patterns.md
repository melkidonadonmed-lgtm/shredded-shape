# `@xyflow/react` Custom Nodes, `150ms` WebSocket Batching & Next.js 15+ Async Params

Keep dense graphs responsive at 60fps while enforcing crisp 5-Plane `OKLCH` legibility, zero empty handles, `<= 2` node badges, coalesced `150ms` telemetry, and Next.js 15/16+ async safety.

## 1. `@xyflow/react` Custom Node Pattern (Memoized & Slop-Free)
- Wrap node components in `React.memo(...)` and hoist `nodeTypes` / `edgeTypes` outside render.
- Assign explicit `id` and `Position` to every `<Handle>`, add `nodrag nopan` to inner buttons/controls, keep interactive hit targets `>= 44x44px` (`48x48px` coarse), and use ONE verified SVG family (`24x24` Lucide `<svg>`):
```tsx
"use client";
import { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";

export interface ServiceNodeData {
  label: string;
  latencyMs: number;
  status: "idle" | "loading" | "error" | "success";
  onInspect: (id: string) => void;
}

export const ServiceGraphNode = memo(function ServiceGraphNode({ id, data }: NodeProps<ServiceNodeData>) {
  return (
    <article className="card-host card-matte" data-state={data.status}>
      <Handle id={`${id}-in`} type="target" position={Position.Left} />
      <header className="flex-row-safe">
        <span className="truncate-safe">{data.label}</span>
        <span className="engraved-pill">
          <span className="lum-bead" aria-hidden="true" />
          <span className="tabular-nums">{data.latencyMs}ms</span>
        </span>
      </header>
      <div className="card-body">
        <button type="button" className="nodrag nopan tactile-key" onClick={() => data.onInspect(id)}>
          Inspect Node
        </button>
      </div>
      <Handle id={`${id}-out`} type="source" position={Position.Right} />
    </article>
  );
});
```
- **Ban Hardcoded Node Badges:** Never emit `'[PASS]'` strings inside node markup or overload a single node card with `>= 3` `.metric-badge` pills.

## 2. `150ms` WebSocket / Chokidar Coalesced Micro-Batching
Never call `setNodes` synchronously on every socket message; coalesce queued frames at `150ms` intervals inside `useEffect` with clean `AbortController` teardown:
```typescript
import { useEffect, useRef } from "react";

export function useTelemetryBatch<T>(
  socketUrl: string,
  applyBatch: (events: T[]) => void,
  intervalMs = 150,
): void {
  const queueRef = useRef<T[]>([]);
  const applyRef = useRef(applyBatch);
  applyRef.current = applyBatch;

  useEffect(() => {
    const ctrl = new AbortController();
    const ws = new WebSocket(socketUrl);
    ws.addEventListener("message", (ev) => {
      try { queueRef.current.push(JSON.parse(String(ev.data)) as T); }
      catch { return; }
    }, { signal: ctrl.signal });
    const timer = window.setInterval(() => {
      if (queueRef.current.length === 0) return;
      applyRef.current(queueRef.current.splice(0, queueRef.current.length));
    }, intervalMs);
    return () => {
      window.clearInterval(timer);
      ctrl.abort();
      ws.close();
    };
  }, [socketUrl, intervalMs]);
}
```

## 3. Next.js 15/16+ Async `params` & Streamed HTML Sanitization
```tsx
import DOMPurify from "isomorphic-dompurify";
import { use } from "react";

export default async function TelemetryRoute({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <TelemetryDetail slug={slug} />;
}

export function SafeStreamPanel({ params, htmlLog }: { params: Promise<{ slug: string }>; htmlLog: string }) {
  const { slug } = use(params);
  const cleanHtml = DOMPurify.sanitize(htmlLog);
  return <section aria-label={slug} dangerouslySetInnerHTML={{ __html: cleanHtml }} />;
}
```
- Always inspect with `complex_zero_ast_auditor.py <target> --json` and enforce `content-visibility: auto` on large log inspector sidebars.
