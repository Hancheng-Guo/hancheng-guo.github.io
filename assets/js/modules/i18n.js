import { fromRoot } from './paths.js';
import { markdownInline } from './markdown.js';

let language = localStorage.getItem('lang') || 'en';
let messages = {};
const listeners = new Set();

function nestedValue(object, key) {
  return key.split('.').reduce((value, part) => value?.[part], object);
}

export function t(key) {
  return nestedValue(messages, key) ?? key;
}

export function currentLanguage() {
  return language;
}

export function renderMarkdown(value) {
  const values = Array.isArray(value) ? value : [value];
  return values.map((item) => markdownInline(item)).join('');
}

function translatePage() {
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const value = t(element.dataset.i18n);
    if (value === element.dataset.i18n) return;

    if (element instanceof HTMLImageElement) {
      element.alt = String(value);
    } else {
      element.innerHTML = renderMarkdown(value);
    }
  });

  document.querySelectorAll('[data-i18n-aria-label]').forEach((element) => {
    const key = element.dataset.i18nAriaLabel;
    const value = t(key);
    if (value !== key) element.setAttribute('aria-label', String(value));
  });

  const toggle = document.querySelector('.lang-toggle');
  if (toggle) {
    toggle.dataset.language = language;
    const label = String(t(language === 'en' ? 'nav.switchToChinese' : 'nav.switchToEnglish'));
    toggle.setAttribute('aria-label', label);
    toggle.setAttribute('title', label);
    const hidden = toggle.querySelector('.visually-hidden');
    if (hidden) hidden.textContent = label;
    const icon = toggle.querySelector('.language-target-icon');
    if (icon) icon.src = fromRoot(`assets/icons/language-switch-${language === 'zh' ? 'en' : 'ch'}.svg`);
  }
  const theme = document.querySelector('.theme-toggle');
  if (theme) {
    const dark = document.documentElement.dataset.theme === 'dark';
    const label = String(t(dark ? 'nav.switchToLight' : 'nav.switchToDark'));
    theme.setAttribute('aria-label', label);
    theme.setAttribute('title', label);
  }
}

async function loadLanguage(nextLanguage) {
  const response = await fetch(fromRoot(`lang/${nextLanguage}.json`));
  if (!response.ok) throw new Error(`Unable to load language: ${nextLanguage}`);
  messages = await response.json();
  translatePage();
  await Promise.all([...listeners].map((listener) => listener(nextLanguage)));
}

export async function initLanguage() {
  try {
    await loadLanguage(language);
  } catch (error) {
    console.error('[i18n] Load failed:', error);
  }
}

export async function changeLanguage(nextLanguage) {
  if (nextLanguage === language) return;
  language = nextLanguage;
  localStorage.setItem('lang', language);
  await loadLanguage(language);
}

export function onLanguageChange(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}
