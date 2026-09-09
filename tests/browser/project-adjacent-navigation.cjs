const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };
const project = (id, hasDetailPage, status) => ({
  id,
  page: `pages/projects/${id}.html`,
  hasDetailPage,
  ...(status ? { status } : {}),
  thumbnail: { src: 'assets/images/Avatar.jpg', alt: { en: id, zh: id } },
  tags: [],
  locales: { en: { title: id, summary: 'Summary', blocks: [] }, zh: { title: id, summary: '摘要', blocks: [] } },
  links: [],
});

async function links(page) {
  return page.locator('.project-adjacent-link').evaluateAll((items) => items.map((item) => ({
    className: item.className,
    href: new URL(item.href).pathname,
  })));
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const noJs = await browser.newContext({ javaScriptEnabled: false });
    const staticPage = await noJs.newPage();
    await staticPage.goto(`${origin}/pages/projects/project2.html`);
    ok(JSON.stringify(await links(staticPage)) === JSON.stringify([
      { className: 'project-adjacent-link previous', href: '/pages/projects/project1.html' },
      { className: 'project-adjacent-link next', href: '/pages/projects/project4.html' },
    ]), 'Static project navigation did not skip the coming-soon project');
    for (const target of ['/pages/projects/project1.html', '/pages/projects/project4.html']) {
      const response = await staticPage.goto(`${origin}${target}`);
      ok(response?.ok(), `Static adjacent target is missing: ${target}`);
    }
    await noJs.close();

    const context = await browser.newContext();
    const page = await context.newPage();
    const fixture = { schemaVersion: 2, projects: [
      project('leading-soon', false),
      project('project1', true),
      project('project2', true),
      project('middle-soon-1', false),
      project('middle-soon-2', false),
      project('project4', true),
      project('trailing-soon', false),
      project('draft', true, 'draft'),
    ] };
    await page.route('**/assets/data/projects.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify(fixture) }));
    await page.goto(`${origin}/pages/projects/project2.html`);
    await page.waitForLoadState('networkidle');
    ok(JSON.stringify(await links(page)) === JSON.stringify([
      { className: 'project-adjacent-link previous', href: '/pages/projects/project1.html' },
      { className: 'project-adjacent-link next', href: '/pages/projects/project4.html' },
    ]), 'Hydrated project navigation did not skip coming-soon or draft projects');
    for (const target of ['/pages/projects/project1.html', '/pages/projects/project4.html']) {
      const response = await page.request.get(`${origin}${target}`);
      ok(response.ok(), `Hydrated adjacent target is missing: ${target}`);
    }

    await page.unroute('**/assets/data/projects.json');
    await page.route('**/assets/data/projects.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify({ schemaVersion: 2, projects: [project('project2', true)] }) }));
    await page.goto(`${origin}/pages/projects/project2.html`);
    await page.waitForLoadState('networkidle');
    ok((await links(page)).length === 0, 'A sole detail page must not show adjacent buttons after hydration');
    await context.close();
    console.log('Project adjacent navigation browser regression passed');
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
