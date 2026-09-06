import { fromRoot } from './paths.js';

let projectsPromise;

export function loadProjects() {
  projectsPromise ??= fetch(fromRoot('assets/data/projects.json')).then((response) => {
    if (!response.ok) throw new Error('Unable to load project data');
    return response.json();
  }).then((data) => data.projects);

  return projectsPromise;
}

export async function loadProject(id) {
  const projects = await loadProjects();
  return projects.find((project) => project.id === id);
}
