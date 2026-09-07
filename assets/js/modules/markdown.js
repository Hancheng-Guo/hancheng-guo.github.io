import { marked } from '../../vendor/marked/marked.esm.js';

const underlineExtension = {
  name: 'underline',
  level: 'inline',
  start(source) {
    const match = /(^|[\s([{>])_(?!_)\S/.exec(source);
    return match ? match.index + match[1].length : -1;
  },
  tokenizer(source) {
    const match = /^_(?!_)(?=\S)([^_\n]*?\S)_(?!_)/.exec(source);
    if (!match) return undefined;
    return {
      type: 'underline',
      raw: match[0],
      tokens: this.lexer.inlineTokens(match[1]),
    };
  },
  renderer(token) {
    return `<u>${this.parser.parseInline(token.tokens)}</u>`;
  },
};

marked.use({ extensions: [underlineExtension] });
marked.setOptions({
  gfm: true,
  breaks: true,
});

const BLOCKED_ELEMENTS = 'script, style, iframe, object, embed, form, input, button, textarea, select';
const SAFE_PROTOCOLS = new Set(['http:', 'https:', 'mailto:', 'tel:']);
const UNDERSCORE_PLACEHOLDER = '\uE000';

function protectWordUnderscores(value) {
  return String(value ?? '').replace(/(?<=[\p{L}\p{N}])_(?=[\p{L}\p{N}])/gu, UNDERSCORE_PLACEHOLDER);
}

function restoreWordUnderscores(value) {
  return value.replaceAll(UNDERSCORE_PLACEHOLDER, '_');
}

function sanitize(html) {
  const template = document.createElement('template');
  template.innerHTML = html;
  template.content.querySelectorAll(BLOCKED_ELEMENTS).forEach((element) => element.remove());
  template.content.querySelectorAll('*').forEach((element) => {
    for (const attribute of [...element.attributes]) {
      const name = attribute.name.toLowerCase();
      if (name.startsWith('on') || name === 'style' || name === 'srcdoc') {
        element.removeAttribute(attribute.name);
      }
    }
    for (const attributeName of ['href', 'src']) {
      const value = element.getAttribute(attributeName);
      if (!value || value.startsWith('#') || value.startsWith('/') || value.startsWith('./') || value.startsWith('../')) continue;
      try {
        const url = new URL(value, window.location.href);
        if (!SAFE_PROTOCOLS.has(url.protocol)) element.removeAttribute(attributeName);
      } catch {
        element.removeAttribute(attributeName);
      }
    }
    if (element instanceof HTMLAnchorElement && element.href.startsWith('http')) {
      element.rel = 'noopener noreferrer';
    }
  });
  return template.innerHTML;
}

export function markdownInline(value) {
  return sanitize(restoreWordUnderscores(marked.parseInline(protectWordUnderscores(value))));
}

export function markdownBlock(value) {
  return sanitize(restoreWordUnderscores(marked.parse(protectWordUnderscores(value))));
}

export function renderInline(element, value) {
  if (element) element.innerHTML = markdownInline(value);
  return element;
}

export function renderBlock(element, value) {
  if (element) element.innerHTML = markdownBlock(value);
  return element;
}

export function markdownText(value) {
  const template = document.createElement('template');
  template.innerHTML = markdownInline(value);
  return template.content.textContent ?? '';
}
