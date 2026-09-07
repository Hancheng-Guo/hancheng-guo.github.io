import { clear, qs } from './dom.js';
import { formatDateRange } from './date.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { fromRoot } from './paths.js';
import { loadProjects } from './project-data.js';
import { applySiteIdentity, loadSiteData } from './site-data.js';
import { markdownText, renderInline } from './markdown.js';

function localized(value) {
  if (typeof value === 'string') return value;
  return value?.[currentLanguage()] ?? value?.en ?? '';
}

async function renderProjects() {
  const grid = qs('.projects-grid');
  if (!grid) return;
  grid.innerHTML = '<p class="status-view" role="status">' + t('projects.loading') + '</p>';
  let projects;
  try { projects = await loadProjects(); } catch (error) {
    grid.innerHTML = '<div class="status-view error-state" role="alert"><p>' + t('projects.loadError') + '</p><button class="control-btn" type="button">' + t('projects.retry') + '</button></div>';
    grid.querySelector('button')?.addEventListener('click', () => renderProjects());
    return;
  }
  projects = projects.filter((project) => project.status !== 'draft');
  if (!projects.length) { grid.innerHTML = '<p class="status-view">' + t('projects.empty') + '</p>'; return; }
  clear(grid);
  projects.forEach((project) => {
    const content = project.locales[currentLanguage()] || project.locales.en;
    const card = document.createElement('article');
    card.className = 'card';
    const projectUrl = fromRoot(project.page);
    card.tabIndex = 0;
    card.addEventListener('click', (event) => {
      if (!event.target.closest('a')) window.location.href = projectUrl;
    });
    card.addEventListener('keydown', (event) => {
      if ((event.key === 'Enter' || event.key === ' ') && !event.target.closest('a')) {
        event.preventDefault();
        window.location.href = projectUrl;
      }
    });
    card.innerHTML = `
      <div class="project-thumbnail-wrapper">
        <img class="project-thumbnail" loading="lazy" decoding="async">
      </div>
      <div class="project-info">
        <h3></h3><p></p><div class="project-tags"></div><a class="project-link"></a>
      </div>`;
    const image = qs('.project-thumbnail', card);
    image.src = fromRoot(project.thumbnail.src);
    image.alt = project.thumbnail.alt?.[currentLanguage()] || content.title;
    renderInline(qs('h3', card), content.title);
    renderInline(qs('.project-info > p', card), content.summary);
    renderInline(qs('.project-link', card), t('projects.viewDetail'));
    qs('.project-link', card).href = projectUrl;
    const tags = qs('.project-tags', card);
    (project.tags || []).forEach((tag) => {
      const badge = document.createElement('span');
      badge.className = 'project-tag';
      renderInline(badge, localized(tag));
      tags.appendChild(badge);
    });
    grid.appendChild(card);
  });
}

function renderTimeline(events) {
  const container = qs('.timeline-container');
  if (!container) return;
  clear(container);
  const ordered = [...events].reverse();
  ordered.forEach((event, index) => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = '<div class="timeline-dot"></div><div class="timeline-summary"><span class="timeline-date"></span><h3></h3></div><div class="timeline-content"><p></p></div>';
    qs('.timeline-date', item).textContent = formatDateRange(event.date);
    renderInline(qs('.timeline-summary h3', item), localized(event.title));
    renderInline(qs('p', item), localized(event.description));
    if (index >= 4) item.classList.add('timeline-extra');
    container.appendChild(item);
  });
  const toggle = qs('.timeline-toggle');
  if (toggle) {
    toggle.hidden = ordered.length <= 4;
    toggle.setAttribute('aria-expanded', 'false');
    renderInline(toggle, t('timeline.showMore'));
    toggle.onclick = () => { const expanded = toggle.getAttribute('aria-expanded') === 'true'; toggle.setAttribute('aria-expanded', String(!expanded)); renderInline(toggle, t(expanded ? 'timeline.showMore' : 'timeline.showLess')); container.classList.toggle('timeline-expanded', !expanded); };
  }
}

function renderContacts(contacts, profile = {}) {
  const container = qs('.contact-links');
  if (!container) return;
  clear(container);
  const email = localized(profile.email);
  if (email) {
    const item = document.createElement('div');
    item.className = 'contact-item email-contact-item';
    const link = document.createElement('a');
    link.className = 'email-contact-link';
    link.href = `mailto:${email}`;
    link.setAttribute('aria-label', email);
    const icon = document.createElement('span');
    icon.className = 'svg-icon icon-envelope';
    icon.setAttribute('aria-hidden', 'true');
    const label = document.createElement('span');
    label.textContent = email;
    link.append(icon, label);
    item.appendChild(link);
    container.appendChild(item);
  }
  const socialGroup = document.createElement('div');
  socialGroup.className = 'social-contact-group';
  contacts.forEach((contact) => {
    const item = document.createElement('div');
    item.className = 'contact-item';
    const link = document.createElement('a');
    link.href = contact.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', markdownText(localized(contact.label)));
    link.title = markdownText(localized(contact.label));
    const icon = document.createElement('span');
    icon.className = `svg-icon icon-${contact.icon}`;
    icon.setAttribute('aria-hidden', 'true');
    const label = document.createElement('span');
    label.className = 'visually-hidden';
    renderInline(label, localized(contact.label));
    link.append(icon, label);
    item.appendChild(link);
    socialGroup.appendChild(item);
  });
  if (socialGroup.childElementCount) container.appendChild(socialGroup);
}

function renderPortfolio(site) {
  applySiteIdentity(site);
  const profile = site.profile || {};
  const name = localized(profile.name);
  const title = qs('.hero-title');
  const summary = qs('.hero-summary');
  if (title && name) renderInline(title, t('intro.greeting').replace('{name}', name));
  if (summary && profile.summary) renderInline(summary, localized(profile.summary));

  const actions = qs('.intro-actions');
  if (!actions) return;
  clear(actions);
  const resume = site.resume || {};
  const resumeUrl = localized(resume.url);
  if (!resumeUrl) return;
  const link = document.createElement('a');
  link.className = 'publish-link primary-action';
  const external = /^https?:/.test(resumeUrl);
  link.href = external ? resumeUrl : fromRoot(resumeUrl);
  const icon = document.createElement('span');
  icon.className = 'svg-icon icon-file-pdf';
  icon.setAttribute('aria-hidden', 'true');
  const label = document.createElement('span');
  renderInline(label, localized(resume.label) || t('intro.downloadCv'));
  link.append(icon, label);
  if (external) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
  else if (resume.download !== false) link.setAttribute('download', '');
  actions.appendChild(link);
}
function renderPublicationEntries(selector, entries) {
  const container = qs(selector);
  if (!container) return;
  clear(container);
  (entries || []).forEach((entry) => {
    const item = document.createElement('article');
    item.className = 'content-entry';
    const heading = document.createElement('h3');
    renderInline(heading, localized(entry.title || entry));
    const detail = document.createElement('p');
    renderInline(detail, [formatDateRange(entry.date), localized(entry.venue)].filter(Boolean).join(' · '));
    item.append(heading, detail);
    container.appendChild(item);
  });
}

function renderPublications(site) {
  renderPublicationEntries('.home-journals', site.publications?.journalArticles);
  renderPublicationEntries('.home-conferences', site.publications?.conferencePapers);
}

async function renderHome() {
  let site;
  try { await renderProjects(); site = await loadSiteData(); } catch (error) {
    ['.timeline-container', '.contact-links'].forEach((selector) => { const element = qs(selector); if (element) element.innerHTML = `<p class="status-view error-state" role="alert">${t('projects.loadError')}</p>`; });
    return;
  }
  renderTimeline(site.timeline || []);
  renderPublications(site);
  renderPortfolio(site);
  renderContacts(site.contacts || [], site.profile || {});
}

export function initHome() {
  onLanguageChange(renderHome);
}
