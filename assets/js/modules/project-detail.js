import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { initLightbox } from './lightbox.js';
import { fromRoot } from './paths.js';
import { loadProject } from './project-data.js';

const LINK_PRESENTATION = {
  github: { icon: 'fab fa-github', className: 'github' },
  techDoc: { icon: 'fas fa-file-pdf', className: '' },
  demo: { icon: 'fab fa-bilibili', className: 'bilibili' },
};

function createLink(link) {
  const presentation = LINK_PRESENTATION[link.type];
  if (!presentation || !/^https:\/\//.test(link.url || '')) return null;
  const anchor = document.createElement('a');
  anchor.href = link.url;
  anchor.target = '_blank';
  anchor.rel = 'noopener noreferrer';
  anchor.className = `publish-link ${presentation.className}`;
  const icon = document.createElement('i');
  icon.className = presentation.icon;
  icon.setAttribute('aria-hidden', 'true');
  const label = document.createElement('span');
  label.textContent = t(`projectLinks.${link.type}`);
  anchor.append(icon, ' ', label);
  return anchor;
}

function renderLinks(container, links = []) {
  const wrapper = document.createElement('div');
  const list = document.createElement('div');
  wrapper.className = 'publish-links-wrapper';
  list.className = 'publish-links';
  links.map(createLink).filter(Boolean).forEach((link) => list.appendChild(link));
  if (list.childElementCount) {
    wrapper.appendChild(list);
    container.appendChild(wrapper);
  }
}

function renderBlocks(container, blocks = []) {
  blocks.forEach((block) => {
    if (!block || typeof block !== 'object') return;
    const type = block.type;
    if (type === 'heading') {
      const heading = document.createElement(`h${Math.min(6, Math.max(2, Number(block.level) || 2))}`);
      heading.textContent = block.text || ''; container.appendChild(heading);
    } else if (type === 'paragraph') {
      String(block.text || '').split(/\n{2,}/).filter(Boolean).forEach((text) => {
        const paragraph = document.createElement('p');
        paragraph.className = 'project-detail-desc';
        paragraph.textContent = text;
        container.appendChild(paragraph);
      });
    } else if (type === 'image') {
      const image = document.createElement('img'); image.className = 'project-img'; image.src = fromRoot(block.src || ''); image.alt = block.alt || ''; image.loading = 'lazy'; image.decoding = 'async'; container.appendChild(image);
    } else if (type === 'gallery') {
      const gallery = document.createElement('div'); gallery.className = 'project-gallery';
      (block.images || []).forEach((item) => { const image = document.createElement('img'); image.className = 'project-img'; image.src = fromRoot(item.src || ''); image.alt = item.alt || ''; image.loading = 'lazy'; gallery.appendChild(image); });
      container.appendChild(gallery);
    } else if (type === 'list') {
      const list = document.createElement(block.ordered ? 'ol' : 'ul'); (block.items || []).forEach((item) => { const li = document.createElement('li'); li.textContent = item || ''; list.appendChild(li); }); container.appendChild(list);
    } else if (type === 'quote') {
      const quote = document.createElement('blockquote'); quote.textContent = block.text || ''; if (block.source) quote.setAttribute('cite', block.source); container.appendChild(quote);
    } else if (type === 'metrics') {
      const metrics = document.createElement('dl'); metrics.className = 'project-metrics'; (block.items || []).forEach((item) => { const dt = document.createElement('dt'); dt.textContent = item.label || ''; const dd = document.createElement('dd'); dd.textContent = item.value || ''; metrics.append(dt, dd); }); container.appendChild(metrics);
    } else if (type === 'video' && /^https:\/\//.test(block.url || '')) {
      const link = document.createElement('a'); link.href = block.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = block.title || block.url; container.appendChild(link);
    }
  });
}
function updateMeta(content, project) {
  document.title = `${content.title} - Lain-Ego`;
  let description = document.querySelector('meta[name="description"]');
  if (!description) { description = document.createElement('meta'); description.name = 'description'; document.head.appendChild(description); }
  description.content = content.summary || '';
  let ogTitle = document.querySelector('meta[property="og:title"]');
  if (!ogTitle) { ogTitle = document.createElement('meta'); ogTitle.setAttribute('property', 'og:title'); document.head.appendChild(ogTitle); }
  ogTitle.content = content.title;
  let ogDescription = document.querySelector('meta[property="og:description"]');
  if (!ogDescription) { ogDescription = document.createElement('meta'); ogDescription.setAttribute('property', 'og:description'); document.head.appendChild(ogDescription); }
  ogDescription.content = content.summary || '';
  const canonicalUrl = new URL(window.location.href);
  canonicalUrl.hash = '';
  let canonical = document.querySelector('link[rel="canonical"]');
  if (!canonical) { canonical = document.createElement('link'); canonical.rel = 'canonical'; document.head.appendChild(canonical); }
  canonical.href = canonicalUrl.href;
  for (const [property, value] of [['og:url', canonicalUrl.href], ['og:image', fromRoot(project.thumbnail.src)]]) {
    let meta = document.querySelector(`meta[property="${property}"]`);
    if (!meta) { meta = document.createElement('meta'); meta.setAttribute('property', property); document.head.appendChild(meta); }
    meta.content = value;
  }
}

async function renderProject() {
  const container = qs('.project-container');
  const id = document.body.dataset.projectId || new URLSearchParams(window.location.search).get('id');
  if (!container || !id) return;

  container.innerHTML = '<p class="status-view" role="status">' + t('projects.loading') + '</p>';
  let project;
  try { project = await loadProject(id); } catch (error) {
    container.innerHTML = '<div class="status-view error-state" role="alert"><p>' + t('projects.loadError') + '</p><button class="control-btn retry-button" type="button">' + t('projects.retry') + '</button></div>';
    container.querySelector('.retry-button')?.addEventListener('click', renderProject);
    return;
  }
  if (!project) {
    container.innerHTML = `<h2>${t('projects.notFound')}</h2>`;
    return;
  }

  const content = project.locales[currentLanguage()] || project.locales.en;
  clear(container);
  const backLink = document.createElement('a');
  backLink.className = 'back-link';
  backLink.href = fromRoot('index.html#projects');
  backLink.textContent = `← ${t('projects.back')}`;
  container.appendChild(backLink);
  if (project.status === 'draft') {
    const notice = document.createElement('p');
    notice.className = 'status-view draft-notice';
    notice.setAttribute('role', 'status');
    notice.textContent = t('projects.draft');
    container.appendChild(notice);
  }
  updateMeta(content, project);
  const title = document.createElement('h2');
  title.textContent = content.title;
  container.appendChild(title);
  renderBlocks(container, content.blocks);
  renderLinks(container, project.links);
  initLightbox(container);
}

export function initProjectDetail() {
  onLanguageChange(renderProject);
}
