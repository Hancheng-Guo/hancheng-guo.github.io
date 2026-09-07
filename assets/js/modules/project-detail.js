import { clear, qs } from './dom.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { initLightbox } from './lightbox.js';
import { fromRoot } from './paths.js';
import { loadProject, loadProjects } from './project-data.js';
import { applySiteIdentity, loadSiteData } from './site-data.js';
import { markdownText, renderBlock, renderInline } from './markdown.js';

const LINK_PRESENTATION = {
  github: { icon: 'github', className: 'github' },
  techDoc: { icon: 'file-pdf', className: '' },
  bilibili: { icon: 'bilibili', className: 'bilibili' },
  youtube: { icon: 'youtube', className: 'youtube' },
};

function createLink(link) {
  const presentation = LINK_PRESENTATION[link.type];
  if (!presentation || !/^https:\/\//.test(link.url || '')) return null;
  const anchor = document.createElement('a');
  anchor.href = link.url;
  anchor.target = '_blank';
  anchor.rel = 'noopener noreferrer';
  anchor.className = `publish-link ${presentation.className}`;
  const icon = document.createElement('span');
  icon.className = `svg-icon icon-${presentation.icon}`;
  icon.setAttribute('aria-hidden', 'true');
  const label = document.createElement('span');
  const customLabel = typeof link.label === 'string'
    ? link.label
    : link.label?.[currentLanguage()] ?? link.label?.en;
  renderInline(label, customLabel || t(`projectLinks.${link.type}`));
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
      renderInline(heading, block.text || ''); container.appendChild(heading);
    } else if (type === 'paragraph') {
      const content = document.createElement('div');
      content.className = 'project-detail-desc markdown-body';
      renderBlock(content, block.text || '');
      container.appendChild(content);
    } else if (type === 'image') {
      const figure = document.createElement('figure');
      const image = document.createElement('img'); image.className = 'project-img'; image.src = fromRoot(block.src || ''); image.alt = markdownText(block.alt || ''); image.loading = 'lazy'; image.decoding = 'async'; figure.appendChild(image);
      if (block.caption) { const caption = document.createElement('figcaption'); renderInline(caption, block.caption); figure.appendChild(caption); }
      container.appendChild(figure);
    } else if (type === 'gallery') {
      const gallery = document.createElement('div'); gallery.className = 'project-gallery';
      (block.images || []).forEach((item) => { const figure = document.createElement('figure'); const image = document.createElement('img'); image.className = 'project-img'; image.src = fromRoot(item.src || ''); image.alt = markdownText(item.alt || ''); image.loading = 'lazy'; figure.appendChild(image); if (item.caption) { const caption = document.createElement('figcaption'); renderInline(caption, item.caption); figure.appendChild(caption); } gallery.appendChild(figure); });
      container.appendChild(gallery);
    } else if (type === 'list') {
      const list = document.createElement(block.ordered ? 'ol' : 'ul'); (block.items || []).forEach((item) => { const li = document.createElement('li'); renderInline(li, item || ''); list.appendChild(li); }); container.appendChild(list);
    } else if (type === 'quote') {
      const quote = document.createElement('blockquote');
      renderBlock(quote, block.text || '');
      if (block.source) { const source = document.createElement('cite'); renderInline(source, block.source); quote.appendChild(source); }
      container.appendChild(quote);
    } else if (type === 'metrics') {
      const metrics = document.createElement('dl'); metrics.className = 'project-metrics'; (block.items || []).forEach((item) => { const dt = document.createElement('dt'); renderInline(dt, item.label || ''); const dd = document.createElement('dd'); renderInline(dd, item.value || ''); metrics.append(dt, dd); }); container.appendChild(metrics);
    } else if (type === 'video' && /^https:\/\//.test(block.url || '')) {
      const link = document.createElement('a'); link.href = block.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; renderInline(link, block.title || block.url); container.appendChild(link);
    }
  });
}
function updateMeta(content, project, site) {
  applySiteIdentity(site, content.title);
  let description = document.querySelector('meta[name="description"]');
  if (!description) { description = document.createElement('meta'); description.name = 'description'; document.head.appendChild(description); }
  description.content = markdownText(content.summary || '');
  let ogTitle = document.querySelector('meta[property="og:title"]');
  if (!ogTitle) { ogTitle = document.createElement('meta'); ogTitle.setAttribute('property', 'og:title'); document.head.appendChild(ogTitle); }
  ogTitle.content = markdownText(content.title);
  let ogDescription = document.querySelector('meta[property="og:description"]');
  if (!ogDescription) { ogDescription = document.createElement('meta'); ogDescription.setAttribute('property', 'og:description'); document.head.appendChild(ogDescription); }
  ogDescription.content = markdownText(content.summary || '');
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

  let project;
  let site;
  try { [project, site] = await Promise.all([loadProject(id), loadSiteData()]); } catch (error) {
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
  renderInline(backLink, `&lt; ${t('projects.back')}`);
  container.appendChild(backLink);
  if (project.status === 'draft') {
    const notice = document.createElement('p');
    notice.className = 'status-view draft-notice';
    notice.setAttribute('role', 'status');
    renderInline(notice, t('projects.draft'));
    container.appendChild(notice);
  }
  updateMeta(content, project, site);
  const title = document.createElement('h2');
  renderInline(title, content.title);
  container.appendChild(title);
  renderBlocks(container, content.blocks);
  renderLinks(container, project.links);
  initLightbox(container);
  const projects = (await loadProjects()).filter((item) => item.status !== 'draft');
  const position = projects.findIndex((item) => item.id === id);
  const adjacent = document.createElement('nav');
  adjacent.className = 'project-adjacent';
  adjacent.setAttribute('aria-label', t('projects.navigation'));
  [[position > 0, `< ${t('projects.previous')}`, position - 1, 'previous'], [position >= 0 && position < projects.length - 1, `${t('projects.next')} >`, position + 1, 'next']].forEach(([show, label, index, direction]) => {
    if (!show) return;
    const link = document.createElement('a');
    link.className = `project-adjacent-link ${direction}`;
    link.href = fromRoot(projects[index].page);
    const directionLabel = document.createElement('span');
    directionLabel.className = 'project-adjacent-label';
    renderInline(directionLabel, label.replace('<', '&lt;'));
    const projectName = document.createElement('span');
    projectName.className = 'project-adjacent-name';
    renderInline(projectName, projects[index].locales[currentLanguage()]?.title || projects[index].locales.en.title);
    link.append(directionLabel, projectName);
    adjacent.appendChild(link);
  });
  if (adjacent.childElementCount) container.appendChild(adjacent);
}

export function initProjectDetail() {
  onLanguageChange(renderProject);
}
