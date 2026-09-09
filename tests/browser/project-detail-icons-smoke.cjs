const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const workspace = path.resolve(__dirname, '..', '..');
const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8799';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };

async function iconState(locator) {
  return locator.evaluate((icon) => {
    const style = getComputedStyle(icon);
    const box = icon.getBoundingClientRect();
    return {
      inline: icon.classList.contains('svg-icon--inline'),
      paths: icon.querySelectorAll('path').length,
      width: box.width,
      height: box.height,
      color: style.color,
      paint: icon.classList.contains('svg-icon--inline') ? style.fill : style.backgroundColor,
      mask: style.maskImage || style.webkitMaskImage,
    };
  });
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const staticContext = await browser.newContext({ javaScriptEnabled: false });
    const staticPage = await staticContext.newPage();
    await staticPage.goto(pathToFileURL(path.join(workspace, 'pages/projects/project1.html')).href);
    const staticGithub = await iconState(staticPage.locator('.publish-link .icon-github'));
    ok(staticGithub.inline && staticGithub.paths > 0 && staticGithub.width > 0 && staticGithub.height > 0 && staticGithub.paint === staticGithub.color, `Direct-file static GitHub icon is not visible: ${JSON.stringify(staticGithub)}`);
    await staticContext.close();

    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(`${origin}/pages/projects/project1.html`);
    await page.waitForLoadState('networkidle');
    for (const [selector, asset] of [
      ['.publish-link .icon-github', 'github.svg'],
      ['.publish-link .icon-file-pdf', 'file-pdf.svg'],
      ['.publish-link .icon-bilibili', 'bilibili.svg'],
    ]) {
      const icon = page.locator(selector);
      const link = icon.locator('xpath=..');
      for (const theme of ['dark', 'light']) {
        if ((await page.locator('html').getAttribute('data-theme')) !== theme) await page.locator('.theme-toggle').click();
        await link.hover();
        await link.focus();
        const state = await iconState(icon);
        ok(!state.inline && state.width > 0 && state.height > 0 && state.paint === state.color && state.mask.includes(asset), `${selector} ${theme} hydrated state is incorrect: ${JSON.stringify(state)}`);
      }
    }
    await context.close();
    console.log('Project detail icon browser smoke passed');
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
