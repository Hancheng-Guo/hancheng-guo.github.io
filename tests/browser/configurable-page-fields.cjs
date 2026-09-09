const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };
const site = {
  schemaVersion: 1,
  site: { name: { en: 'Test', zh: '测试' }, author: { en: 'Test', zh: '测试' }, copyrightText: { en: '', zh: '' }, lastUpdateDate: '2026-01-01' },
  profile: { name: { en: 'Test', zh: '测试' }, summary: { en: 'Summary', zh: '简介' } }, contacts: [], resume: {},
  education: [{ date: { start: '2020-01' }, position: { en: 'Education', zh: '教育' } }],
  workExperience: [{ date: { start: '2021-01' }, position: { en: 'Work', zh: '工作' } }],
  awards: [{ date: { start: '2022-01' }, title: { en: 'Award', zh: '奖项' } }], techStack: [],
  publications: { journalArticles: [{ title: { en: 'Hidden journal', zh: '隐藏论文' } }], conferencePapers: [] },
  timeline: [{ date: { start: '2025-01' }, title: { en: 'Timeline', zh: '时间线' }, description: { en: 'Event', zh: '事件' } }],
  layout: { homeFields: ['profile', 'timeline'], cvFields: ['profile', 'work experience', 'awards and scholarships', 'education'] },
};
const nav = '<nav><div class="nav-links"><a href="index.html#profile" data-i18n="nav.profile">Profile</a><a href="index.html#timeline" data-i18n="nav.timeline">Timeline</a><a href="pages/cv.html" data-i18n="nav.resume">CV</a></div><button class="lang-toggle" data-language="en"></button><button class="theme-toggle"></button><button class="menu-toggle"></button></nav>';
const home = `<!doctype html><link rel="stylesheet" href="assets/css/style.css"><body data-page="home">${nav}<main><section id="profile" class="intro profile-section"><div class="container"><h1 class="hero-title">Hello, I'm Test</h1><div class="hero-summary">Summary</div><div class="intro-actions"></div><div class="contact-links"></div></div></section><section id="timeline"><h2 data-i18n="timeline.title">Timeline</h2><div class="timeline-container"><div class="timeline-item">Timeline</div></div><button class="timeline-toggle"><span class="timeline-toggle-label"></span></button></section></main><script type="module" src="assets/js/app.js"></script>`;
const cv = `<!doctype html><link rel="stylesheet" href="../assets/css/style.css"><body data-page="resume">${nav.replaceAll('assets/', '../assets/')}<main><div class="resume-page"><div class="resume-layout"><aside class="resume-sidebar"><h2 class="resume-profile-name">Test</h2><div class="resume-download"></div><div class="resume-profile-details"><p>Summary</p></div><div class="resume-contact-links"></div></aside><div class="resume-main"><section><div class="resume-work">Work</div></section><section><div class="resume-awards">Award</div></section><section><div class="resume-education">Education</div></section></div></div></div></main><script type="module" src="assets/js/resume.js"></script>`;

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const noJsContext = await browser.newContext({ javaScriptEnabled: false });
    const noJs = await noJsContext.newPage();
    await noJs.route('**/layout-home.html', route => route.fulfill({ contentType: 'text/html', body: home }));
    await noJs.goto(`${origin}/layout-home.html`);
    ok(await noJs.locator('#timeline').count() === 1 && await noJs.locator('#projects, #publications').count() === 0, 'No-JS home layout contains hidden sections');
    await noJsContext.close();
    const page = await browser.newPage();
    await page.route('**/layout-home.html', route => route.fulfill({ contentType: 'text/html', body: home }));
    await page.route('**/pages/layout-cv.html', route => route.fulfill({ contentType: 'text/html', body: cv }));
    await page.route('**/assets/data/site.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify(site) }));
    await page.route('**/assets/data/projects.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify({ schemaVersion: 2, projects: [] }) }));
    await page.goto(`${origin}/layout-home.html`); await page.waitForLoadState('networkidle');
    ok(await page.locator('#timeline').count() === 1 && await page.locator('#projects, #publications').count() === 0, 'Hydrated home recreated hidden sections');
    ok(await page.locator('.nav-links a[href*="#projects"], .nav-links a[href*="#publications"]').count() === 0, 'Navigation links to hidden home sections');
    await page.locator('.lang-toggle').click(); await page.waitForTimeout(100);
    ok((await page.locator('#timeline').textContent()).includes('时间线') && await page.locator('#projects, #publications').count() === 0, 'Language switch changed hidden home layout');
    await page.goto(`${origin}/pages/layout-cv.html`); await page.waitForLoadState('networkidle');
    const classes = await page.locator('.resume-main > section').evaluateAll(nodes => nodes.map(node => node.querySelector('[class^="resume-"]').className));
    ok(JSON.stringify(classes) === JSON.stringify(['resume-work', 'resume-awards', 'resume-education']), `CV section order changed: ${JSON.stringify(classes)}`);
    ok(await page.locator('.resume-journals, .resume-conferences, .resume-skills').count() === 0 && await page.locator('.resume-sidebar').count() === 1, 'CV hydration recreated hidden section or removed profile');
    // Home already proves the language-switch hydration path; on CV the same
    // static containers are retained and absent ones are never created.
    console.log('Configurable page fields browser regression passed');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
