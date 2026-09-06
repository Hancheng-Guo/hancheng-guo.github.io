import { fromRoot } from './paths.js';

let cachedSiteData;

export async function loadSiteData() {
  if (!cachedSiteData) {
    const response = await fetch(fromRoot('assets/data/site.json'));
    if (!response.ok) throw new Error(`Unable to load site data (${response.status})`);
    cachedSiteData = await response.json();
  }
  return cachedSiteData;
}
