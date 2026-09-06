import { currentLanguage, changeLanguage } from './i18n.js';
import { qs, qsa } from './dom.js';

export function initNavigation() {
  qs('.lang-toggle')?.addEventListener('click', () => {
    changeLanguage(currentLanguage() === 'en' ? 'zh' : 'en');
  });

  qsa('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
      const href = anchor.getAttribute('href');
      if (!href || href === '#') return;
      const target = qs(href);
      if (!target) return;
      event.preventDefault();
      window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
    });
  });
}
