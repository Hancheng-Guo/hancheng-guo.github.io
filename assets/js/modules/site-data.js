import { fromRoot } from './paths.js';
import { currentLanguage } from './i18n.js';
import { formatFullDate } from './date.js';
import { markdownText, renderInline } from './markdown.js';

let cachedSiteData;

export async function loadSiteData() {
  if (!cachedSiteData) {
    const response = await fetch(fromRoot('assets/data/site.json'));
    if (!response.ok) throw new Error(`Unable to load site data (${response.status})`);
    cachedSiteData = await response.json();
  }
  return cachedSiteData;
}

function localized(value) {
  if (typeof value === 'string') return value;
  return value?.[currentLanguage()] ?? value?.en ?? '';
}

export function applySiteIdentity(site, pageTitle = '') {
  const siteName = localized(site?.site?.name) || 'Portfolio';
  const author = localized(site?.site?.author) || siteName;
  const plainSiteName = markdownText(siteName);
  document.title = pageTitle ? `${markdownText(pageTitle)} - ${plainSiteName}` : plainSiteName;
  document.querySelectorAll('.logo-text').forEach((element) => renderInline(element, author));

  const lastUpdateDate = site?.site?.lastUpdateDate ?? '';
  const copyrightText = localized(site?.site?.copyrightText);
  const copyrightSuffix = copyrightText ? `, ${copyrightText}` : '';
  const copyrightLine = `© ${lastUpdateDate.slice(0, 4)} ${author}${copyrightSuffix}`;
  const formattedDate = formatFullDate(lastUpdateDate);
  const updatedLine = currentLanguage() === 'zh'
    ? `网站最后更新于 ${formattedDate}`
    : `Site last updated ${formattedDate}`;
  document.querySelectorAll('footer').forEach((footer) => {
    const copyright = footer.querySelector('.footer-copyright');
    const updated = footer.querySelector('.footer-updated');
    if (copyright) renderInline(copyright, copyrightLine);
    if (updated) updated.textContent = updatedLine;
  });
  return siteName;
}
