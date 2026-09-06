import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { fromRoot } from './paths.js';
import { loadProjects } from './project-data.js';
import { CONTACT_LINKS, TECH_STACK, TIMELINE_EVENTS } from './site-data.js';

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

function renderTimeline() {
  const container = qs('.timeline-container');
  if (!container) return;
  clear(container);
  TIMELINE_EVENTS.forEach((key) => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = `<div class="timeline-dot"></div><span class="timeline-date">${t(`${key}.date`)}</span><div class="timeline-content"><h3>${t(`${key}.title`)}</h3><p>${t(`${key}.desc`)}</p></div>`;
    container.appendChild(item);
  });
}

function renderTechStack() {
  const container = qs('.skills-wrapper');
  if (!container) return;
  clear(container);
  TECH_STACK.forEach((group) => {
    const column = document.createElement('div');
    column.className = 'skill-category';
    column.innerHTML = `<h3>${t(group.category)}</h3><div class="skill-list">${group.items.map((item) => `<div class="skill-badge"><i class="${item.icon}"></i> ${item.name}</div>`).join('')}</div>`;
    container.appendChild(column);
  });
}

function renderContacts() {
  const container = qs('.contact-links');
  if (!container) return;
  clear(container);
  CONTACT_LINKS.forEach((contact) => {
    const item = document.createElement('div');
    item.className = 'contact-item';
    item.innerHTML = `<a href="${contact.link}" target="_blank" rel="noopener noreferrer"><i class="${contact.icon}"></i><p>${t(contact.key)}</p></a>`;
    container.appendChild(item);
  });
}

async function renderHome() {
  await renderProjects();
  renderTimeline();
  renderTechStack();
  renderContacts();
}

export function initHome() {
  onLanguageChange(renderHome);
}
