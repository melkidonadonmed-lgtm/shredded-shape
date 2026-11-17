# Audit Criteria — `ui-quality-judge`

- **`[PASS]`**: `ui_judge_gatekeeper.py` returns `verdict: "PASSED"` with zero `CRITICAL` findings across all 5 batteries (OKLCH/WCAG 2.2 contrast `>= 4.5:1` AA or `>= 7.0:1` AAA, zero `#000000`, zero neon `C > 0.23`, `:focus-visible` intact, `DOM == Visual Order`, `48x48px` coarse touch, `prefers-reduced-motion`, zero UI emojis, zero Base64 `> 50KB`, anti-XSS clean, real FSM).
- **`[FAIL]`**: Any `CRITICAL` violation emits `verdict: "REJECTED"` with exact `file:line` evidence (`[OBSERVED FACT]`) triggering a `Self-Refine` cycle in `ui-clean-worker`.
- **`[UNVERIFIED]`**: `target_path` does not exist or contains no eligible frontend artifacts.
