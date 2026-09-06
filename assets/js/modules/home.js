import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { fromRoot } from './paths.js';
import { loadProjects } from './project-data.js';
import { loadSiteData } from './site-data.js';

function localized(value) {
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
    const card = document.createElement('a');
    card.className = 'card';
    card.href = fromRoot(project.page);
    card.innerHTML = `
      <div class="project-thumbnail-wrapper">
        <img class="project-thumbnail" loading="lazy" decoding="async">
      </div>
      <div class="project-info">
        <h3></h3><p></p><div class="project-tags"></div><span class="project-link"></span>
      </div>`;
    const image = qs('.project-thumbnail', card);
    image.src = fromRoot(project.thumbnail.src);
    image.alt = project.thumbnail.alt?.[currentLanguage()] || content.title;
    qs('h3', card).textContent = content.title;
    qs('.project-info > p', card).textContent = content.summary;
    qs('.project-link', card).textContent = t('projects.viewDetail');
    const tags = qs('.project-tags', card);
    (project.tags || []).forEach((tag) => {
      const badge = document.createElement('span');
      badge.className = 'project-tag';
      badge.textContent = tag;
      tags.appendChild(badge);
    });
    grid.appendChild(card);
  });
}

function renderTimeline(events) {
  const container = qs('.timeline-container');
  if (!container) return;
  clear(container);
  [...events].reverse().forEach((event) => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = '<div class="timeline-dot"></div><span class="timeline-date"></span><div class="timeline-content"><h3></h3><p></p></div>';
    qs('.timeline-date', item).textContent = localized(event.date);
    qs('h3', item).textContent = localized(event.title);
    qs('p', item).textContent = localized(event.description);
    container.appendChild(item);
  });
}

function renderTechStack(groups) {
  const container = qs('.skills-wrapper');
  if (!container) return;
  clear(container);
  groups.forEach((group) => {
    const column = document.createElement('div');
    column.className = 'skill-category';
    const heading = document.createElement('h3');
    heading.textContent = localized(group.title);
    const list = document.createElement('div');
    list.className = 'skill-list';
    group.items.forEach((item) => {
      const badge = document.createElement('div');
      badge.className = 'skill-badge';
      const icon = document.createElement('i');
      icon.className = item.icon;
      badge.append(icon, document.createTextNode(` ${item.name}`));
      list.appendChild(badge);
    });
    column.append(heading, list);
    container.appendChild(column);
  });
}

function renderContacts(contacts) {
  const container = qs('.contact-links');
  if (!container) return;
  clear(container);
  contacts.forEach((contact) => {
    const item = document.createElement('div');
    item.className = 'contact-item';
    const link = document.createElement('a');
    link.href = contact.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    const icon = document.createElement('i');
    icon.className = contact.icon;
    const label = document.createElement('p');
    label.textContent = localized(contact.label);
    link.append(icon, label);
    item.appendChild(link);
    container.appendChild(item);
  });
}

async function renderHome() {
  const [, site] = await Promise.all([renderProjects(), loadSiteData()]);
  renderTimeline(site.timeline || []);
  renderTechStack(site.techStack || []);
  renderContacts(site.contacts || []);
}

export function initHome() {
  onLanguageChange(renderHome);
}
