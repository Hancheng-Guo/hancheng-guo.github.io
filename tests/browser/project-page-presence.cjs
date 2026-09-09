const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };
const html = '<!doctype html><link rel="stylesheet" href="assets/css/style.css"><body data-page="home"><main><section id="projects"><div class="projects-grid"></div></section></main><script type="module" src="assets/js/app.js"></script>';
const project = (id, hasDetailPage) => ({ id, page: `pages/projects/${id}.html`, hasDetailPage, thumbnail: { src: 'assets/images/Avatar.jpg', alt: { en: id, zh: id } }, tags: [], locales: { en: { title: id, summary: 'Summary', blocks: [] }, zh: { title: id, summary: '摘要', blocks: [] } }, links: [] });

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    const data = { schemaVersion: 2, projects: [project('with-page', true), project('card-only', false)] };
    await page.route('**/project-page-presence.html', (route) => route.fulfill({ contentType: 'text/html', body: html }));
    await page.route('**/assets/data/projects.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify(data) }));
    await page.goto(`${origin}/project-page-presence.html`);
    await page.waitForLoadState('networkidle');
    const detailed = page.locator('.card').filter({ hasText: 'with-page' });
    const cardOnly = page.locator('.card').filter({ hasText: 'card-only' });
    ok(await detailed.getAttribute('role') === 'link' && await detailed.getAttribute('tabindex') === '0' && await detailed.locator('.project-link').count() === 1, 'Detail project lost its static-equivalent link behavior');
    const inert = await cardOnly.evaluate((card) => ({ tabindex: card.getAttribute('tabindex'), role: card.getAttribute('role'), label: card.getAttribute('aria-label'), href: card.getAttribute('data-project-href'), cue: card.querySelector('.project-link')?.textContent.trim(), status: card.querySelector('.project-status')?.textContent.trim(), arrow: card.querySelector('.chevron-right'), cursor: getComputedStyle(card).cursor }));
    ok(inert.tabindex === '0' && inert.role === null && inert.label === null && inert.href === null && inert.cue === 'Details Coming Soon ...' && inert.status === 'Details Coming Soon ...' && inert.arrow === null && inert.cursor !== 'pointer', `Page-less card must be focusable but non-operable after hydration: ${JSON.stringify(inert)}`);
    await cardOnly.hover();
    ok(await cardOnly.evaluate((card) => getComputedStyle(card).cursor) !== 'pointer', 'Page-less card shows pointer on hover');
    await cardOnly.click();
    ok(page.url().endsWith('/project-page-presence.html'), 'Click navigated a page-less card');
    await cardOnly.focus();
    ok(await page.evaluate(() => document.activeElement?.textContent.includes('card-only')), 'Page-less card is not keyboard-focusable');
    ok(await cardOnly.evaluate((card) => getComputedStyle(card).cursor) !== 'pointer', 'Page-less card shows pointer on focus');
    await page.keyboard.press('Enter');
    ok(page.url().endsWith('/project-page-presence.html'), 'Enter navigated a page-less card');
    await page.keyboard.press('Space');
    ok(page.url().endsWith('/project-page-presence.html'), 'Space navigated a page-less card');
    await detailed.focus();
    await Promise.all([page.waitForURL('**/pages/projects/with-page.html'), page.keyboard.press('Enter')]);
    await context.close();
    const chineseContext = await browser.newContext();
    await chineseContext.addInitScript(() => localStorage.setItem('lang', 'zh'));
    const chinesePage = await chineseContext.newPage();
    await chinesePage.route('**/project-page-presence.html', (route) => route.fulfill({ contentType: 'text/html', body: html }));
    await chinesePage.route('**/assets/data/projects.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify(data) }));
    await chinesePage.goto(`${origin}/project-page-presence.html`);
    await chinesePage.waitForLoadState('networkidle');
    const chineseCardOnly = chinesePage.locator('.card').filter({ hasText: 'card-only' });
    ok((await chineseCardOnly.locator('.project-status').textContent()).trim() === '详情即将上线…', 'Page-less card did not use the Chinese coming-soon translation');
    ok(await chineseCardOnly.getAttribute('tabindex') === '0' && await chineseCardOnly.getAttribute('role') === null && await chineseCardOnly.getAttribute('data-project-href') === null, 'Chinese page-less card lost its non-operable focus behavior');
    await chineseContext.close();
    console.log('Project detail-page presence browser regression passed');
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
