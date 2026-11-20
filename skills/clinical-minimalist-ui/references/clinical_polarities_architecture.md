# Clinical Polarities, Sticky Safety Header & Deterministic Calculators

Clinical interfaces serve clinicians across bright ward fluorescence (`clinical-day`) and dark ICU shifts (`clinical-night`). Every control preserves `>= 7.0:1` WCAG AAA contrast and bounded medical math.

## 1. Dual Clinical Polarity Calibration (`WCAG AAA >= 7.0:1`)
| Token | `clinical-day` | `clinical-night` (`!= #000000`) | Clinical Rationale |
| :--- | :--- | :--- | :--- |
| `--bg-well` | `oklch(0.945 0.006 245)` | `oklch(0.120 0.012 250)` | Recessed input & lab badge wells without border clutter. |
| `--bg-canvas` | `oklch(0.985 0.005 245)` | `oklch(0.155 0.014 250)` | Paper-grade matte surface free of OLED black smearing. |
| `--bg-card` | `oklch(1.000 0.000 0)` | `oklch(0.205 0.017 250)` | Anodized order/prescription containers (`L_card > L_canvas`). |
| `--bg-card-lit` | `oklch(1.000 0.000 0)` | `oklch(0.245 0.020 250)` | Focused order cards & active clinical warnings. |
| `--ink-primary` | `oklch(0.170 0.020 255)` | `oklch(0.960 0.005 245)` | Guarantees `> 12:1` primary legibility for doses and IDs. |
| `--ink-muted` | `oklch(0.375 0.018 255)` | `oklch(0.750 0.014 250)` | Guarantees `>= 7.0:1` timestamps, ICD codes, and units. |
| `--status-danger` | `oklch(0.500 0.210 25)` | `oklch(0.700 0.195 25)` | Semantic clinical alert (`15°..40°`, `C <= 0.24`), zero magenta/cyan neon. |

## 2. 3-Click Patient Safety Banner & Sticky Header
- Anchor a compact sticky `<header>` displaying Patient Full Name, DOB, Allergies (`role="status"`), and Primary Identifier (`tabular-nums`) within zero scrolling hops.
- Every primary workflow (`Vitals -> Prescription -> Print A4`) must complete in `<= 3` clicks without hidden drawer traps or `outline: none`.

## 3. Deterministic Medical Calculator Pattern (Bounded FSM + `aria-live`)
Isolate physiological dose equations as pure functions (`<= 60` lines) with explicit physiological bounds rejecting impossible inputs before rendering results:
```tsx
"use client";
import { useState } from "react";

type CalcState =
  | { status: "idle" }
  | { status: "error"; message: string }
  | { status: "success"; crClMlMin: number };

export function computeCockcroftGault(age: number, weightKg: number, scrMgDl: number, female: boolean): CalcState {
  if (!Number.isFinite(age) || age < 18 || age > 120) return { status: "error", message: "Age out of range (18-120 yr)." };
  if (!Number.isFinite(weightKg) || weightKg < 25 || weightKg > 300) return { status: "error", message: "Weight out of range (25-300 kg)." };
  if (!Number.isFinite(scrMgDl) || scrMgDl < 0.2 || scrMgDl > 20) return { status: "error", message: "Serum Cr out of range (0.2-20 mg/dL)." };
  const raw = ((140 - age) * weightKg) / (72 * scrMgDl);
  const adjusted = Number((female ? raw * 0.85 : raw).toFixed(1));
  return { status: "success", crClMlMin: adjusted };
}

export function RenalClearanceWidget() {
  const [state, setState] = useState<CalcState>({ status: "idle" });
  const handleCalculate = (fd: FormData) => {
    const next = computeCockcroftGault(
      Number(fd.get("age")), Number(fd.get("weight")), Number(fd.get("scr")), fd.get("sex") === "F",
    );
    setState(next);
  };
  return (
    <section aria-labelledby="crcl-title" className="surface-card">
      <h2 id="crcl-title">Creatinine Clearance (Cockcroft-Gault)</h2>
      <form action={handleCalculate} className="ram-grid">
        <label className="clinical-field"><span>Age (yr)</span><input name="age" type="number" min={18} max={120} required className="clinical-input" /></label>
        <label className="clinical-field"><span>Weight (kg)</span><input name="weight" type="number" step="0.1" min={25} max={300} required className="clinical-input" /></label>
        <label className="clinical-field"><span>Serum Cr (mg/dL)</span><input name="scr" type="number" step="0.01" min={0.2} max={20} required className="clinical-input" /></label>
        <label className="clinical-field"><span>Sex</span><select name="sex" className="clinical-input"><option value="M">Male</option><option value="F">Female</option></select></label>
        <button type="submit" className="tactile-key">Calculate CrCl</button>
      </form>
      <output aria-live="polite" data-state={state.status} className="clinical-unit">
        {state.status === "idle" && "Awaiting validated vitals."}
        {state.status === "error" && state.message}
        {state.status === "success" && `${state.crClMlMin} mL/min`}
      </output>
    </section>
  );
}
```
- **Print Rule:** Always test the `.sus-grid` sheet with `ui_judge_gatekeeper.py <target> --wcag AAA --composite --json` prior to handoff.

## 4. 3-Layer Clinical Navigation, Silent Breadcrumbs & Anti-Slop Sterility
- **3 Complementary Nav Layers:** (1) Global (Collapsible Rail `>= 840px`, `48x48px` Bottom Bar `< 600px`), (2) In-Page Contextual ToC, and (3) Silent Breadcrumbs (`<ol role="list">` with `aria-current="page"` and CSS `li + li::before { content: "/"; }` — never raw `/` in HTML so screen readers stay silent).
- **Landmark Clarity & Ergonomics:** Assign unique `<nav aria-label>` without repeating `"navigation"`, include a GPU `.skip-link` (`transform`) to `<main id="main-content" tabindex="-1">`, preserve `DOM == Tab Order` (zero `order`/`row-reverse`/`grid-auto-flow: dense`), and ban decorative side-stripes, gradient text, mystery icon-only nav, and `01/02/03` decorative counters on clinical chrome.
