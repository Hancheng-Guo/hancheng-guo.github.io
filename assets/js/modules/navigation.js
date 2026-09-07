import { currentLanguage, changeLanguage } from './i18n.js';
import { qs, qsa } from './dom.js';

const NAVIGATION_OFFSET = 70;
const SCROLL_DURATION = 220;
let activeScrollAnimation = null;

function normalizedPathname(pathname) {
  return pathname.replace(/\/index\.html$/i, '/');
}

function sameDocument(targetUrl) {
  return targetUrl.origin === window.location.origin
    && normalizedPathname(targetUrl.pathname) === normalizedPathname(window.location.pathname)
    && targetUrl.search === window.location.search;
}

function targetTop(target) {
  return Math.max(0, target.getBoundingClientRect().top + window.scrollY - NAVIGATION_OFFSET);
}

function stopScrollAnimation() {
  if (activeScrollAnimation !== null) cancelAnimationFrame(activeScrollAnimation);
  activeScrollAnimation = null;
}

function scrollToTarget(target, reduced) {
  stopScrollAnimation();
  const destination = targetTop(target);
  if (reduced) { window.scrollTo(0, destination); return; }
  const start = window.scrollY;
  const distance = destination - start;
  if (Math.abs(distance) < 1) return;
  const startedAt = performance.now();
  const easeOutCubic = (progress) => 1 - ((1 - progress) ** 3);
  const step = (now) => {
    const progress = Math.min(1, (now - startedAt) / SCROLL_DURATION);
    window.scrollTo(0, start + distance * easeOutCubic(progress));
    if (progress < 1) activeScrollAnimation = requestAnimationFrame(step);
    else activeScrollAnimation = null;
  };
  activeScrollAnimation = requestAnimationFrame(step);
}

function prepareCrossDocumentAnchor(targetUrl) {
  try { sessionStorage.setItem('portfolio.pending-anchor', `${targetUrl.pathname}${targetUrl.search}${targetUrl.hash}`); } catch { /* Storage may be unavailable. */ }
}

export function revealInitialAnchor() {
  const root = document.documentElement;
  if (!root.dataset.anchorPending) return;
  const fragment = decodeURIComponent(window.location.hash.slice(1));
  const target = fragment && document.getElementById(fragment);
  let framesUntilReveal = 7;
  const settle = () => {
    if (target) window.scrollTo(0, targetTop(target));
    if (--framesUntilReveal > 0) { requestAnimationFrame(settle); return; }
    requestAnimationFrame(() => {
      if (target) window.scrollTo(0, targetTop(target));
      root.classList.add('anchor-ready');
      try { sessionStorage.removeItem('portfolio.pending-anchor'); } catch { /* no-op */ }
    });
  };
  requestAnimationFrame(settle);
}

export function initNavigation() {
  qs('.lang-toggle')?.addEventListener('click', () => changeLanguage(currentLanguage() === 'en' ? 'zh' : 'en'));
  const menuButton = qs('.menu-toggle');
  const navLinks = qs('.nav-links');
  const closeMenu = () => { navLinks?.classList.remove('is-open'); menuButton?.setAttribute('aria-expanded', 'false'); };

  qsa('a[href]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || anchor.hasAttribute('download')) return;
      const href = anchor.getAttribute('href');
      if (!href) return;
      let targetUrl;
      try { targetUrl = new URL(href, window.location.href); } catch { return; }
      if (!targetUrl.hash || targetUrl.origin !== window.location.origin) return;
      if (!sameDocument(targetUrl)) { prepareCrossDocumentAnchor(targetUrl); closeMenu(); return; }
      const target = qs(targetUrl.hash);
      if (!target) return;
      event.preventDefault();
      scrollToTarget(target, Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches));
      history.pushState(null, '', targetUrl.hash);
      closeMenu();
    });
  });
  menuButton?.addEventListener('click', () => {
    const open = navLinks?.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(Boolean(open)));
  });
  navLinks?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
}
