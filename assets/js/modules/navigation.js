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
  const menuButton = qs('.menu-toggle');
  const navLinks = qs('.nav-links');
  menuButton?.addEventListener('click', () => {
    const open = navLinks?.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(Boolean(open)));
  });
  const closeMenu = () => { navLinks?.classList.remove('is-open'); menuButton?.setAttribute('aria-expanded', 'false'); };
  navLinks?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
}
