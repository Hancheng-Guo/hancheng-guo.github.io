export const ROOT_URL = new URL('../../../', import.meta.url);

export function fromRoot(path) {
  return new URL(path, ROOT_URL).href;
}
