import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { fromRoot } from './paths.js';
import { loadProjects } from './project-data.js';
import { CONTACT_LINKS, TECH_STACK, TIMELINE_EVENTS } from './site-data.js';

function renderTags(tags, className) {
  return tags.map((tag) => `<span class="${className}">${tag}</span>`).join('');
}

async function renderProjects() {
  const grid = qs('.projects-grid');
  if (!grid) return;
  clear(grid);

  const projects = await loadProjects();
  projects.forEach((project) => {
    const content = project.locales[currentLanguage()] || project.locales.en;
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div class="project-thumbnail-wrapper">
        <img src="${fromRoot(project.thumbnail)}" alt="${t('projects.imgAlt')}" class="project-thumbnail">
      </div>
      <div class="project-info">
        <h3>${content.title}</h3>
        <p>${content.summary}</p>
        <div class="project-tags">${renderTags(content.tags, 'project-tag')}</div>
        <a href="${fromRoot(project.page)}" class="project-link">${t('projects.viewDetail')}</a>
      </div>`;
    card.addEventListener('click', () => { window.location.href = fromRoot(project.page); });
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
