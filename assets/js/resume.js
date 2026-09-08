import { clear, qs } from './modules/dom.js';
import { formatDateRange } from './modules/date.js';
import { currentLanguage, initLanguage, onLanguageChange, t } from './modules/i18n.js';
import { initNavigation, revealInitialAnchor } from './modules/navigation.js';
import { applySiteIdentity, loadSiteData } from './modules/site-data.js';
import { initTheme } from './modules/theme.js';
import { markdownText, renderInline } from './modules/markdown.js';
import { fromRoot } from './modules/paths.js';

function localized(value) {
  if (typeof value === 'string') return value;
  return value?.[currentLanguage()] ?? value?.en ?? '';
}

function renderEntries(selector, entries, fields) {
  const container = qs(selector);
  if (!container) return;
  clear(container);
  entries.filter((entry) => entry.status !== 'draft').forEach((entry) => {
    const card = document.createElement('article');
    card.className = 'content-entry';
    const heading = document.createElement('h3');
    renderInline(heading, localized(entry[fields[0]]) || t('content.placeholder'));
    const detail = document.createElement('p');
    const values = [];
    const dateText = formatDateRange(entry.date);
    if (dateText) values.push({ value: dateText, date: true });
    fields.slice(1).forEach((field) => {
      const value = localized(entry[field]);
      if (value) values.push({ value, date: false });
    });
    values.forEach((part, index) => {
      if (index) {
        const separator = document.createElement('span');
        separator.className = 'entry-separator';
        separator.textContent = ' · ';
        detail.appendChild(separator);
      }
      const element = document.createElement(part.date ? 'time' : 'span');
      element.className = part.date ? 'entry-date' : 'entry-detail';
      if (part.date) element.textContent = part.value;
      else renderInline(element, part.value);
      detail.appendChild(element);
    });
    card.append(heading, detail);
    container.appendChild(card);
  });
}

function appendContact(container, { label, icon, url, email = false }) {
  const item = document.createElement('div');
  item.className = `contact-item${email ? ' email-contact-item' : ''}`;
  const link = document.createElement('a');
  if (email) link.className = 'email-contact-link';
  link.href = url;
  link.setAttribute('aria-label', markdownText(label));
  link.title = markdownText(label);
  if (!email) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
  const iconElement = document.createElement('span');
  iconElement.className = `svg-icon icon-${icon}`;
  iconElement.setAttribute('aria-hidden', 'true');
  const text = document.createElement('span');
  if (email) text.textContent = label;
  else renderInline(text, label);
  if (!email) text.className = 'visually-hidden';
  link.append(iconElement, text);
  item.appendChild(link);
  container.appendChild(item);
}

function renderProfile(profile, contacts, resume) {
  const name = qs('.resume-profile-name');
  if (name) renderInline(name, localized(profile.name) || t('content.placeholder'));
  const download = qs('.resume-download');
  clear(download);
  const resumeUrl = localized(resume?.url);
  if (resumeUrl) {
    const link = document.createElement('a');
    link.className = 'publish-link primary-action';
    const external = /^https?:/.test(resumeUrl);
    link.href = external ? resumeUrl : fromRoot(resumeUrl);
    const icon = document.createElement('span');
    icon.className = 'svg-icon icon-file-pdf';
    icon.setAttribute('aria-hidden', 'true');
    const label = document.createElement('span');
    renderInline(label, localized(resume.label) || 'Download CV');
    link.append(icon, label);
    if (external) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
    else if (resume.download !== false) link.setAttribute('download', '');
    download.appendChild(link);
  }
  const details = qs('.resume-profile-details');
  clear(details);
  ['summary'].forEach((field) => {
    const value = localized(profile[field]);
    if (!value) return;
    const paragraph = document.createElement('p');
    renderInline(paragraph, value);
    details.appendChild(paragraph);
  });
  const links = qs('.resume-contact-links');
  clear(links);
  links.classList.toggle('has-multiple-socials', (contacts || []).length >= 2);
  const email = localized(profile.email);
  if (email) appendContact(links, { label: email, icon: 'envelope', url: `mailto:${email}`, email: true });
  const socialGroup = document.createElement('div');
  socialGroup.className = 'social-contact-group';
  (contacts || []).forEach((contact) => appendContact(socialGroup, {
    label: localized(contact.label), icon: contact.icon, url: contact.url,
  }));
  if (socialGroup.childElementCount) links.appendChild(socialGroup);
}

function renderResume(site) {
  applySiteIdentity(site, t('resume.title'));
  renderProfile(site.profile || {}, site.contacts || [], site.resume || {});
  renderEntries('.resume-education', site.education || [], ['institution', 'degree']);
  renderEntries('.resume-work', site.workExperience || [], ['title', 'organization', 'summary']);
  renderEntries('.resume-journals', site.publications?.journalArticles || [], ['title', 'venue']);
  renderEntries('.resume-conferences', site.publications?.conferencePapers || [], ['title', 'venue']);
  renderEntries('.resume-awards', site.awards || [], ['title']);
  const skills = qs('.resume-skills');
  if (!skills) { qs('#resume-status')?.remove(); return; }
  clear(skills);
  (site.techStack || []).filter((group) => group.status !== 'draft').forEach((group) => {
    const card = document.createElement('article');
    card.className = 'content-entry';
    const heading = document.createElement('h3');
    renderInline(heading, localized(group.title));
    const detail = document.createElement('p');
    (group.items || []).forEach((item, index) => {
      if (index) {
        const separator = document.createElement('span');
        separator.className = 'entry-separator';
        separator.textContent = ' · ';
        detail.appendChild(separator);
      }
      const value = document.createElement('span');
      value.className = 'entry-detail';
      renderInline(value, localized(item.name));
      detail.appendChild(value);
    });
    card.append(heading, detail);
    skills.appendChild(card);
  });
  qs('#resume-status')?.remove();
}

async function start() {
  initTheme();
  initNavigation();
  await initLanguage();
  revealInitialAnchor();
  try {
    const site = await loadSiteData();
    renderResume(site);
    onLanguageChange(() => renderResume(site));
  } catch (error) {
    const status = qs('#resume-status');
    if (status) { status.setAttribute('role', 'alert'); renderInline(status, t('resume.error')); }
  }
}

start();
