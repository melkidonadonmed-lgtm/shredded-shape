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

  for (const nav of navNodes) {
    const items = nav.querySelectorAll('a, button');
    for (const item of items) {
      const style = getComputedStyle(item);
      if (parseFloat(style.fontSize) < 13) {
        crampedMenus.push({ text: (item.textContent || '').trim().slice(0, 40), fontSize: style.fontSize });
      }
    }
  }

  for (const el of interactive.slice(0, 200)) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
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
  }

  let maxDepth = 0;
  const walk = (node, depth) => {
    if (depth > maxDepth) maxDepth = depth;
    if (depth > 28) return;
    for (const child of node.children) walk(child, depth + 1);
  };
  if (body) walk(body, 0);

  const emojiRe = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu;
  const visibleText = body ? body.innerText || '' : '';
  const emojiMatches = visibleText.match(emojiRe) || [];

  return {
    url: location.href,
    viewport: { width: window.innerWidth, height: window.innerHeight },
    horizontalOverflow: docEl.scrollWidth > window.innerWidth,
    domDepthMax: maxDepth,
    navCount: navNodes.length,
    crampedMenus: crampedMenus.slice(0, 20),
    smallTouchTargetsCount: smallTargets.length,
    smallTouchTargetsSample: smallTargets.slice(0, 15),
    uniqueComputedColorsSample: Array.from(colors).slice(0, 25),
    computedFontFamilies: Array.from(fonts).filter(Boolean),
    loadedFontFaces: Array.from(document.fonts || []).map((f) => `${f.family}:${f.weight}:${f.status}`).slice(0, 20),
    emojiCount: emojiMatches.length,
  };
})();
