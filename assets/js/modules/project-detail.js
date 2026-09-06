import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, renderMarkdown, t } from './i18n.js';
import { initLightbox } from './lightbox.js';
import { fromRoot } from './paths.js';
import { loadProject } from './project-data.js';

const LINK_PRESENTATION = {
  github: { icon: 'fab fa-github', className: 'github' },
  techDoc: { icon: 'fas fa-file-pdf', className: '' },
  demo: { icon: 'fab fa-bilibili', className: 'bilibili' },
};

function renderLink(link) {
  const presentation = LINK_PRESENTATION[link.type];
  const attributes = link.url ? `href="${link.url}" target="_blank" rel="noopener noreferrer"` : 'aria-disabled="true"';
  return `<a ${attributes} class="publish-link ${presentation.className}"><i class="${presentation.icon}"></i> <span>${t(`projectLinks.${link.type}`)}</span></a>`;
}

async function renderProject() {
  const container = qs('.project-container');
  const id = document.body.dataset.projectId;
  if (!container || !id) return;

  const project = await loadProject(id);
  if (!project) {
    container.innerHTML = `<h2>${t('projects.notFound')}</h2>`;
    return;
  }

  const content = project.locales[currentLanguage()] || project.locales.en;
  clear(container);
  document.title = `${content.title} - Lain-Ego`;
  container.insertAdjacentHTML('beforeend', `<h2>${content.title}</h2>`);

  project.gallery.forEach((image, index) => {
    if (index === 1 && content.sections[1]?.heading) {
      container.insertAdjacentHTML('beforeend', `<h3>${renderMarkdown(content.sections[1].heading)}</h3><div class="project-detail-desc">${renderMarkdown(content.sections[1].body)}</div>`);
    }

    if (index === 0) {
      const width = project.imageWidth ? ` style="--img-width:${project.imageWidth};"` : '';
      container.insertAdjacentHTML('beforeend', `<img src="${fromRoot(image)}" alt="${t(`projectImages.${index}`)}" class="project-img"${width}>`);
      container.insertAdjacentHTML('beforeend', `<div class="project-detail-desc">${renderMarkdown(content.sections[0]?.body || '')}</div>`);
    } else {
      container.insertAdjacentHTML('beforeend', `<img src="${fromRoot(image)}" alt="${t(`projectImages.${index}`)}" class="project-img">`);
    }
  });

  container.insertAdjacentHTML('beforeend', `<div class="publish-links-wrapper"><div class="publish-links">${project.links.map(renderLink).join('')}</div></div>`);
  initLightbox(container);
}

export function initProjectDetail() {
  onLanguageChange(renderProject);
}
