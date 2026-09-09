const { chromium } = require('playwright');

const origin = process.env.PORTFOLIO_TEST_ORIGIN || 'http://127.0.0.1:8765';
const executablePath = process.env.PORTFOLIO_BROWSER;
const ok = (value, message) => { if (!value) throw new Error(message); };

async function captureThemeFrames(page, count = 32) {
  return page.locator('.intro').evaluate((intro, frameCount) => new Promise((resolve) => {
    const frames = [];
    const sample = () => {
      frames.push({
        body: getComputedStyle(document.body).backgroundColor,
        intro: getComputedStyle(intro).backgroundColor,
        fade: getComputedStyle(intro).getPropertyValue('--hero-fade-color').trim(),
        pseudoFade: getComputedStyle(intro, '::after').getPropertyValue('--hero-fade-color').trim(),
      });
      if (frames.length < frameCount) requestAnimationFrame(sample);
      else resolve(frames);
    };
    requestAnimationFrame(sample);
  }), count);
}

async function assertThemeSync(page, label) {
  const bodyTransition = await page.locator('body').evaluate((body) => getComputedStyle(body).transition);
  ok(bodyTransition.includes('background-color 0.4s'), `${label}: anchor reveal replaced the page theme transition: ${bodyTransition}`);
  const framesPromise = captureThemeFrames(page);
  await page.locator('.theme-toggle').click();
  const frames = await framesPromise;
  for (const frame of frames) {
    ok(frame.body === frame.intro && frame.body === frame.fade && frame.body === frame.pseudoFade,
      `${label}: profile background lost theme synchronization: ${JSON.stringify(frames)}`);
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();

    await page.goto(`${origin}/index.html#profile`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(450);
    await assertThemeSync(page, 'Initial hash Profile');

    await page.goto(`${origin}/index.html#projects`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(450);
    await assertThemeSync(page, 'Initial non-Profile hash');

    await page.goto(`${origin}/pages/cv.html`);
    await page.waitForLoadState('networkidle');
    await Promise.all([
      page.waitForURL('**/index.html#profile'),
      page.locator('.nav-links a[href="../index.html#profile"]').click(),
    ]);
    await page.waitForTimeout(450);
    await assertThemeSync(page, 'Initial CV to Profile');

    await page.goto(`${origin}/index.html`);
    await page.waitForLoadState('networkidle');
    await Promise.all([
      page.waitForURL('**/pages/cv.html'),
      page.locator('.nav-links a[href="pages/cv.html"]').click(),
    ]);
    await Promise.all([
      page.waitForURL('**/index.html#profile'),
      page.locator('.nav-links a[href="../index.html#profile"]').click(),
    ]);
    await page.waitForTimeout(450);
    await assertThemeSync(page, 'Home to CV to Profile');

    await context.close();
    console.log('Profile theme synchronization passed: hash and CV navigation paths.');
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
