(() => {
  const EDUCATION_EVENTS = [
    'education.event2',
    'education.event1',
  ]

  const PROJECTS = [
    {
      img: 'assets/images/Portfolio-01.png',
      titleKey: 'projects.item1.title',
      descKey: 'projects.item1.desc',
      tagsKey: 'projects.item1.tags',
      link: 'pages/projects/project1.html',
    },
    {
      img: 'assets/images/Portfolio-02.png',
      titleKey: 'projects.item2.title',
      descKey: 'projects.item2.desc',
      tagsKey: 'projects.item2.tags',
      link: 'pages/projects/project2.html',
    },
    {
      img: 'assets/images/Portfolio-03.png',
      titleKey: 'projects.item3.title',
      descKey: 'projects.item3.desc',
      tagsKey: 'projects.item3.tags',
      link: 'pages/projects/project3.html',
    },
    {
      img: 'assets/images/Portfolio-04.png',
      titleKey: 'projects.item4.title',
      descKey: 'projects.item4.desc',
      tagsKey: 'projects.item4.tags',
      link: 'pages/projects/project4.html',
    }
  ];

  const OPEN_SOURCE_ITEMS = [
    { key: 'opensource.item1', linkCode: 'https://github.com/Lain-Ego0/BRS-Parallel-Robot', linkDoc: null },
    { key: 'opensource.item2', linkCode: 'https://github.com/Lain-Ego0/SliverWolf-ArmRobotDog', linkDoc: null },
    { key: 'opensource.item3', linkCode: null, linkDoc: 'https://wcn9j5638vrr.feishu.cn/wiki/space/7570988375279517715' },
    { key: 'opensource.item4', linkCode: 'https://github.com/Lain-Ego0/ROBOCON2024-R1', linkDoc: null },
    { key: 'opensource.item5', linkCode: 'https://github.com/Lain-Ego0/ROBOCON2024-3508DOG', linkDoc: null },
    { key: 'opensource.item6', linkCode: 'https://github.com/Lain-Ego0/HTDW4438_Isaacgym', linkDoc: null },
    { key: 'opensource.item7', linkCode: 'https://github.com/Lain-Ego0/HTDW4438-OpenDog', linkDoc: null },
    { key: 'opensource.item8', linkCode: 'https://github.com/Lain-Ego0/Lain-s-Note', linkDoc: null },
    { key: 'opensource.item9', linkCode: 'https://github.com/Lain-Ego0/Lain-s-PDF2PNG', linkDoc: null },
  ];

  const TIMELINE_EVENTS = [
    'timeline.event9',
    'timeline.event8',
    'timeline.event7',
    'timeline.event6',
    'timeline.event5',
    'timeline.event4',
    'timeline.event3',
    'timeline.event2',
    'timeline.event1',
  ];

  const TECH_STACK = [
    {
      category: 'skills.embedded',
      items: [
        { name: 'STM32', icon: 'fas fa-microchip' },
        { name: 'ESP32', icon: 'fas fa-wifi' },
        { name: 'FreeRTOS', icon: 'fas fa-cogs' },
        { name: 'C/C++', icon: 'fas fa-code' },
      ],
    },
    {
      category: 'skills.robotics',
      items: [
        { name: 'ROS/ROS2', icon: 'fas fa-robot' },
        { name: 'Gazebo', icon: 'fas fa-cube' },
        { name: 'Motion Control', icon: 'fas fa-wave-square' },
        { name: 'RL', icon: 'fas fa-brain' },
      ],
    },
    {
      category: 'skills.hardware',
      items: [
        { name: 'Altium', icon: 'fas fa-pencil-ruler' },
        { name: 'SolidWorks', icon: 'fas fa-drafting-compass' },
        { name: 'PCB', icon: 'fas fa-layer-group' },
      ],
    },
    {
      category: 'skills.software',
      items: [
        { name: 'Linux', icon: 'fab fa-linux' },
        { name: 'Python', icon: 'fab fa-python' },
        { name: 'Git', icon: 'fab fa-git-alt' },
      ],
    },
  ];

  const CONTACT_LINKS = [
    { icon: 'fab fa-bilibili', key: 'contact.bilibili', link: 'https://space.bilibili.com/385516781/upload/video' },
    { icon: 'fab fa-github', key: 'contact.github', link: 'https://github.com/Lain-Ego0' },
    { icon: 'fab fa-twitter', key: 'contact.twitter', link: 'https://x.com/Lain_Ego0' },
    { icon: 'fab fa-zhihu', key: 'contact.zhihu', link: 'https://www.zhihu.com/people/hua-99-50-21' },
  ];

  function qs(selector, root = document) {
    return root.querySelector(selector);
  }

  function qsa(selector, root = document) {
    return Array.from(root.querySelectorAll(selector));
  }

  function clear(el) {
    if (!el) return;
    el.innerHTML = '';
  }

  function t(key) {
    return window.i18n?.get ? window.i18n.get(key) : key;
  }

  function renderSpanTags(tags, className) {
    if (!Array.isArray(tags)) return '';
    return tags.map((tag) => `<span class="${className}">${tag}</span>`).join('');
  }

  function renderProjectTags(tags) {
    if (!Array.isArray(tags)) return '';
    return `<div class="project-tags">${renderSpanTags(tags, 'project-tag')}</div>`;
  }

  function initThemeToggle() {
    const toggleBtn = qs('.theme-toggle');
    const htmlEl = document.documentElement;
    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);

    toggleBtn.addEventListener('click', () => {
      const currentTheme = htmlEl.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      htmlEl.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      console.log(`[Theme] Switched to ${newTheme}`);
    });
  }

  function initLangToggle() {
    const toggleBtn = qs('.lang-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
      const current = window.i18n.currentLang();
      const next = current === 'en' ? 'zh' : 'en';
      console.log(`[Lang] Switching to ${next}...`);
      window.i18n.changeLang(next);
    });
  }

  function initEducation() {
    const container = qs('.education-container');
    if (!container) return;
    clear(container);

    EDUCATION_EVENTS.forEach((key) => {
      const item = document.createElement('div');
      item.className = 'timeline-item';
      item.innerHTML = `
        <div class="timeline-dot"></div>
        <span class="timeline-date">${t(`${key}.date`)}</span>
        <div class="timeline-content">
          <h3>${t(`${key}.title`)}</h3> 
          <p>${t(`${key}.desc`)}</p>
        </div>
      `;
      container.appendChild(item);
    });
  }

  function initProjects() {
    const grid = qs('.projects-grid');
    if (!grid) return;
    clear(grid);

    PROJECTS.forEach((project) => {
      const tagsHtml = renderProjectTags(t(project.tagsKey));

      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="project-thumbnail-wrapper">
          <img src="${project.img}" alt="${t('projects.imgAlt')}" class="project-thumbnail">
        </div>
        <div class="project-info">
          <h3>${t(project.titleKey)}</h3>
          <p>${t(project.descKey)}</p>
          ${tagsHtml}
          <a href="${project.link}" class="project-link">${t('projects.viewDetail')}</a>
        </div>
      `;
      card.onclick = () => {window.location.href = project.link;};
      grid.appendChild(card); 
    });
  }

  function initOpenSource() {
    const grid = qs('.opensource-grid');
    if (!grid) return;
    clear(grid);

    OPEN_SOURCE_ITEMS.forEach((item) => {
      const tags = t(`${item.key}.tags`) || [];
      const tagsHtml = renderSpanTags(tags, 'os-tag');

      let buttonsHtml = '';
      if (item.linkCode) {
        buttonsHtml += `<a href="${item.linkCode}" target="_blank" rel="noopener noreferrer" class="os-btn"><i class="fab fa-github"></i> ${t('opensource.btnCode')}</a>`;
      }
      if (item.linkDoc) {
        buttonsHtml += `<a href="${item.linkDoc}" target="_blank" rel="noopener noreferrer" class="os-btn"><i class="fas fa-book"></i> ${t('opensource.btnDoc')}</a>`;
      }

      const card = document.createElement('div');
      card.className = 'os-card';
      card.innerHTML = `
        <div class="os-header">
          <div class="os-title">${t(`${item.key}.title`)}</div>
          <i class="fas fa-code-branch" style="color:var(--primary); opacity:0.5;"></i>
        </div>
        <p class="os-desc">${t(`${item.key}.desc`)}</p>
        <div class="os-tags">${tagsHtml}</div>
        <div class="os-actions">${buttonsHtml}</div>
      `;
      grid.appendChild(card);
    });
  }

  function initTimeline() {
    const container = qs('.timeline-container');
    if (!container) return;
    clear(container);

    TIMELINE_EVENTS.forEach((key) => {
      const item = document.createElement('div');
      item.className = 'timeline-item';
      item.innerHTML = `
        <div class="timeline-dot"></div>
        <span class="timeline-date">${t(`${key}.date`)}</span>
        <div class="timeline-content">
          <h3>${t(`${key}.title`)}</h3> 
          <p>${t(`${key}.desc`)}</p>
        </div>
      `;
      container.appendChild(item);
    });
  }

  function initTechStack() {
    const container = qs('.skills-wrapper');
    if (!container) return;
    clear(container);

    TECH_STACK.forEach((group) => {
      const itemsHtml = group.items
        .map((s) => `<div class="skill-badge"><i class="${s.icon}"></i> ${s.name}</div>`)
        .join('');

      const col = document.createElement('div');
      col.className = 'skill-category';
      col.innerHTML = `<h3>${t(group.category)}</h3><div class="skill-list">${itemsHtml}</div>`;
      container.appendChild(col);
    });
  }

  function initContactLinks() {
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

  function initSmoothScroll() {
    qsa('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const href = this.getAttribute('href');
        if (!href || href === '#') return;

        let target;
        try {
          target = qs(href);
        } catch {
          return;
        }

        if (target) {
          window.scrollTo({
            top: target.offsetTop - 80,
            behavior: 'smooth',
          });
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initLangToggle();
    initSmoothScroll();
  });

  window.addEventListener('i18nLoaded', () => {
    console.log('[main] i18n loaded, rendering content...');
    // initEducation()
    initProjects();
    // initOpenSource();
    initTimeline();
    initTechStack();
    initContactLinks();
  });




  const images = document.querySelectorAll('.project-img');
  let overlay = null;

  images.forEach(img => {
    img.addEventListener('click', () => {
      overlay = document.createElement('div');
      overlay.className = 'lightbox-overlay';

      const largeImg = document.createElement('img');
      largeImg.src = img.dataset.large || img.src;
      largeImg.alt = img.alt || '';

      const closeBtn = document.createElement('button');
      closeBtn.className = 'lightbox-close';
      closeBtn.type = 'button';
      closeBtn.setAttribute('aria-label', 'Close image');
      closeBtn.innerHTML = '&times;';

      let scale = 1;
      let translateX = 0;
      let translateY = 0;
      const minScale = 0.2;
      const maxScale = 8;
      const wheelStep = 0.12;
      const dblclickScale = 2.2;

      let isDragging = false;
      let startX = 0;
      let startY = 0;
      let startTranslateX = 0;
      let startTranslateY = 0;

      function updateTransform() {
        largeImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
      }

      largeImg.addEventListener('click', e => {
        e.stopPropagation();
      });

      closeBtn.addEventListener('click', e => {
        e.stopPropagation();
        closeLightbox();
      });

      overlay.addEventListener('wheel', e => {
        e.preventDefault();

        scale += e.deltaY < 0 ? wheelStep : -wheelStep;
        scale = Math.max(minScale, Math.min(maxScale, scale));

        updateTransform();
      }, { passive: false });

      largeImg.addEventListener('dblclick', e => {
        e.stopPropagation();

        if (scale === 1) {
          scale = dblclickScale;
        } else {
          scale = 1;
          translateX = 0;
          translateY = 0;
        }

        updateTransform();
      });

      largeImg.addEventListener('mousedown', e => {
        e.preventDefault();
        e.stopPropagation();

        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        startTranslateX = translateX;
        startTranslateY = translateY;

        largeImg.classList.add('dragging');
      });

      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);

      function handleMouseMove(e) {
        if (!isDragging) return;

        translateX = startTranslateX + (e.clientX - startX);
        translateY = startTranslateY + (e.clientY - startY);

        updateTransform();
      }

      function handleMouseUp() {
        if (!isDragging) return;
        isDragging = false;
        largeImg.classList.remove('dragging');
      }

      overlay.appendChild(largeImg);
      overlay.appendChild(closeBtn);
      document.body.appendChild(overlay);
      document.body.style.overflow = 'hidden';

      // overlay.addEventListener('click', closeLightbox);
      overlay.addEventListener('click', closeLightbox, { once: true });

      overlay._cleanup = () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    });
  });

  function closeLightbox() {
    if (!overlay) return;
    overlay.remove();
    overlay = null;
    document.body.style.overflow = '';
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeLightbox();
  });

})();
