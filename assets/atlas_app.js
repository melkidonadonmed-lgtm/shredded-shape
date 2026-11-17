/* Atlas Unificado Shredded-Shape v1.4 — Logica UI em IIFE compativel com file:// */
(function () {
  "use strict";

  var CHAPTER_NAMES = [
    "1. Pipeline & 7 Estilos", "2. Hierarquia & Anti-Slop", "3. Mobile-First & Foco Tab",
    "4. OKLCH 5 Planos & Gradientes", "5. Elevacao & Luz Zenital", "6. Hardware Tatil & Estados",
    "7. @container, Flex & Subgrid"
  ];

  var TO_BE_ITEMS = [
    {
      id: "ui-frontend-analyst", title: "0. ui-frontend-analyst", sub: "Stage 0 · Read-Only", badge: "AST + DevTools", tone: "ok",
      cmd: "uv run python skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py assets/ui_skills_architecture_atlas.html --json",
      desc: "Auditoria AST/CDP somente leitura cobrindo 12 vetores Anti-Slop, modulos >600L e navegacao CLAREZA.",
      specs: [["Ferramentas", "chrome-devtools-plugin, modern-web-guidance"], ["Saida", "Relatorio CLAREZA em 7 secoes + Mermaid"]]
    },
    {
      id: "ui-brand-ux-planner", title: "1. ui-brand-ux-planner", sub: "Stage 1 · Read-Only", badge: "DAG <= 5", tone: "ok",
      cmd: "uv run python skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py . --style tactile --hue 255 --json",
      desc: "Projeta paleta 5-Plane OKLCH sem neon, 7 arquetipos nominais, catalogo SVG 24x24 e DAG disjunto.",
      specs: [["Planos", "--bg-well -> --bg-canvas -> --bg-card -> --bg-card-lit -> --bg-key"], ["Contrato", "DESIGN.md (8 secoes) + UIExecutionDAG"]]
    },
    {
      id: "ui-clean-worker", title: "2. ui-clean-worker", sub: "Stage 2 · ReAct + RAW", badge: "SHA-256", tone: "ok",
      cmd: "uv run python skills/ui-clean-worker/scripts/verify_raw_frontend.py assets/ui_skills_architecture_atlas.html --json",
      desc: "Materializa DESIGN.md com Tactile Matte, Nexus 135°, @container isolado de subgrid e FSM real.",
      specs: [["Pos-Edicao", "verify_raw_frontend.py (--run-tsc fail-closed)"], ["Motion", "GPU transform/opacity + allow-discrete"]]
    },
    {
      id: "ui-quality-judge", title: "3. ui-quality-judge", sub: "Stage 3 · Gatekeeper", badge: "WCAG OKLab", tone: "ok",
      cmd: "uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py assets/ui_skills_architecture_atlas.html --wcag AA --composite --json",
      desc: "Verifica contraste por polaridade OKLab, Readiness >= 90, 6-Dim >= 85, WAI-ARIA e zero Slop.",
      specs: [["Motores", "Gatekeeper + Tactile + 6-Dim evaluate_target()"], ["Ciclos", "PASSED ou REJECTED (max 3 refinamentos)"]]
    },
    {
      id: "clinical-minimalist-ui", title: "clinical-minimalist-ui", sub: "Domain · EHR/PEP", badge: "AAA Print", tone: "ok",
      cmd: "uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py . --wcag AAA --composite --json",
      desc: "Suporta prontuarios clinicos WCAG AAA >= 7.0:1, calculadoras com FSM e folhas A4 @media print.",
      specs: [["Impressao", "@page A4 12mm com zero box-shadow"], ["Seguranca", "Stage Role Guards + tabular-nums"]]
    },
    {
      id: "complex-zero", title: "complex-zero", sub: "Domain · Canvas CDP", badge: "2.4 sRGB", tone: "ok",
      cmd: "uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py assets/ui_skills_architecture_atlas.html --json",
      desc: "Inspeciona @xyflow/react, micro-batching WebSocket 150ms, Ghost Nodes e params async no Next 15+.",
      specs: [["Auditoria", "AST multi-arquivo + sonda CDP evaluate_script"], ["Limite", "<= 3 landmarks de navegacao e <= 6 abas"]]
    }
  ];

  var AS_IS_ITEMS = [
    {
      id: "asis-l3", title: "Referencia L3 Rasa", sub: "Defeito 1 · Contexto", badge: "Resolvido", tone: "warn",
      cmd: "uv run python scripts/validate_shredded_shape.py --strict",
      desc: "15 de 16 guias L3 tinham < 45 linhas sem receitas CSS/TSX concretas de espacamento e layout.",
      specs: [["Correcao", "Arquitetura L3 em 2 niveis <= 150L/arquivo"], ["Resultado", "Stage 2 com receitas prontas de @container e FSM"]]
    },
    {
      id: "asis-cli", title: "Assimetria de Flags CLI", sub: "Defeito 2 · Scripts", badge: "Resolvido", tone: "warn",
      cmd: "uv run pytest -v",
      desc: "6 scripts divergiam entre <target> posicional, --target, --scope e --out opcional.",
      specs: [["Correcao", "_ss_core.resolve_cli_target() + --out em DAG"], ["Garantia", "Self-tests e CLI positional cobertos no pytest"]]
    },
    {
      id: "asis-theme", title: "Vazamento [data-theme]", sub: "Defeito 3 · Contraste", badge: "Resolvido", tone: "danger",
      cmd: "uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py assets/ui_skills_architecture_atlas.html --json",
      desc: "Auditoria antiga ignorava temas nomeados ou misturava polaridades escura e clara no mesmo mapa.",
      specs: [["Correcao", "extract_theme_oklch_maps() isolado por polaridade"], ["Regra", "Verifica well < canvas < card < card-lit no escuro"]]
    },
    {
      id: "asis-style", title: "Lab de Estilos Parcial", sub: "Defeito 4 · Atlas", badge: "Evoluido", tone: "ok",
      cmd: "uv run python scripts/sync_shredded_shape.py",
      desc: "Preview antigo mudava apenas --lab-radius sem refletir tipografia, bordas e sombras dos 7 arquetipos.",
      specs: [["Correcao", "7 presets fisicos + 6 laboratorios interativos"], ["Entrega", "Bundle local 3 arquivos <= 520L compativel file://"]]
    }
  ];

  var STYLE_DATA = {
    soft: { title: "Soft (Nexus 135° Borderless)", meta: "radius: 1.35rem · shadow 135° · Plus Jakarta Sans", light: "Dual offset 8px/20px claro sobre canvas mineral e planos L=0.145->0.235 no escuro." },
    "hi-tech": { title: "Hi-Tech (Precisao Anodizada)", meta: "radius: 0.375rem · hairline 0.06 · Space Grotesk", light: "Topo --light-zenith sutil + borda de precisao sem halos cianos." },
    tactile: { title: "Tactile Matte (5 Planos Fisicos)", meta: "radius: 1.0rem · carved well · + .tactile-key", light: "Recessos --bg-well combinados com tampas --bg-key e LEDs 6px .lum-bead." },
    elevated: { title: "Elevated (Camadas Z Profundas)", meta: "radius: 1.10rem · penumbra negativa · frosted header", light: "Separacao clara de elevacao Z com backdrop-filter fosco e isolation." },
    retro: { title: "Retro (Regra Geometrica)", meta: "radius: 0.25rem · borda 2px · offset controlado", light: "Cantos curtos e sombra grafica limpa sem wireframes tracejados." },
    vintage: { title: "Vintage (Quiet Titanium)", meta: "radius: 0.50rem · Instrument Serif · 65ch", light: "Contraste editorial equilibrado com leitura tipografica serena." },
    clinical: { title: "Clinical (Hospitalar AAA)", meta: "radius: 0.50rem · >= 7.0:1 AAA · Folha A4", light: "Sem ofuscamento noturno e sem box-shadow no @media print." }
  };

  var SANDBOX_QUEUE = [
    { id: "rem-4092", code: "REM-4092", route: "Porto Velho -> Manaus", temp: "4.0 C", filter: "transito", status: "Em Transito", critical: true, detail: "Porto Velho -> Manaus · 4.0 C · Sensor calibrado em tempo real." },
    { id: "rem-4108", code: "REM-4108", route: "Curitiba -> Doca Sul", temp: "2.5 C", filter: "doca", status: "Doca", critical: true, detail: "Curitiba -> Doca Sul · 2.5 C · Prioridade termica alta na doca." },
    { id: "rem-4115", code: "REM-4115", route: "Campinas -> Santos", temp: "6.2 C", filter: "transito", status: "Em Transito", critical: false, detail: "Campinas -> Santos · 6.2 C · Rota nominal sem alertas." },
    { id: "rem-4120", code: "REM-4120", route: "Recife -> Hub NE", temp: "5.0 C", filter: "auditado", status: "Auditado", critical: false, detail: "Recife -> Hub NE · 5.0 C · Lote auditado e liberado." }
  ];

  var state = { chapter: 1, mode: "tobe", selectedId: TO_BE_ITEMS[0].id, rail: "expanded", exportFmt: "css", concentricErr: false, sbScope: "all", sbFilter: "todos", sbSelected: "rem-4092" };
  var toastTimer = null;

  function byId(id) { return document.getElementById(id); }

  function mk(tag, cls, txt) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (txt !== undefined) node.textContent = txt;
    return node;
  }

  function showToast(msg) {
    var el = byId("toast");
    if (!el) return;
    el.textContent = msg;
    el.classList.add("visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () { el.classList.remove("visible"); }, 2200);
  }

  function copyWithFallback(text, label) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        showToast("Copiado: " + label);
      }).catch(function () {
        openExportDialogWith(text);
      });
      return;
    }
    openExportDialogWith(text);
  }

  function setMobileDrawer(open) {
    var side = byId("side-drawer");
    var scrim = byId("drawer-scrim");
    var mainEl = byId("main-content");
    var isDesktop = window.matchMedia("(min-width: 52.5rem)").matches;
    var active = Boolean(open) && !isDesktop;
    if (side) side.classList.toggle("mobile-open", active);
    if (scrim) scrim.classList.toggle("visible", active);
    if (mainEl) mainEl.inert = active;
    if (!isDesktop && byId("nav-toggle")) byId("nav-toggle").setAttribute("aria-expanded", String(active));
  }

  function toggleRailCollapse() {
    state.rail = state.rail === "expanded" ? "collapsed" : "expanded";
    byId("app-shell").dataset.rail = state.rail;
    var expanded = state.rail === "expanded";
    if (byId("nav-toggle")) byId("nav-toggle").setAttribute("aria-expanded", String(expanded));
    if (byId("rail-collapse-btn")) byId("rail-collapse-btn").setAttribute("aria-expanded", String(expanded));
  }

  function setChapter(num, opts) {
    state.chapter = Math.max(1, Math.min(7, Number(num) || 1));
    document.querySelectorAll(".chapter-view").forEach(function (sec, idx) {
      sec.hidden = idx + 1 !== state.chapter;
    });
    document.querySelectorAll("[data-chapter]").forEach(function (btn) {
      if (Number(btn.dataset.chapter) === state.chapter) btn.setAttribute("aria-current", "page");
      else btn.removeAttribute("aria-current");
    });
    var titleEl = byId("navbar-chapter-title");
    var pagerEl = byId("pager-indicator");
    var prevBtn = byId("pager-prev");
    var nextBtn = byId("pager-next");
    if (titleEl) titleEl.textContent = CHAPTER_NAMES[state.chapter - 1];
    if (pagerEl) pagerEl.textContent = "Cap. " + state.chapter + " / 7";
    if (prevBtn) prevBtn.disabled = state.chapter === 1;
    if (nextBtn) nextBtn.disabled = state.chapter === 7;
    setMobileDrawer(false);
    var shouldAnnounceFocus = !opts || opts.focus !== false;
    var liveEl = byId("live-status");
    if (liveEl && shouldAnnounceFocus) liveEl.textContent = "Capitulo ativo: " + CHAPTER_NAMES[state.chapter - 1];
    var mainEl = byId("main-content");
    if (mainEl && shouldAnnounceFocus) mainEl.focus({ preventScroll: true });
  }

  function applyTheme(themeName) {
    document.documentElement.setAttribute("data-theme", themeName);
    var sel = byId("theme-select");
    if (sel) sel.value = themeName;
    try { window.localStorage.setItem("ss-atlas-preset", themeName); } catch (_err) { void 0; }
    refreshTokenExportText();
  }

  function applyHue(hueVal) {
    var hue = String(hueVal || "255");
    document.documentElement.style.setProperty("--brand-hue", hue);
    document.querySelectorAll("[data-hue]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.dataset.hue === hue));
    });
    var ro = byId("hue-readout");
    if (ro) ro.textContent = "H=" + hue;
    refreshTokenExportText();
  }

  function inspectNode(item) {
    if (!item) return;
    state.selectedId = item.id;
    byId("insp-title").textContent = item.title;
    byId("insp-sub").textContent = item.sub;
    byId("insp-badge").textContent = item.badge;
    byId("insp-bead").dataset.tone = item.tone || "ok";
    byId("insp-desc").textContent = item.desc;
    var copyBtn = byId("insp-copy-btn");
    copyBtn.dataset.copy = item.cmd;
    copyBtn.dataset.label = item.title;
    var dl = byId("insp-specs");
    dl.replaceChildren();
    item.specs.forEach(function (pair) {
      var row = mk("div", "spec-row");
      row.append(mk("dt", "", pair[0]), mk("dd", "", pair[1]));
      dl.appendChild(row);
    });
    renderCatalog();
  }

  function renderCatalog() {
    var grid = byId("catalog-grid");
    var empty = byId("catalog-empty");
    if (!grid || !empty) return;
    var list = state.mode === "tobe" ? TO_BE_ITEMS : AS_IS_ITEMS;
    var q = (byId("search-input").value || "").trim().toLowerCase();
    var filtered = list.filter(function (it) {
      return !q || (it.title + " " + it.desc + " " + it.sub + " " + it.badge).toLowerCase().indexOf(q) !== -1;
    });
    grid.replaceChildren();
    empty.hidden = filtered.length > 0;
    filtered.forEach(function (item) {
      var card = mk("article", "card interactive catalog-card");
      card.dataset.selected = String(item.id === state.selectedId);
      var head = mk("header", "card-head");
      var left = mk("div", "card-head-main");
      left.append(mk("h3", "truncate-safe", item.title), mk("p", "card-meta", item.sub));
      var pill = mk("span", "engraved-pill");
      var bead = mk("span", "lum-bead");
      bead.dataset.tone = item.tone || "ok";
      pill.append(bead, document.createTextNode(item.badge));
      head.append(left, pill);
      var foot = mk("footer", "card-foot flex-row");
      var btn = mk("button", "tactile-key", "Inspecionar");
      btn.type = "button";
      btn.setAttribute("aria-pressed", String(item.id === state.selectedId));
      btn.addEventListener("click", function () { inspectNode(item); });
      var cmdBtn = mk("button", "quiet-btn", "Copiar CLI");
      cmdBtn.type = "button";
      cmdBtn.addEventListener("click", function () { copyWithFallback(item.cmd, item.title); });
      foot.append(btn, cmdBtn);
      card.append(head, mk("p", "muted", item.desc), foot);
      grid.appendChild(card);
    });
    byId("main-content").dataset.state = filtered.length ? "idle" : "empty";
  }

  function updateConcentricBox() {
    var rExt = Number(byId("r-ext-slider").value);
    var pad = Number(byId("pad-slider").value);
    var rInt = state.concentricErr ? rExt : Math.max(4, rExt - pad);
    byId("r-ext-val").textContent = rExt + "px";
    byId("pad-val").textContent = pad + "px";
    var outer = byId("concentric-outer");
    var inner = byId("concentric-inner");
    outer.style.borderRadius = rExt + "px";
    outer.style.padding = pad + "px";
    inner.style.borderRadius = rInt + "px";
    byId("concentric-formula").textContent = state.concentricErr
      ? "ERRO: R_int " + rInt + "px igual a R_ext " + rExt + "px"
      : "R_int = max(4px, " + rExt + "px - " + pad + "px) = " + rInt + "px";
  }

  function selectSandboxItem(item) {
    if (!item) return;
    state.sbSelected = item.id;
    byId("sb-detail-status").textContent = item.status + (item.critical ? " · Prioritario" : "");
    byId("sb-detail-title").textContent = item.code;
    byId("sb-detail-meta").textContent = item.detail;
    renderSandboxQueue();
  }

  function renderSandboxQueue() {
    var listEl = byId("sandbox-list");
    if (!listEl) return;
    var rows = SANDBOX_QUEUE.filter(function (it) {
      var scopeOk = state.sbScope !== "alert" || it.critical;
      var filterOk = state.sbFilter === "todos" || it.filter === state.sbFilter;
      return scopeOk && filterOk;
    });
    listEl.replaceChildren();
    byId("sb-count-badge").textContent = rows.length + (rows.length === 1 ? " item" : " itens");
    rows.forEach(function (it) {
      var li = mk("li", "");
      var btn = mk("button", "list-row-btn ergo-target");
      btn.type = "button";
      btn.setAttribute("aria-pressed", String(it.id === state.sbSelected));
      btn.addEventListener("click", function () { selectSandboxItem(it); });
      var label = mk("span", "truncate-safe", it.code + " · " + it.route + " (" + it.temp + ")");
      var hint = mk("span", "engraved-pill row-action-hint", it.id === state.sbSelected ? "Ativo" : it.status);
      btn.append(label, hint);
      li.appendChild(btn);
      listEl.appendChild(li);
    });
  }

  function updateSandboxPosture(posture) {
    var shell = byId("sandbox-shell");
    if (!shell) return;
    shell.dataset.posture = posture;
    var widths = { compact: "360px", medium: "640px", expanded: "100%" };
    var labels = { compact: "Compacto: Bottom Bar + Sheet", medium: "Medio: Icon Rail 64px", expanded: "Expandido: Sidebar + Fila" };
    shell.style.setProperty("--sb-w", widths[posture] || "360px");
    byId("posture-badge").textContent = labels[posture] || "";
    document.querySelectorAll("[data-posture]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.posture === posture));
    });
  }

  function wireToggle(id, cb) {
    var el = byId(id);
    if (!el) return;
    el.addEventListener("click", function () {
      var next = el.getAttribute("aria-pressed") !== "true";
      el.setAttribute("aria-pressed", String(next));
      if (cb) cb(next, el);
    });
  }

  function wireSandboxList() {
    document.querySelectorAll("[data-sb-scope]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.sbScope = b.dataset.sbScope;
        document.querySelectorAll("[data-sb-scope]").forEach(function (x) {
          if (x === b) x.setAttribute("aria-current", "page");
          else x.removeAttribute("aria-current");
        });
        renderSandboxQueue();
      });
    });
    document.querySelectorAll("[data-sb-filter]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.sbFilter = b.dataset.sbFilter;
        document.querySelectorAll("[data-sb-filter]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        renderSandboxQueue();
      });
    });
    wireToggle("sb-rail-toggle", function (next) { byId("sandbox-shell").dataset.sbCollapsed = String(next); });
    byId("sandbox-cta").addEventListener("click", function () { showToast("Lote despachado: " + state.sbSelected.toUpperCase()); });
  }

  function updateCqWidth(pxVal) {
    var clamped = Math.max(260, Math.min(820, Math.round(pxVal)));
    var host = byId("cq-host");
    if (host) host.style.setProperty("--cq-w", clamped + "px");
    var stageTxt = clamped < 380 ? "Estagio 1: Pilha Vertical (<380px)" : (clamped < 580 ? "Estagio 2: Grade Dupla (>=380px)" : "Estagio 3: Expandido (>=580px)");
    byId("cq-width-label").textContent = clamped + "px · " + stageTxt;
    document.querySelectorAll("[data-cq-preset]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(Number(b.dataset.cqPreset) === clamped));
    });
  }

  function buildExportTokensText(fmt) {
    var hue = document.documentElement.style.getPropertyValue("--brand-hue") || "255";
    var theme = document.documentElement.getAttribute("data-theme") || "tactile-matte";
    if (fmt === "tailwind") {
      return "@theme {\n  --color-bg-well: var(--bg-well);\n  --color-bg-canvas: var(--bg-canvas);\n  --color-bg-card: var(--bg-card);\n  --color-bg-card-lit: var(--bg-card-lit);\n  --color-bg-key: var(--bg-key);\n  --color-ink-on-key: var(--ink-on-key);\n  --color-brand-primary: oklch(0.72 0.14 " + hue + ");\n  --color-brand-fill: var(--brand-fill);\n  --color-ink-on-brand: var(--ink-on-brand);\n  --radius-card: 1rem;\n}\n/* Tema ativo: " + theme + " */";
    }
    return ":root {\n  color-scheme: light dark;\n  --brand-hue: " + hue + ";\n  --bg-well: light-dark(oklch(0.922 0.010 250), oklch(0.118 0.012 260));\n  --bg-canvas: light-dark(oklch(0.962 0.007 250), oklch(0.145 0.014 260));\n  --bg-card: light-dark(oklch(0.994 0.003 250), oklch(0.195 0.018 262));\n  --bg-card-lit: light-dark(oklch(1.000 0.000 0), oklch(0.235 0.022 262));\n  --bg-key: light-dark(oklch(0.998 0.002 250), oklch(0.262 0.024 262));\n  --ink-on-key: light-dark(oklch(0.175 0.020 255), oklch(0.955 0.008 255));\n  --brand-primary: light-dark(oklch(0.46 0.15 " + hue + "), oklch(0.72 0.14 " + hue + "));\n  --brand-fill: light-dark(oklch(0.43 0.15 " + hue + "), oklch(0.75 0.14 " + hue + "));\n  --ink-on-brand: light-dark(oklch(0.992 0.003 255), oklch(0.140 0.022 255));\n}";
  }

  function refreshTokenExportText() {
    var area = byId("token-export-code");
    if (area) area.value = buildExportTokensText(state.exportFmt);
  }

  function openExportDialogWith(overrideText) {
    var dlg = byId("token-export-modal"), area = byId("token-export-code");
    if (!dlg || !area) return;
    area.value = overrideText || buildExportTokensText(state.exportFmt);
    if (typeof dlg.showModal === "function" && !dlg.open) dlg.showModal();
    if (overrideText) { area.focus(); area.select(); }
    else if (byId("copy-export-btn")) { byId("copy-export-btn").focus(); }
  }

  function wireDragContainer() {
    var handle = byId("cq-drag-handle"), host = byId("cq-host");
    if (!handle || !host) return;
    var active = false, startX = 0, startW = 680;
    handle.addEventListener("pointerdown", function (ev) {
      active = true; startX = ev.clientX; startW = host.getBoundingClientRect().width;
      handle.setPointerCapture(ev.pointerId);
    });
    handle.addEventListener("pointermove", function (ev) { if (active) updateCqWidth(startW + (ev.clientX - startX)); });
    handle.addEventListener("pointerup", function () { active = false; });
    handle.addEventListener("keydown", function (ev) {
      var cur = host.getBoundingClientRect().width;
      if (ev.key === "ArrowLeft") updateCqWidth(cur - 40);
      if (ev.key === "ArrowRight") updateCqWidth(cur + 40);
    });
  }

  function wireSlidersAndDemos() {
    byId("r-ext-slider").addEventListener("input", updateConcentricBox);
    byId("pad-slider").addEventListener("input", updateConcentricBox);
    byId("toggle-concentric-err").addEventListener("click", function () {
      state.concentricErr = !state.concentricErr;
      this.setAttribute("aria-pressed", String(state.concentricErr));
      updateConcentricBox();
    });
    byId("toggle-slop-diag").addEventListener("click", function () {
      var on = this.getAttribute("aria-pressed") === "true";
      var next = !on;
      this.setAttribute("aria-pressed", String(next));
      byId("diag-clean-box").hidden = next;
      byId("diag-slop-svg").hidden = !next;
    });
    byId("grad-angle-slider").addEventListener("input", function () {
      document.documentElement.style.setProperty("--light-angle", this.value + "deg");
      byId("grad-angle-val").textContent = this.value + "deg";
    });
    byId("spec-slider").addEventListener("input", function () {
      document.documentElement.style.setProperty("--specular-strength", (Number(this.value) / 100).toFixed(2));
      byId("spec-val").textContent = this.value + "%";
    });
    byId("shadow-y-slider").addEventListener("input", function () {
      document.documentElement.style.setProperty("--shadow-y-scale", (Number(this.value) / 100).toFixed(2));
      byId("shadow-y-val").textContent = (Number(this.value) / 100).toFixed(1) + "x";
    });
    byId("grain-slider").addEventListener("input", function () {
      document.documentElement.style.setProperty("--matte-grain", (Number(this.value) / 1000).toFixed(3));
      byId("grain-val").textContent = (Number(this.value) / 10).toFixed(1) + "%";
    });
    document.querySelectorAll("[data-grad-pair]").forEach(function (b) {
      b.addEventListener("click", function () {
        var c1 = b.dataset.c1, c2 = b.dataset.c2;
        byId("bar-oklch").style.background = "linear-gradient(in oklch to right, " + c1 + ", " + c2 + ")";
        byId("bar-srgb").style.background = "linear-gradient(in srgb to right, " + c1 + ", " + c2 + ")";
        document.querySelectorAll("[data-grad-pair]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      });
    });
  }

  function wireNavigationAndTheme() {
    document.querySelectorAll("[data-chapter]").forEach(function (btn) {
      btn.addEventListener("click", function () { setChapter(btn.dataset.chapter); });
    });
    byId("pager-prev").addEventListener("click", function () { setChapter(state.chapter - 1); });
    byId("pager-next").addEventListener("click", function () { setChapter(state.chapter + 1); });
    byId("nav-toggle").addEventListener("click", function () {
      if (window.matchMedia("(min-width: 52.5rem)").matches) toggleRailCollapse();
      else setMobileDrawer(!byId("side-drawer").classList.contains("mobile-open"));
    });
    byId("rail-collapse-btn").addEventListener("click", toggleRailCollapse);
    byId("drawer-scrim").addEventListener("click", function () { setMobileDrawer(false); });
    byId("theme-select").addEventListener("change", function () { applyTheme(this.value); });
    document.querySelectorAll("[data-hue]").forEach(function (b) { b.addEventListener("click", function () { applyHue(b.dataset.hue); }); });
    document.querySelectorAll("[data-catalog-mode]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.mode = b.dataset.catalogMode;
        document.querySelectorAll("[data-catalog-mode]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        inspectNode(state.mode === "tobe" ? TO_BE_ITEMS[0] : AS_IS_ITEMS[0]);
      });
    });
    byId("search-input").addEventListener("input", renderCatalog);
  }

  function wireStyleAndInteractions() {
    wireNavigationAndTheme();
    document.querySelectorAll("[data-style-key]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.dataset.styleKey;
        var info = STYLE_DATA[key];
        byId("style-lab-stage").dataset.previewStyle = key;
        byId("lab-title").textContent = info.title;
        byId("lab-meta").textContent = info.meta;
        byId("lab-light").textContent = info.light;
        document.querySelectorAll("[data-style-key]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === btn)); });
      });
    });
    document.querySelectorAll("[data-posture]").forEach(function (b) { b.addEventListener("click", function () { updateSandboxPosture(b.dataset.posture); }); });
    wireToggle("toggle-stretch-btn", function (next) { byId("sandbox-cta").style.inlineSize = next ? "100%" : "auto"; });
    wireToggle("toggle-tabs-wrap", function (next) { byId("sandbox-tabs").classList.toggle("is-wrapped", next); });
    wireToggle("toggle-ergo-guides", function (next) { byId("sandbox-shell").classList.toggle("ergo-guides", next); });
    wireToggle("demo-latch-btn");
    document.querySelectorAll("[data-rate-btn]").forEach(function (b) {
      b.addEventListener("click", function () { document.querySelectorAll("[data-rate-btn]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); });
    });
    document.querySelectorAll("[data-cq-preset]").forEach(function (b) { b.addEventListener("click", function () { updateCqWidth(Number(b.dataset.cqPreset)); }); });
    document.querySelectorAll(".accordion-trigger").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest(".accordion-card");
        if (!card) return;
        var open = card.dataset.open !== "true";
        card.dataset.open = String(open);
        btn.setAttribute("aria-expanded", String(open));
      });
    });
    wireDialogsAndHotkeys();
  }

  function wireDialogsAndHotkeys() {
    byId("open-export-btn").addEventListener("click", function () { openExportDialogWith(); });
    byId("close-export-btn").addEventListener("click", function () { byId("token-export-modal").close(); });
    byId("copy-export-btn").addEventListener("click", function () { copyWithFallback(byId("token-export-code").value, "Tokens CSS"); });
    document.querySelectorAll("[data-export-fmt]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.exportFmt = b.dataset.exportFmt;
        document.querySelectorAll("[data-export-fmt]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        refreshTokenExportText();
      });
    });
    document.addEventListener("click", function (ev) {
      var target = ev.target.closest("[data-copy]");
      if (target) copyWithFallback(target.dataset.copy, target.dataset.label || "Comando");
    });
    document.addEventListener("keydown", function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "k") { ev.preventDefault(); byId("search-input").focus(); }
      if (ev.key === "Escape") setMobileDrawer(false);
      var tag = document.activeElement ? document.activeElement.tagName : "";
      if (ev.key === "[" && tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT" && window.matchMedia("(min-width: 52.5rem)").matches) {
        toggleRailCollapse();
      }
    });
  }

  function init() {
    try {
      var saved = window.localStorage.getItem("ss-atlas-preset");
      if (saved) applyTheme(saved);
    } catch (_err) { void 0; }
    applyHue("255");
    setChapter(1, { focus: false });
    inspectNode(TO_BE_ITEMS[0]);
    updateConcentricBox();
    updateSandboxPosture("compact");
    renderSandboxQueue();
    updateCqWidth(680);
    wireSlidersAndDemos();
    wireSandboxList();
    wireStyleAndInteractions();
    wireDragContainer();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
