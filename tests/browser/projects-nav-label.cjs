const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };
const pages = [
  ['index.html', 'index.html#projects'],
  ['pages/cv.html', '../index.html#projects'],
  ['pages/projects/project1.html', '../../index.html#projects'],
];

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    for (const javaScriptEnabled of [false, true]) {
      const context = await browser.newContext({ javaScriptEnabled });
      if (javaScriptEnabled) await context.addInitScript(() => localStorage.setItem('lang', 'en'));
      const page = await context.newPage();
      for (const [path, href] of pages) {
        await page.goto(`${origin}/${path}`);
        if (javaScriptEnabled) await page.waitForLoadState('networkidle');
        const nav = page.locator(`.nav-links a[href="${href}"]`);
        ok(await nav.count() === 1, `${path}: Projects navigation link is missing`);
        ok(await nav.getAttribute('data-i18n') === 'nav.projects' && (await nav.textContent()).trim() === 'Projects', `${path}: static/hydrated English label is not Projects`);
        if (javaScriptEnabled) {
          await page.locator('.lang-toggle').click();
          await page.waitForFunction((link) => link.textContent.trim() === '项目', await nav.elementHandle());
          ok((await nav.textContent()).trim() === '项目', `${path}: Chinese navigation label changed`);
          await page.locator('.lang-toggle').click();
          await page.waitForFunction((link) => link.textContent.trim() === 'Projects', await nav.elementHandle());
          ok((await nav.textContent()).trim() === 'Projects', `${path}: English label did not return to Projects`);
        }
      }
      await context.close();
    }
    console.log('Projects navigation label browser regression passed');
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
