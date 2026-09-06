import { qsa } from './dom.js';

export function initLightbox(root = document) {
  qsa('.project-img', root).forEach((image) => {
    image.addEventListener('click', () => openLightbox(image));
  });
}

function openLightbox(sourceImage) {
  const overlay = document.createElement('div');
  const image = document.createElement('img');
  const closeButton = document.createElement('button');
  let scale = 1;
  let translateX = 0;
  let translateY = 0;
  let dragging = false;
  let startX = 0;
  let startY = 0;
  let startTranslateX = 0;
  let startTranslateY = 0;

  overlay.className = 'lightbox-overlay';
  image.src = sourceImage.dataset.large || sourceImage.src;
  image.alt = sourceImage.alt || '';
  closeButton.className = 'lightbox-close';
  closeButton.type = 'button';
  closeButton.setAttribute('aria-label', 'Close image');
  closeButton.innerHTML = '&times;';

  const updateTransform = () => {
    image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
  };

  const close = () => {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
    document.removeEventListener('keydown', onKeyDown);
    overlay.remove();
    document.body.style.overflow = '';
  };

  const onMouseMove = (event) => {
    if (!dragging) return;
    translateX = startTranslateX + event.clientX - startX;
    translateY = startTranslateY + event.clientY - startY;
    updateTransform();
  };

  const onMouseUp = () => {
    dragging = false;
    image.classList.remove('dragging');
  };

  const onKeyDown = (event) => {
    if (event.key === 'Escape') close();
  };

  overlay.addEventListener('click', close);
  closeButton.addEventListener('click', close);
  image.addEventListener('click', (event) => event.stopPropagation());
  image.addEventListener('wheel', (event) => {
    event.preventDefault();
    scale = Math.max(0.2, Math.min(8, scale + (event.deltaY < 0 ? 0.12 : -0.12)));
    updateTransform();
  }, { passive: false });
  image.addEventListener('dblclick', (event) => {
    event.stopPropagation();
    scale = scale === 1 ? 2.2 : 1;
    if (scale === 1) translateX = translateY = 0;
    updateTransform();
  });
  image.addEventListener('mousedown', (event) => {
    event.preventDefault();
    event.stopPropagation();
    dragging = true;
    startX = event.clientX;
    startY = event.clientY;
    startTranslateX = translateX;
    startTranslateY = translateY;
    image.classList.add('dragging');
  });

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
  document.addEventListener('keydown', onKeyDown);
  overlay.append(image, closeButton);
  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';
}
