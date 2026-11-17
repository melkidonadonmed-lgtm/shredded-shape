# WCAG 2.2 & Perceptual OKLCH Actor-Critic Rubric (`FNR < 0.001`)

## 1. Perceptual CIE 1931 $Y$ / OKLCH Contrast Math (`SUPERVISOR FRONT END`)

Convert OKLCH lightness $L \in [0, 1]$ to relative luminance $Y$ and compute contrast ratio $CR$:

$$Y(L) = \begin{cases} \frac{L}{0.08} \cdot 0.01 & L \le 0.08 \\ \left(\frac{L + 0.16}{1.16}\right)^3 & L > 0.08 \end{cases}, \qquad CR = \frac{\max(Y_1, Y_2) + 0.05}{\min(Y_1, Y_2) + 0.05}$$

- **Normal Text:** `>= 4.5:1` (`AA`) or `>= 7.0:1` (`AAA`).
- **Large Text / UI Controls / Focus Rings:** `>= 3.0:1`.
- **Target False Negative Rate:** $FNR = \frac{FN}{FN + TP} < 0.001$ (inaccessible contrast must never pass).

## 2. The 5 Deterministic Inspection Batteries

1. **OKLCH Polarity & Anti-Neon:** Zero `#000000` (`oklch(0 0 0)`), Dark Mode `L_card > L_canvas`, no surface chroma `C > 0.23`.
2. **Touch Ergonomics (Fitts' Law):** `@media (any-pointer: coarse)` or explicit `min-block-size >= 48px` on interactive controls (`gap >= 8px`).
3. **Keyboard Focus Integrity:** Ban `outline: none` / `outline: 0` unless paired with visible `:focus-visible`.
4. **DOM == Visual Order:** Ban `flex-direction: row-reverse` and CSS `order:` properties that break Tab traversal.
5. **Motion, Visual Hygiene & Security:** `@media (prefers-reduced-motion: reduce)`, zero UI emojis, zero Base64 images `> 50 KB`, zero unguarded `dangerouslySetInnerHTML` / `eval()`, and authentic FSM state handling.

## 3. Closed-Loop Self-Refine Handoff (`REJECTED -> ui-clean-worker`)

When `verdict == "REJECTED"`, return ONLY the `findings` array (`rule_id`, `severity`, `epistemic_type`, `file:line`, `message`, `remediation`) back to `ui-clean-worker` for surgical repair, never rewriting code directly from `ui-judge`.
