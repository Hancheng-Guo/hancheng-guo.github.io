const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };
const site = {
  schemaVersion: 1,
  site: { name: { en: 'Test', zh: '测试' }, author: { en: 'Test', zh: '测试' }, copyrightText: { en: '', zh: '' }, lastUpdateDate: '2026-01-01' },
  profile: { name: { en: 'Test', zh: '测试' }, summary: { en: 'Summary', zh: '简介' } }, contacts: [],
  resume: { label: { en: 'Download CV', zh: '下载简历' }, url: { en: 'assets/documents/CVTest.pdf', zh: 'assets/documents/CVTest.pdf' } },
  education: [], workExperience: [], awards: [], techStack: [], publications: { journalArticles: [], conferencePapers: [] }, timeline: [],
  layout: { homeFields: ['profile'], cvFields: [] },
};
const nav = '<nav><div class="nav-links"><a href="index.html#profile" data-i18n="nav.profile">Profile</a></div><button class="lang-toggle" data-language="en"></button><button class="theme-toggle"></button><button class="menu-toggle"></button></nav>';
const home = `<!doctype html><link rel="stylesheet" href="assets/css/style.css"><body data-page="home">${nav}<main><section id="profile" class="intro profile-section"><div class="container"><h1 class="hero-title">Test</h1><div class="hero-summary">Summary</div><div class="intro-actions"><a class="publish-link primary-action" href="assets/documents/CVTest.pdf" download>Download CV</a></div><div class="contact-links"></div></div></section></main><script type="module" src="assets/js/app.js"></script>`;
const project = `<!doctype html><link rel="stylesheet" href="../../assets/css/style.css"><body data-page="project" data-project-id="demo">${nav.replaceAll('index.html', '../../index.html').replaceAll('assets/', '../../assets/')}<main><div class="project-container"></div></main><script type="module" src="../../assets/js/app.js"></script>`;

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const noJsContext = await browser.newContext({ javaScriptEnabled: false });
    const noJs = await noJsContext.newPage();
    await noJs.route('**/cv-disabled-home.html', (route) => route.fulfill({ contentType: 'text/html', body: home }));
    await noJs.route('**/pages/projects/cv-disabled-project.html', (route) => route.fulfill({ contentType: 'text/html', body: project }));
    await noJs.goto(`${origin}/cv-disabled-home.html`);
    ok(await noJs.locator('[data-i18n="nav.resume"]').count() === 0, 'Static disabled home still exposes CV navigation');
    ok(await noJs.locator('.primary-action[download]').count() === 1, 'Static disabled home lost its PDF download');
    await noJs.goto(`${origin}/pages/projects/cv-disabled-project.html`);
    ok(await noJs.locator('[data-i18n="nav.resume"]').count() === 0, 'Static disabled project still exposes CV navigation');
    await noJsContext.close();

    const page = await browser.newPage();
    await page.route('**/cv-disabled-home.html', (route) => route.fulfill({ contentType: 'text/html', body: home }));
    await page.route('**/pages/projects/cv-disabled-project.html', (route) => route.fulfill({ contentType: 'text/html', body: project }));
    await page.route('**/assets/data/site.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify(site) }));
    await page.route('**/assets/data/projects.json', (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify({ schemaVersion: 2, projects: [] }) }));
    await page.goto(`${origin}/cv-disabled-home.html`); await page.waitForLoadState('networkidle');
    ok(await page.locator('[data-i18n="nav.resume"]').count() === 0, 'Hydrated disabled home recreated CV navigation');
    ok(await page.locator('.primary-action[download]').count() === 1, 'Hydrated disabled home lost its PDF download');
    await page.locator('.lang-toggle').click();
    ok(await page.locator('[data-i18n="nav.resume"]').count() === 0, 'Language change recreated CV navigation');
    await page.goto(`${origin}/pages/projects/cv-disabled-project.html`); await page.waitForLoadState('networkidle');
    ok(await page.locator('[data-i18n="nav.resume"]').count() === 0, 'Hydrated disabled project recreated CV navigation');
    console.log('Disabled CV browser regression passed');
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
