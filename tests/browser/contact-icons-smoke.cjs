const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8799';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    for (const [path, javascript] of [['/index.html', false], ['/pages/cv.html', false], ['/index.html', true], ['/pages/cv.html', true]]) {
      const context = await browser.newContext({ javaScriptEnabled: javascript });
      const page = await context.newPage();
      await page.goto(`${origin}${path}`);
      if (javascript) await page.waitForLoadState('networkidle');
      const state = await page.locator('.contact-item a[href="https://orcid.org/0009-0005-2213-1604"] .svg-icon').evaluate((icon) => {
        const style = getComputedStyle(icon);
        return {
          inline: icon.classList.contains('svg-icon--inline'),
          paths: icon.querySelectorAll('path').length,
          className: icon.getAttribute('class') || '',
          mask: style.maskImage || style.webkitMaskImage,
          color: style.color,
          paint: icon.classList.contains('svg-icon--inline') ? style.fill : style.backgroundColor,
        };
      });
      ok(!state.className.includes('icon-orcid') && state.paint === state.color, `${path} JS=${javascript}: contact icon lost path-based currentColor rendering: ${JSON.stringify(state)}`);
      if (javascript) ok(state.mask.includes('orcid.svg') && !state.inline, `${path}: hydrated contact icon did not use its local SVG mask: ${JSON.stringify(state)}`);
      else ok(state.inline && state.paths > 0, `${path}: static contact icon was not inlined: ${JSON.stringify(state)}`);
      await context.close();
    }
    console.log('Contact icon browser smoke passed');
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
