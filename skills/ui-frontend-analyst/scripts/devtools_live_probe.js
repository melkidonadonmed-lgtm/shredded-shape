/**
 * devtools_live_probe.js
 * Injected via chrome-devtools-mcp evaluate_script to collect live computed UI telemetry.
 */
(() => {
  const docEl = document.documentElement;
  const body = document.body;
  const navNodes = Array.from(document.querySelectorAll('nav, [role="navigation"]'));
  const interactive = Array.from(document.querySelectorAll('a, button, input, select, [role="button"], [role="tab"]'));

  const crampedMenus = [];
  const wrappedNavItems = [];
  const smallTargets = [];
  const colors = new Set();
  const fonts = new Set();
  const syntheticEls = [];
  let mysteryIconOnlyNavCount = 0;

  const extractCleanNavLabel = (el) => {
    const clone = el.cloneNode(true);
    clone.querySelectorAll('svg, .sr-only, .nav-step, [aria-hidden="true"]').forEach((n) => n.remove());
    return (clone.textContent || '').replace(/\s+/g, ' ').trim();
  };

  for (const nav of navNodes) {
    const navRect = nav.getBoundingClientRect();
    const isNavVisible = navRect.width > 0 && navRect.height > 0;
    const navStyle = getComputedStyle(nav);
    const navGap = parseFloat(navStyle.gap || navStyle.columnGap || '8');
    for (const item of nav.querySelectorAll('a, button')) {
      const style = getComputedStyle(item);
      if (parseFloat(style.fontSize) < 13 || (!Number.isNaN(navGap) && navGap < 8)) {
        crampedMenus.push({
          text: (item.textContent || '').trim().slice(0, 40),
          fontSize: style.fontSize,
          gap: navStyle.gap || '0px',
        });
      }
      if (!isNavVisible) continue;
      const itemRect = item.getBoundingClientRect();
      if (itemRect.width <= 0 || itemRect.height <= 0) continue;
      const cleanLabel = extractCleanNavLabel(item);
      if (cleanLabel && (item.getClientRects().length > 1 || cleanLabel.length > 28)) {
        wrappedNavItems.push({ text: cleanLabel.slice(0, 40), length: cleanLabel.length, rects: item.getClientRects().length });
      }
      if (!cleanLabel && item.querySelector('svg') && !item.getAttribute('aria-label') && !item.getAttribute('title') && !item.getAttribute('data-tooltip')) {
        mysteryIconOnlyNavCount++;
      }
    }
  }

  const isCoarse = typeof window.matchMedia === 'function' && window.matchMedia('(any-pointer: coarse)').matches;
  const minTargetPx = isCoarse ? 48 : 44;
  const pseudoIconRe = /[✕✖✗✘≡⋮⋯▾▸▴◂▼▲▶◀☰⚙★☆🗑✎✏]|^[+×←→↑↓✓✔]$/;
  const pseudoIconControls = [];
  const clippedControls = [];

  for (const el of interactive.slice(0, 200)) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const labelText = (el.textContent || el.getAttribute('aria-label') || '').trim();
    if (rect.width > 0 && rect.height > 0 && (rect.width < minTargetPx || rect.height < minTargetPx)) {
      smallTargets.push({
        tag: el.tagName.toLowerCase(),
        text: labelText.slice(0, 32),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      });
    }
    if (labelText && pseudoIconRe.test(labelText)) {
      pseudoIconControls.push({ tag: el.tagName.toLowerCase(), text: labelText.slice(0, 24) });
    }
    if (el.scrollWidth > el.clientWidth + 1 && style.overflowX !== 'visible') {
      clippedControls.push({ tag: el.tagName.toLowerCase(), text: labelText.slice(0, 32), scrollWidth: el.scrollWidth, clientWidth: el.clientWidth });
    }
    colors.add(style.color);
    colors.add(style.backgroundColor);
    fonts.add(style.fontFamily.split(',')[0].replace(/['"]/g, '').trim());
    if (style.fontSynthesis && style.fontSynthesis !== 'none') syntheticEls.push(el.tagName.toLowerCase());
  }

  let maxDepth = 0;
  let blurBlobElementsCount = 0;
  let neonGlowCount = 0;
  let dashedWireframeCount = 0;
  let gradientTextCount = 0;
  const walk = (node, depth) => {
    if (depth > maxDepth) maxDepth = depth;
    const cs = getComputedStyle(node);
    const blurMatch = (cs.filter || '').match(/blur\((\d+(?:\.\d+)?)px\)/i);
    if (blurMatch && parseFloat(blurMatch[1]) >= 40) blurBlobElementsCount++;
    if (/0px\s+0px\s+(?:1[2-9]|[2-9]\d+)px/.test(cs.boxShadow || '')) neonGlowCount++;
    if ([cs.borderTopStyle, cs.borderRightStyle, cs.borderBottomStyle, cs.borderLeftStyle].includes('dashed')) {
      dashedWireframeCount++;
    }
    if ((cs.backgroundClip === 'text' || cs.webkitBackgroundClip === 'text')
      && (cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)' || cs.color === 'rgba(0, 0, 0, 0)')
      && (cs.backgroundImage || '').includes('gradient')) {
      gradientTextCount++;
    }
    if (depth > 28) return;
    for (const child of node.children) walk(child, depth + 1);
  };
  if (body) walk(body, 0);

  let malformedSvgCount = 0;
  for (const svg of document.querySelectorAll('svg')) {
    if (svg.closest('svg[hidden]') || svg.hasAttribute('hidden') || svg.querySelector('symbol, defs, use')) continue;
    const r = svg.getBoundingClientRect();
    if (Math.max(r.width, r.height) > 48) continue;
    if (svg.children.length === 0 || !svg.hasAttribute('viewBox')) malformedSvgCount++;
  }

  const orphanedInputsCount = Array.from(document.querySelectorAll('input, select, textarea')).filter((inp) => {
    const safeId = inp.id && typeof CSS !== 'undefined' && typeof CSS.escape === 'function' ? CSS.escape(inp.id) : inp.id;
    const hasFor = safeId && document.querySelector(`label[for="${safeId}"]`);
    const hasAria = inp.getAttribute('aria-label') || inp.getAttribute('aria-labelledby');
    return !hasFor && !hasAria && !inp.closest('label');
  }).length;

  const emojiRe = /[\u{1F300}-\u{1FAFF}\u{26A0}-\u{26FF}\u{2702}-\u{27B0}]/gu;
  const emojiMatches = (body ? body.innerText || '' : '').match(emojiRe) || [];
  const bodyOptimizeLegibility = body ? getComputedStyle(body).textRendering === 'optimizelegibility' : false;
  const mainEl = document.querySelector('main[tabindex="-1"]');
  const mainCs = mainEl ? getComputedStyle(mainEl) : null;
  const mainFocusOutline = Boolean(mainCs && mainCs.outlineStyle !== 'none' && parseFloat(mainCs.outlineWidth || '0') > 0);
  const skipLinkPresent = Boolean(
    Array.from(document.querySelectorAll('a[href^="#"]')).slice(0, 5).find((a) => {
      const id = (a.getAttribute('href') || '').slice(1);
      const tgt = id ? document.getElementById(id) : null;
      return Boolean(tgt && tgt.matches('main, [role="main"], #main, #content, #conteudo-principal'));
    })
  );

  return {
    url: location.href,
    viewport: { width: window.innerWidth, height: window.innerHeight },
    horizontalOverflow: docEl.scrollWidth > window.innerWidth,
    domDepthMax: maxDepth,
    navCount: navNodes.length,
    crampedMenus: crampedMenus.slice(0, 20),
    crampedMenuItems: crampedMenus.slice(0, 20),
    wrappedNavItems: wrappedNavItems.slice(0, 20),
    mysteryIconOnlyNavCount,
    gradientTextCount,
    skipLinkPresent,
    smallTouchTargetsCount: smallTargets.length,
    smallTouchTargetsSample: smallTargets.slice(0, 15),
    smallTouchTargets: smallTargets.slice(0, 15),
    uniqueComputedColorsSample: Array.from(colors).slice(0, 25),
    uniqueColorsSample: Array.from(colors).slice(0, 25),
    computedFontFamilies: Array.from(fonts).filter(Boolean),
    fontFamilies: Array.from(fonts).filter(Boolean),
    loadedFontFaces: Array.from(document.fonts || []).map((f) => `${f.family}:${f.weight}:${f.status}`).slice(0, 20),
    syntheticFonts: syntheticEls.slice(0, 20),
    blurBlobElementsCount,
    neonGlowCount,
    dashedWireframeCount,
    bodyOptimizeLegibility,
    mainFocusOutline,
    malformedSvgCount,
    orphanedInputsCount,
    emojiCount: emojiMatches.length,
    emojiHits: emojiMatches.length,
    interactiveTotal: interactive.length,
    interactiveTruncated: interactive.length > 200,
    pseudoIconControlsCount: pseudoIconControls.length,
    pseudoIconControlsSample: pseudoIconControls.slice(0, 15),
    clippedControlsCount: clippedControls.length,
    clippedControlsSample: clippedControls.slice(0, 15),
    routeManifest: Array.from(document.querySelectorAll('[role="tab"], a[href], button[data-route]'))
      .map((el) => (el.getAttribute('href') || el.getAttribute('data-route') || el.textContent || '').trim())
      .filter(Boolean)
      .slice(0, 30),
    openOverlaysInspected: document.querySelectorAll('dialog[open], [role="dialog"]:not([aria-hidden="true"]), [popover]:popover-open').length,
  };
})();
