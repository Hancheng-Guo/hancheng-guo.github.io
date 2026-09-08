import { qs } from './dom.js';
import { t } from './i18n.js';

function updateThemeLabel(toggle, theme) {
  const label = String(t(theme === 'dark' ? 'nav.switchToLight' : 'nav.switchToDark'));
  toggle.setAttribute('aria-label', label);
  toggle.setAttribute('title', label);
}

export function initTheme() {
  const html = document.documentElement;
  const toggle = qs('.theme-toggle');
  const initialTheme = localStorage.getItem('theme') || html.dataset.theme || 'dark';

  html.dataset.theme = initialTheme;
  if (!toggle) return;
  updateThemeLabel(toggle, initialTheme);

  toggle.addEventListener('click', () => {
    const nextTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = nextTheme;
    localStorage.setItem('theme', nextTheme);
    updateThemeLabel(toggle, nextTheme);
  });
}
