import { currentLanguage } from './i18n.js';

function formatMonth(month) {
  const [year, monthNumber] = month.split('-').map(Number);
  return new Intl.DateTimeFormat(currentLanguage() === 'zh' ? 'zh-CN' : 'en', {
    year: 'numeric',
    month: 'short',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, monthNumber - 1, 1)));
}

export function formatDateRange(value) {
  if (!value) return '';
  const start = typeof value === 'string' ? value : value.start;
  const end = typeof value === 'object' ? value.end : undefined;
  if (!start) return '';
  if (typeof value === 'object' && !end) {
    if (currentLanguage() === 'zh') {
      const [year, month] = start.split('-').map(Number);
      return `${year}年${month}月 至今`;
    }
    return `Since ${formatMonth(start)}`;
  }
  return end && end !== start ? `${formatMonth(start)} – ${formatMonth(end)}` : formatMonth(start);
}

export function formatFullDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value ?? '')) return '';
  const [year, month, day] = value.split('-').map(Number);
  return new Intl.DateTimeFormat(currentLanguage() === 'zh' ? 'zh-CN' : 'en', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, month - 1, day)));
}
