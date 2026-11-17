# AGENTS.md — Operational Kernel and Governance (v2.1)

## 0. PROJECT CONTEXT (Auto-detected)
- **Project:** `shredded-shape`
- **Temporal Baseline & Models:** Use the session's temporal context and verify official docs/MCP before assuming APIs or SDKs; never hardcode or downgrade models in static rules (respect the host/project model configuration).
- **Active Stack:** Python 3.12+ (uv / pyproject.toml)
- **State Architecture:**
  - `.agents/AGENTS.md`: Local behavioral rules (loaded at boot).
  - `.context/context.md`: Authoritative project state and handoff ledger (read/write on demand).
  - `.context/spec.md`: Technical implementation contract and scope lock for the active feature (when applicable).

## 1. NON-NEGOTIABLE GOLDEN RULES
1. **State Synchronization (Read-Before-Write):** On persistent mutations, inspect `.context/context.md` and `.context/spec.md` (if present) before editing code; propose creating `spec.md` before complex features.
2. **YAGNI & Scope Lock:** Solve strictly what was requested by the simplest path. Do not invent premature abstractions or out-of-spec features.
3. **Physical Verification & Update (Read-After-Write):** Read files before editing. After modifying code or config, verify physically in the terminal (linter, build, or real tests) and **update `.context/context.md`** with the change and next step before closing.
4. **Context Economy (Anti-Bloat):** Never dump large files, full directory trees, or raw logs into chat. Use targeted searches (`rg`/`grep`), concise summaries, or subagents (`/boost`, `/teamwork`) to keep the main context window clean.
5. **Code Quality & Defensive Design:** Short functions (`<= 60` lines, max 3 nesting levels via *Early Return*, cyclomatic complexity `M <= 10`) inside cohesive modules (`<= 600` lines), strict typing on internal contracts and MCP inputs (`extra="forbid"`, `z.strictObject()`, Go structs / `DisallowUnknownFields()` for closed schemas), and never swallow errors silently (`pass`, `...`, bare `except:`, empty `catch {}`; explicit typed suppression like `contextlib.suppress(...)` is allowed).
6. **Zero-Trust & Sanitization:** Treat external data as untrusted. Never expose keys, `.env`, or secrets in code, logs, or tool arguments. In the **Managed Antigravity Agent** (Interactions API), `generation_config` rejects (`400`) `temperature`, `top_p`, `top_k`, `stop_sequences`, and `max_output_tokens`; in standard `generateContent` / `interactions.create` calls (e.g., `gemini-4-argon`), `max_output_tokens` is supported and recommended. MCP server names must match `^[a-z0-9_-]+$`.
7. **Risk-Oriented Execution & Autonomous Compensation (HITL):** Always deliver the best outcome for the request; on low-risk, reversible, or read-only failures, **compensate autonomously** by switching strategy, parameters, or tools. Reserve mandatory HITL pauses exclusively for destructive actions (bulk file deletion, `.env`/production changes) or critical ambiguity.
8. **Language Separation & Bilingual Bridge (CRITICAL):** Keep all internal artifacts (`AGENTS.md`, `SKILL.md`, `rules/*.md`, `agents/*.md`, `.context/{context,spec}.md`, schemas, comments) in Technical English, and formulate all direct user dialogue, plans, status reports, and deliverables in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.

## 2. EVOLUTIONARY MEMORY (Project-Learned Rules)
<!-- Max 5 concise rules born from real errors. Once 5 are reached, refactor into .agents/skills/<name>/SKILL.md -->
- [Empty at init — awaiting practical learnings]

---

## 3. DELIVERY CLOSING BLOCK (Triad v2.0 / Persistent Mutations)
On persistent file/code mutations, conclude the user-facing response in **Portuguese (`pt-BR`)** using this concise block (omit for read-only inspections or simple Q&A):

### 📊 Resumo & Análise (Self-Refine)
- **Feito e Validado (RAW):** [Arquivos alterados + resultado real do teste/linter no terminal]
- **Estado do `context.md`:** [Confirmar atualização ou "N/A — leitura pura"]
- **Ponto de Atrito:** [O que exigiu retentativa/compensação na execução ou "Execução limpa em 1ª passagem"]

### 💡 Próximo Passo & Evolução
- **Dica para a Próxima Tarefa:** [1 sugestão prática, técnica ou de comando para o próximo passo do backlog]
- **Evolução de Regra (Se aplicável):** [Se houve erro evitável hoje, sugira 1 linha para "Memória Evolutiva" ou criação de Skill]