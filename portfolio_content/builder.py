from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from html import escape
import json
import os
import re
import tempfile

from .validators import ValidationReport, validate_document


def _locales(value: str | dict[str, str]) -> dict[str, str]:
    if isinstance(value, str):
        return {"en": value, "zh": value}
    return {str(k): str(v) for k, v in value.items()}


def _for_language(value: Any, language: str) -> Any:
    """Recursively resolve localized values inside block payloads."""
    if isinstance(value, dict):
        if "en" in value or "zh" in value:
            return _for_language(value.get(language, value.get("en", "")), language)
        return {key: _for_language(item, language) for key, item in value.items()}
    if isinstance(value, list):
        return [_for_language(item, language) for item in value]
    return value


_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
_DAY = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")


def _date_range(value: str | dict[str, str]) -> dict[str, str]:
    if isinstance(value, str):
        result = {"start": value}
    elif isinstance(value, dict):
        result = {key: str(value[key]) for key in ("start", "end") if value.get(key)}
    else:
        raise ValueError("date 必须是 YYYY-MM 或 dict(start=YYYY-MM, end=YYYY-MM)")
    if "start" not in result or any(not _MONTH.fullmatch(month) for month in result.values()):
        raise ValueError("date 必须使用 YYYY-MM 格式")
    if result.get("end", result["start"]) < result["start"]:
        raise ValueError("date.end 不能早于 date.start")
    return result


def _full_date(value: str) -> str:
    if not isinstance(value, str) or not _DAY.fullmatch(value):
        raise ValueError("last_update_date 必须使用 YYYY-MM-DD 格式")
    try:
        __import__("datetime").date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("last_update_date 不是有效日期") from error
    return value


_INLINE_LINK = re.compile(
    r"\[\*\*(?P<bold>[^\]]+)\*\*\]\((?P<bold_url>https?://[^)\s]+)\)"
    r"|\[(?P<label>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)"
)


def _inline_links(value: str) -> str:
    parts: list[str] = []
    cursor = 0
    for match in _INLINE_LINK.finditer(value):
        parts.append(escape(value[cursor:match.start()]))
        label = escape(match.group("bold") or match.group("label"))
        url = escape(match.group("bold_url") or match.group("url"), quote=True)
        content = f"<strong>{label}</strong>" if match.group("bold") else label
        parts.append(f'<a href="{url}">{content}</a>')
        cursor = match.end()
    parts.append(escape(value[cursor:]))
    return "".join(parts)


@dataclass
class ProjectPage:
    project: dict[str, Any]
    template: str = "minimal"

    def _block(self, kind: str, *, languages: tuple[str, ...] = ("en", "zh"), **payload: Any) -> "ProjectPage":
        for lang in languages:
            if lang not in {"en", "zh"}:
                raise ValueError(f"Unsupported language: {lang}")
            localized = {"type": kind}
            for key, value in payload.items():
                localized[key] = _for_language(value, lang)
            self.project.setdefault("locales", {}).setdefault(lang, {}).setdefault("blocks", []).append(localized)
        return self

    def add_heading(self, text: str | dict[str, str], *, level: int = 2, languages: tuple[str, ...] = ("en", "zh")) -> "ProjectPage":
        return self._block("heading", languages=languages, level=level, text=_locales(text))

    def add_paragraph(self, text: str | dict[str, str], *, languages: tuple[str, ...] = ("en", "zh")) -> "ProjectPage":
        return self._block("paragraph", languages=languages, text=_locales(text))

    def add_image(self, src: str, *, alt: str | dict[str, str], caption: str | dict[str, str] | None = None, languages: tuple[str, ...] = ("en", "zh")) -> "ProjectPage":
        item = {"src": src, "alt": _locales(alt)}
        if caption is not None:
            item["caption"] = _locales(caption)
        return self._block("image", languages=languages, **item)

    def add_gallery(self, images: list[dict[str, Any]], *, columns: str = "auto") -> "ProjectPage":
        return self._block("gallery", images=images, columns=columns)

    def add_list(self, items: list[str | dict[str, str]], *, ordered: bool = False) -> "ProjectPage":
        return self._block("list", items=[_locales(item) for item in items], ordered=ordered)

    def add_quote(self, text: str | dict[str, str], *, source: str | dict[str, str] | None = None) -> "ProjectPage":
        payload: dict[str, Any] = {"text": _locales(text)}
        if source is not None:
            payload["source"] = _locales(source)
        return self._block("quote", **payload)

    def add_metrics(self, items: list[dict[str, str]]) -> "ProjectPage":
        return self._block("metrics", items=items)

    def add_video(self, url: str, *, poster: str | None = None, title: str | dict[str, str] | None = None) -> "ProjectPage":
        payload: dict[str, Any] = {"url": url}
        if poster: payload["poster"] = poster
        if title is not None: payload["title"] = _locales(title)
        return self._block("video", **payload)

    def add_link(self, link_type: str, url: str | None, *, label: str | dict[str, str] | None = None) -> "ProjectPage":
        link: dict[str, Any] = {"type": link_type, "url": url}
        if label is not None: link["label"] = _locales(label)
        self.project.setdefault("links", []).append(link)
        return self


@dataclass
class Project:
    """A project returned by Portfolio.add_project()."""

    portfolio: "Portfolio"
    data: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.data["id"])

    def add_page(self, *, template: str = "case-study") -> ProjectPage:
        return self.portfolio._create_page(self.data, template=template)

@dataclass
class Portfolio:
    site_name: dict[str, str] = field(default_factory=lambda: {"en": "Lain-Ego Portfolio", "zh": "Lain-Ego 作品集"})
    author: dict[str, str] = field(default_factory=lambda: {"en": "Lain-Ego", "zh": "Lain-Ego"})
    copyright_text: dict[str, str] = field(default_factory=lambda: {"en": "All rights reserved.", "zh": "保留所有权利。"})
    last_update_date: str = "2025-01-01"
    projects: list[dict[str, Any]] = field(default_factory=list)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    tech_stack: list[dict[str, Any]] = field(default_factory=list)
    contacts: list[dict[str, Any]] = field(default_factory=list)
    profile: dict[str, Any] = field(default_factory=dict)
    education: list[dict[str, Any]] = field(default_factory=list)
    work_experience: list[dict[str, Any]] = field(default_factory=list)
    publications: dict[str, list[dict[str, Any]]] = field(default_factory=lambda: {"journalArticles": [], "conferencePapers": []})
    awards: list[dict[str, Any]] = field(default_factory=list)
    resume: dict[str, Any] = field(default_factory=dict)
    schema_version: int = 2
    _pages_added: set[str] = field(default_factory=set, init=False, repr=False)

    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> "Portfolio":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(projects=data.get("projects", []), schema_version=data.get("schemaVersion", 2))

    def add_project(self, *, title: str | dict[str, str], summary: str | dict[str, str], thumbnail: str, project_id: str | None = None, tags: tuple[str, ...] | list[str] = (), featured: bool = False, year: int | None = None, status: str | None = None, thumbnail_alt: str | dict[str, str] | None = None) -> Project:
        project_id = project_id or self._next_project_id()
        project = {"id": project_id, "page": f"pages/projects/{project_id}.html", "thumbnail": {"src": thumbnail, "alt": _locales(thumbnail_alt or title)}, "tags": list(tags), "locales": {"en": {"title": _locales(title).get("en", ""), "summary": _locales(summary).get("en", ""), "blocks": []}, "zh": {"title": _locales(title).get("zh", _locales(title).get("en", "")), "summary": _locales(summary).get("zh", _locales(summary).get("en", "")), "blocks": []}}, "links": []}
        if featured: project["featured"] = True
        if year is not None: project["year"] = year
        if status is not None: project["status"] = status
        self.projects.append(project)
        return Project(self, project)

    def _next_project_id(self) -> str:
        used = {str(project.get("id")) for project in self.projects}
        number = 1
        while f"project{number}" in used:
            number += 1
        return f"project{number}"

    def add_timeline_event(self, *, date: str | dict[str, str], title: str | dict[str, str], description: str | dict[str, str]) -> None:
        self.timeline.append({"date": _date_range(date), "title": _locales(title), "description": _locales(description)})

    def add_tech_group(self, *, title: str | dict[str, str], items: list[dict[str, str]]) -> None:
        self.tech_stack.append({"title": _locales(title), "items": items})

    def add_contact(self, *, label: str | dict[str, str], icon: str, url: str) -> None:
        self.contacts.append({"label": _locales(label), "icon": icon, "url": url})

    def set_profile(self, **fields: Any) -> "Portfolio":
        self.profile.update(fields); return self

    def add_education(self, *, date: str | dict[str, str], **fields: Any) -> "Portfolio":
        self.education.append({"date": _date_range(date), **fields}); return self

    def add_work_experience(self, *, date: str | dict[str, str], **fields: Any) -> "Portfolio":
        self.work_experience.append({"date": _date_range(date), **fields}); return self

    def add_publication(self, *, publication_type: str, date: str | dict[str, str], **fields: Any) -> "Portfolio":
        keys = {"journal": "journalArticles", "conference": "conferencePapers"}
        if publication_type not in keys:
            raise ValueError("publication_type 必须是 journal 或 conference")
        self.publications[keys[publication_type]].append({"date": _date_range(date), **fields})
        return self

    def add_award(self, *, date: str | dict[str, str], **fields: Any) -> "Portfolio":
        self.awards.append({"date": _date_range(date), **fields}); return self

    def set_resume(self, **fields: Any) -> "Portfolio":
        self.resume.update(fields); return self

    def site_document(self) -> dict[str, Any]:
        return {"schemaVersion": 1, "site": {"name": _locales(self.site_name), "author": _locales(self.author), "copyrightText": _locales(self.copyright_text), "lastUpdateDate": _full_date(self.last_update_date)}, "profile": self.profile, "education": self.education, "workExperience": self.work_experience, "publications": self.publications, "awards": self.awards, "resume": self.resume, "timeline": self.timeline, "techStack": self.tech_stack, "contacts": self.contacts}

    def _create_page(self, project: dict[str, Any], *, template: str) -> ProjectPage:
        project_id = str(project["id"])
        if project_id in self._pages_added:
            raise ValueError(f"Project {project_id} already has a page")
        self._pages_added.add(project_id)
        page = ProjectPage(project, template)
        headings = {
            "case-study": [("Overview", "概览"), ("My Role", "我的职责"), ("Challenge", "挑战"), ("Approach", "方法"), ("Results", "结果"), ("Evidence", "证据")],
            "research": [("Abstract", "摘要"), ("Research Question", "研究问题"), ("Method", "方法"), ("Experiment", "实验"), ("Findings", "结论"), ("Limitations", "局限")],
            "competition": [("Objective", "目标"), ("Responsibilities", "职责"), ("System Design", "系统设计"), ("Results", "结果"), ("Awards", "奖项")],
            "minimal": [],
        }
        if template not in headings: raise ValueError(f"Unknown template: {template}")
        for english, chinese in headings[template]:
            page.add_heading({"en": english, "zh": chinese})
        return page

    def add_project_page(self, project_id: str, *, template: str = "case-study") -> ProjectPage:
        project = next((p for p in self.projects if p.get("id") == project_id), None)
        if project is None: raise KeyError(f"Unknown project: {project_id}")
        return self._create_page(project, template=template)

    def remove_project(self, project_id: str) -> None:
        self.projects = [p for p in self.projects if p.get("id") != project_id]

    def document(self) -> dict[str, Any]:
        return {"schemaVersion": self.schema_version, "projects": self.projects}

    def validate(self, *, root: str | os.PathLike[str] = ".") -> ValidationReport:
        return validate_document(self.document(), root=Path(root))

    def write(self, output: str | os.PathLike[str], *, root: str | os.PathLike[str] = ".") -> None:
        report = self.validate(root=root)
        if not report.ok: raise ValueError(report.format())
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.document(), ensure_ascii=False, indent=2) + "\n"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
            handle.write(payload); temporary = Path(handle.name)
        os.replace(temporary, destination)

    def write_pages(self, *, root: str | os.PathLike[str] = ".") -> list[Path]:
        root_path = Path(root)
        written: list[Path] = []
        active_pages = {str(root_path / str(project["page"])) for project in self.projects}
        page_directory = root_path / "pages" / "projects"
        if page_directory.is_dir():
            for candidate in page_directory.glob("*.html"):
                if str(candidate) not in active_pages and "<!-- Generated by portfolio.py; do not edit. -->" in candidate.read_text(encoding="utf-8"):
                    candidate.unlink()
        for project in self.projects:
            if str(project.get("page", "")).startswith("pages/project.html?"):
                continue
            destination = root_path / str(project["page"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            html = self._page_html(project)
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
                handle.write(html)
                temporary = Path(handle.name)
            os.replace(temporary, destination)
            written.append(destination)
        return written

    def write_site_data(self, output: str | os.PathLike[str] = "assets/data/site.json") -> Path:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.site_document(), ensure_ascii=False, indent=2) + "\n"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
            handle.write(payload)
            temporary = Path(handle.name)
        os.replace(temporary, destination)
        return destination

    def _page_html(self, project: dict[str, Any]) -> str:
        pid = escape(str(project["id"]), quote=True)
        english = project["locales"]["en"]
        title = escape(english["title"])
        summary = escape(english["summary"], quote=True)
        image = escape(project["thumbnail"]["src"], quote=True)
        page = escape(project["page"], quote=True)
        site_name = escape(_locales(self.site_name).get("en", "Portfolio"))
        author = escape(_locales(self.author).get("en", site_name))
        copyright_text = _inline_links(_locales(self.copyright_text).get("en", ""))
        copyright_suffix = f", {copyright_text}" if copyright_text else ""
        last_update_date = _full_date(self.last_update_date)
        last_update_year = last_update_date[:4]
        robots = '\n  <meta name="robots" content="noindex, nofollow">' if project.get("status") == "draft" else ""
        structured_data = json.dumps({
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": english["title"],
            "description": english["summary"],
            "url": f"https://hancheng-guo.github.io/{project['page']}",
            "image": f"https://hancheng-guo.github.io/{project['thumbnail']['src']}",
        }, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        return f'''<!DOCTYPE html>
<!-- Generated by portfolio.py; do not edit. -->
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - {site_name}</title>
  <meta name="description" content="{summary}">{robots}
  <meta property="og:title" content="{title} - {site_name}">
  <meta property="og:description" content="{summary}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://hancheng-guo.github.io/{page}">
  <meta property="og:image" content="https://hancheng-guo.github.io/{image}">
  <link rel="canonical" href="https://hancheng-guo.github.io/{page}">
  <script type="application/ld+json">{structured_data}</script>
  <link rel="icon" href="../../assets/images/Avatar.jpg">
  <script>document.documentElement.setAttribute('data-theme', localStorage.getItem('theme') || 'dark');</script>
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body data-page="project" data-project-id="{pid}">
  <nav><div class="container nav-container">
    <a href="../../index.html" class="logo"><span class="logo-text">{author}</span><div class="logo-dot"></div></a>
    <div class="nav-actions">
      <button class="control-btn menu-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Open navigation" data-i18n-aria-label="nav.openMenu">☰</button>
      <div class="nav-links" id="primary-navigation">
        <a href="../../index.html#top" data-i18n="nav.portfolio">Portfolio</a>
        <a href="../../index.html#projects" data-i18n="nav.project">Project</a>
        <a href="../../index.html#publications" data-i18n="nav.publications">Publications</a>
        <a href="../../index.html#timeline" data-i18n="nav.timeline">Timeline</a>
        <a href="../cv.html" data-i18n="nav.resume">CV</a>
      </div>
      <div class="nav-controls">
        <button class="control-btn lang-toggle" aria-label="Toggle language" data-i18n-aria-label="nav.toggleLanguage">中文</button>
        <button class="control-btn theme-toggle" aria-label="Toggle color theme" data-i18n-aria-label="nav.toggleTheme"><span class="svg-icon icon-sun sun-icon" aria-hidden="true"></span><span class="svg-icon icon-moon moon-icon" aria-hidden="true"></span></button>
      </div>
    </div>
  </div></nav>
  <section class="section-padding"><div class="container"><div class="card project-detail-card"><div class="project-container"></div></div></div></section>
  <footer><span class="footer-copyright">© {last_update_year} {author}{copyright_suffix}</span><span class="footer-updated">Site last updated {last_update_date}</span></footer>
  <script type="module" src="../../assets/js/app.js"></script>
</body>
</html>
'''
