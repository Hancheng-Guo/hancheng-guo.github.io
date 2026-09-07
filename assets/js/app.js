import { initHome } from './modules/home.js';
import { initLanguage } from './modules/i18n.js';
import { initNavigation, revealInitialAnchor } from './modules/navigation.js';
import { initProjectDetail } from './modules/project-detail.js';
import { initTheme } from './modules/theme.js';

initTheme();
initNavigation();

if (document.body.dataset.page === 'project') {
  initProjectDetail();
} else {
  initHome();
}

await initLanguage();
revealInitialAnchor();
