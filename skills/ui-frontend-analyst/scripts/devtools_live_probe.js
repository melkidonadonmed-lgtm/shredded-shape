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
  const smallTargets = [];
  const colors = new Set();
  const fonts = new Set();
  const syntheticEls = [];

  for (const nav of navNodes) {
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
    }
  }

  const isCoarse = typeof window.matchMedia === 'function' && window.matchMedia('(any-pointer: coarse)').matches;
  const minTargetPx = isCoarse ? 48 : 44;

  for (const el of interactive.slice(0, 200)) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    if (rect.width > 0 && rect.height > 0 && (rect.width < minTargetPx || rect.height < minTargetPx)) {
      smallTargets.push({
        tag: el.tagName.toLowerCase(),
        text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 32),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      });
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
  const walk = (node, depth) => {
    if (depth > maxDepth) maxDepth = depth;
    const cs = getComputedStyle(node);
    const blurMatch = (cs.filter || '').match(/blur\((\d+(?:\.\d+)?)px\)/i);
    if (blurMatch && parseFloat(blurMatch[1]) >= 40) blurBlobElementsCount++;
    if (/0px\s+0px\s+(?:1[2-9]|[2-9]\d+)px/.test(cs.boxShadow || '')) neonGlowCount++;
    if ([cs.borderTopStyle, cs.borderRightStyle, cs.borderBottomStyle, cs.borderLeftStyle].includes('dashed')) {
      dashedWireframeCount++;
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

  return {
    url: location.href,
    viewport: { width: window.innerWidth, height: window.innerHeight },
    horizontalOverflow: docEl.scrollWidth > window.innerWidth,
    domDepthMax: maxDepth,
    navCount: navNodes.length,
    crampedMenus: crampedMenus.slice(0, 20),
    crampedMenuItems: crampedMenus.slice(0, 20),
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
  };
})();
