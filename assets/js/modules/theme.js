import { qs } from './dom.js';

export function initTheme() {
  const html = document.documentElement;
  const toggle = qs('.theme-toggle');
  const initialTheme = localStorage.getItem('theme') || html.dataset.theme || 'dark';

  html.dataset.theme = initialTheme;
  if (!toggle) return;

  toggle.addEventListener('click', () => {
    const nextTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = nextTheme;
    localStorage.setItem('theme', nextTheme);
  });
}
