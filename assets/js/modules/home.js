import { clear, qs } from './dom.js';
import { formatDateRange } from './date.js';
import { currentLanguage, onLanguageChange, t } from './i18n.js';
import { fromRoot } from './paths.js';
import { loadProjects } from './project-data.js';
import { applySiteIdentity, loadSiteData } from './site-data.js';
import { markdownText, renderBlock, renderInline } from './markdown.js';

function linkChevron(direction) { const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); icon.setAttribute('class', `svg-icon svg-icon--inline motion-link-arrow link-chevron chevron-${direction}`); icon.setAttribute('aria-hidden', 'true'); icon.setAttribute('focusable', 'false'); icon.setAttribute('viewBox', '0 0 24 24'); icon.setAttribute('fill', 'none'); icon.setAttribute('stroke', 'currentColor'); icon.setAttribute('stroke-width', '3'); icon.setAttribute('stroke-linecap', 'round'); icon.setAttribute('stroke-linejoin', 'round'); const path = document.createElementNS('http://www.w3.org/2000/svg', 'path'); path.setAttribute('d', 'm6 9 6 6 6-6'); icon.appendChild(path); return icon; }

function localized(value) {
  if (typeof value === 'string') return value;
  return value?.[currentLanguage()] ?? value?.en ?? '';
}

async function renderProjects() {
  const grid = qs('.projects-grid');
  if (!grid) return;
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
    const hasDetailPage = project.hasDetailPage === true;
    if (hasDetailPage) {
      const projectUrl = fromRoot(project.page);
      card.classList.add('project-card-detail');
      card.tabIndex = 0;
      card.setAttribute('role', 'link');
      card.setAttribute('aria-label', `${t('projects.viewDetail')}: ${markdownText(content.title)}`);
      card.dataset.projectHref = projectUrl;
      card.addEventListener('click', (event) => {
        if (!event.target.closest('a')) window.location.href = projectUrl;
      });
      card.addEventListener('keydown', (event) => {
        if ((event.key === 'Enter' || event.key === ' ') && !event.target.closest('a')) {
          event.preventDefault();
          window.location.href = projectUrl;
        }
      });
    } else {
      // Match the static fallback: status-only cards are focusable for
      // reading/visual feedback, but have no link semantics or navigation.
      card.classList.add('project-card-coming-soon');
      card.tabIndex = 0;
    }
    card.innerHTML = `
      <div class="project-thumbnail-wrapper">
        <img class="project-thumbnail" loading="lazy" decoding="async">
      </div>
      <div class="project-info">
        <div class="project-copy"><h3></h3><p class="project-summary"></p></div><div class="project-meta"><div class="project-tags"></div><div class="project-card-footer"><span class="project-link"></span><time class="project-date"></time></div></div>
      </div>`;
    const image = qs('.project-thumbnail', card);
    image.src = fromRoot(project.thumbnail.src);
    image.alt = markdownText(project.thumbnail.alt?.[currentLanguage()] || content.title);
    renderInline(qs('h3', card), content.title);
    renderInline(qs('.project-summary', card), content.summary);
    // Keep the static fallback and hydrated DOM structurally identical so the
    // footer cannot reflow while project data is loading.
    const date = qs('.project-date', card); date.textContent = project.date ? formatDateRange(project.date) : ''; date.hidden = !project.date;
    const detailCue = qs('.project-link', card);
    if (hasDetailPage) {
      renderInline(detailCue, t('projects.viewDetail'));
      detailCue.appendChild(linkChevron('right'));
    } else {
      detailCue.classList.add('project-status');
      renderInline(detailCue, t('projects.detailComingSoon'));
    }
    const tags = qs('.project-tags', card);
    (project.tags || []).forEach((tag) => {
      const badge = document.createElement('span');
      badge.className = 'project-tag';
      renderInline(badge, localized(tag));
      tags.appendChild(badge);
    });
    // The overlay is useful only when the three-line compact treatment has
    // actually hidden content.  Short summaries must remain bit-for-bit in
    // their normal layout on hover and focus.
    const syncCopyOffset = () => {
      const info = qs('.project-info', card);
      const summary = qs('.project-summary', card);
      const copy = qs('.project-copy', card);
      card.classList.remove('project-card-enhanced');
      card.classList.remove('project-card-expandable');
      const tagsTop = tags.getBoundingClientRect().top;
      const infoBottom = info.getBoundingClientRect().bottom;
      card.style.setProperty('--project-info-base-height', `${info.getBoundingClientRect().height}px`);
      card.style.setProperty('--project-copy-active-bottom', `${Math.max(0, infoBottom - tagsTop)}px`);
      // scrollHeight is measured while the normal three-line clamp is active.
      // A small tolerance avoids a false positive from fractional line metrics.
      const expandable = summary.scrollHeight > summary.clientHeight + 1;
      card.classList.toggle('project-card-expandable', expandable);
      if (!expandable) {
        info.style.setProperty('--project-thumbnail-fade-height', '0px');
        info.style.setProperty('--project-thumbnail-fade-solid-stop', '0px');
        return;
      }

      // Measure the copy as it will appear after expansion without changing
      // the card's compact geometry.  The resulting fade is deliberately
      // per-card: longer wrapped summaries reach farther into the thumbnail,
      // and become fully card-coloured just before their first glyph.
      const previousClamp = summary.style.webkitLineClamp;
      const previousOverflow = summary.style.overflow;
      summary.style.webkitLineClamp = 'unset';
      summary.style.overflow = 'visible';
      const expandedCopyHeight = copy.getBoundingClientRect().height;
      summary.style.webkitLineClamp = previousClamp;
      summary.style.overflow = previousOverflow;

      const copyTopWhenExpanded = info.getBoundingClientRect().height
        - Math.max(0, infoBottom - tagsTop) - expandedCopyHeight;
      // Keep a twenty-pixel fully opaque safety margin above text.  Even when
      // the expanded copy fits below the thumbnail, the image edge itself is
      // solid card colour so its old border cannot be distinguished.
      const solidSurfaceY = Math.min(0, copyTopWhenExpanded - 20);
      const fadeHeight = Math.max(64, -solidSurfaceY + 64);
      const solidStop = fadeHeight + solidSurfaceY;
      info.style.setProperty('--project-thumbnail-fade-height', `${fadeHeight}px`);
      info.style.setProperty('--project-thumbnail-fade-solid-stop', `${solidStop}px`);
      card.classList.add('project-card-enhanced');
    };
    grid.appendChild(card);
    syncCopyOffset();
    // Observe the thumbnail wrapper rather than the card itself: changing the
    // enhancement class can affect card descendants, whereas wrapper width is
    // the input that determines text wrapping. This prevents observer loops.
    if ('ResizeObserver' in window) {
      new ResizeObserver(syncCopyOffset).observe(qs('.project-thumbnail-wrapper', card));
    } else {
      window.addEventListener('resize', syncCopyOffset, { passive: true });
    }
    document.fonts?.ready?.then(syncCopyOffset);
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
    item.innerHTML = '<div class="timeline-dot"></div><div class="timeline-summary"><span class="timeline-date"></span><h3></h3></div><div class="timeline-content markdown-body"></div>';
    qs('.timeline-date', item).textContent = formatDateRange(event.date);
    renderInline(qs('.timeline-summary h3', item), localized(event.title));
    renderBlock(qs('.timeline-content', item), localized(event.description));
    if (index >= 8) item.classList.add('timeline-extra');
    container.appendChild(item);
  });
  const toggle = qs('.timeline-toggle');
  if (toggle) {
    toggle.hidden = ordered.length <= 8;
    toggle.setAttribute('aria-expanded', 'false');
    const label = qs('.timeline-toggle-label', toggle);
    renderInline(label || toggle, t('timeline.showMore'));
    toggle.onclick = () => { const expanded = toggle.getAttribute('aria-expanded') === 'true'; toggle.setAttribute('aria-expanded', String(!expanded)); renderInline(label || toggle, t(expanded ? 'timeline.showMore' : 'timeline.showLess')); container.classList.toggle('timeline-expanded', !expanded); };
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

function renderProfile(site) {
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
  (entries || []).filter((entry) => entry.status !== 'draft').forEach((entry) => {
    const item = document.createElement('article');
    item.className = 'content-entry';
    const heading = document.createElement('h3');
    renderInline(heading, localized(entry.title || entry));
    const detail = document.createElement('p');
    const dateText = formatDateRange(entry.date);
    const venueText = localized(entry.venue);
    if (dateText) {
      const date = document.createElement('time');
      date.className = 'entry-date';
      date.textContent = dateText;
      detail.appendChild(date);
    }
    if (dateText && venueText) {
      const separator = document.createElement('span');
      separator.className = 'entry-separator';
      separator.textContent = ' · ';
      detail.appendChild(separator);
    }
    if (venueText) {
      const venue = document.createElement('span');
      venue.className = 'entry-detail';
      renderInline(venue, venueText);
      detail.appendChild(venue);
    }
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
  renderProfile(site);
  renderContacts(site.contacts || [], site.profile || {});
}

export function initHome() {
  onLanguageChange(renderHome);
}
