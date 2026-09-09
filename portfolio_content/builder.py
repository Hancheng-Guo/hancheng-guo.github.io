from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import os
import re
import tempfile

from .validators import ValidationReport, validate_document, validate_education_items, validate_profile_assets, validate_work_experience_items
from .static_renderer import pretty_html, render_cv, render_home, render_project, write_text_atomic


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
_UNSET = object()


def _date_range(value: str | dict[str, str]) -> dict[str, str]:
    if isinstance(value, str):
        # A bare month has historically represented one fixed point in time.
        # Preserve that rendering while allowing a dict with only ``start``
        # to represent an ongoing interval.
        result = {"start": value, "end": value}
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
        if type(level) is not int or not 2 <= level <= 5:
            raise ValueError("level 必须是 2 到 5 之间的整数")
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

    def _add_link(
        self,
        link_type: str,
        url: str | None,
        *,
        label: str | dict[str, str] | None = None,
    ) -> "ProjectPage":
        link: dict[str, Any] = {"type": link_type, "url": url}
        if label is not None:
            link["label"] = _locales(label)
        self.project.setdefault("links", []).append(link)
        return self

    def add_github_link(
        self,
        url: str | None,
        *,
        label: str | dict[str, str] | None = None,
    ) -> "ProjectPage":
        return self._add_link("github", url, label=label)

    def add_doc_link(
        self,
        url: str | None,
        *,
        label: str | dict[str, str] | None = None,
    ) -> "ProjectPage":
        return self._add_link("techDoc", url, label=label)

    def add_bilibili_link(
        self,
        url: str | None,
        *,
        label: str | dict[str, str] | None = None,
    ) -> "ProjectPage":
        return self._add_link("bilibili", url, label=label)

    def add_youtube_link(
        self,
        url: str | None,
        *,
        label: str | dict[str, str] | None = None,
    ) -> "ProjectPage":
        return self._add_link("youtube", url, label=label)


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
    favicon: str | None = None
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

    def add_project(self, *, title: str | dict[str, str], summary: str | dict[str, str], thumbnail: str, project_id: str | None = None, tags: tuple[str, ...] | list[str] = (), featured: bool = False, year: int | None = None, date: str | dict[str, str] | None = None, status: str | None = None, thumbnail_alt: str | dict[str, str] | None = None) -> Project:
        project_id = project_id or self._next_project_id()
        # Detail pages are opt-in. This serialized marker is the shared source
        # of truth for generated HTML and client-side hydration.
        project = {"id": project_id, "page": f"pages/projects/{project_id}.html", "hasDetailPage": False, "thumbnail": {"src": thumbnail, "alt": _locales(thumbnail_alt or title)}, "tags": list(tags), "locales": {"en": {"title": _locales(title).get("en", ""), "summary": _locales(summary).get("en", ""), "blocks": []}, "zh": {"title": _locales(title).get("zh", _locales(title).get("en", "")), "summary": _locales(summary).get("zh", _locales(summary).get("en", "")), "blocks": []}}, "links": []}
        if featured: project["featured"] = True
        if year is not None: project["year"] = year
        if date is not None: project["date"] = _date_range(date)
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

    def set_profile(
        self,
        *,
        avatar: str | None | object = _UNSET,
        hero_background: str | None | object = _UNSET,
        **fields: Any,
    ) -> "Portfolio":
        """Update profile content and optional visual assets.

        ``avatar`` and ``hero_background`` are opt-in local asset paths.
        If either key is omitted, its corresponding image is not rendered.
        Passing ``None`` removes a previously configured image.
        """
        for key, value in (("avatar", avatar), ("hero_background", hero_background)):
            if value is _UNSET:
                continue
            if value is None:
                self.profile.pop(key, None)
            else:
                fields[key] = value
        self.profile.update(fields); return self

    def add_education(
        self,
        *,
        date: str | dict[str, str],
        position: str | dict[str, str] | None = None,
        institute: str | dict[str, str] | None = None,
        location: str | dict[str, str] | None = None,
        detail: str | dict[str, str] | None = None,
        institution: str | dict[str, str] | None = None,
        degree: str | dict[str, str] | None = None,
        **fields: Any,
    ) -> "Portfolio":
        """Add an Education entry using its three-line CV presentation.

        ``position`` and ``institute`` are the recommended names. The older
        ``degree`` and ``institution`` arguments remain supported and map to
        those fields respectively, so existing portfolio sources keep their
        intended meaning without a visual regression.
        """
        if position is None:
            position = degree if degree is not None else institution
        if institute is None:
            institute = institution
        if position is None:
            raise ValueError("add_education 必须提供 position（或旧版 degree/institution）")
        entry: dict[str, Any] = {"date": _date_range(date), "position": _locales(position)}
        if institute is not None:
            entry["institute"] = _locales(institute)
        if location is not None:
            entry["location"] = _locales(location)
        if detail is not None:
            entry["detail"] = _locales(detail)
        entry.update(fields)
        self.education.append(entry)
        return self

    def add_work_experience(
        self,
        *,
        date: str | dict[str, str],
        position: str | dict[str, str] | None = None,
        company: str | dict[str, str] | None = None,
        location: str | dict[str, str] | None = None,
        detail: str | dict[str, str] | None = None,
        status: str | None = None,
    ) -> "Portfolio":
        """Add a three-line Work Experience entry.

        ``position`` is required; ``company``, ``location``, and ``detail``
        are optional.
        """
        if position is None:
            raise ValueError("add_work_experience 必须提供 position")
        entry: dict[str, Any] = {"date": _date_range(date), "position": _locales(position)}
        if company is not None:
            entry["company"] = _locales(company)
        if location is not None:
            entry["location"] = _locales(location)
        if detail is not None:
            entry["detail"] = _locales(detail)
        if status is not None:
            entry["status"] = status
        self.work_experience.append(entry)
        return self

    def add_publication(self, *, publication_type: str, date: str | dict[str, str] | None = None, **fields: Any) -> "Portfolio":
        keys = {"journal": "journalArticles", "conference": "conferencePapers"}
        if publication_type not in keys:
            raise ValueError("publication_type 必须是 journal 或 conference")
        item = dict(fields)
        if date is not None: item["date"] = _date_range(date)
        self.publications[keys[publication_type]].append(item)
        return self

    def add_award(self, *, date: str | dict[str, str], **fields: Any) -> "Portfolio":
        self.awards.append({"date": _date_range(date), **fields}); return self

    def set_resume(self, **fields: Any) -> "Portfolio":
        self.resume.update(fields); return self

    def site_document(self) -> dict[str, Any]:
        site = {
            "name": _locales(self.site_name),
            "author": _locales(self.author),
            "copyrightText": _locales(self.copyright_text),
            "lastUpdateDate": _full_date(self.last_update_date),
        }
        if self.favicon:
            site["favicon"] = self.favicon
        return {
            "schemaVersion": 1,
            "site": site,
            "profile": self.profile,
            "education": self.education,
            "workExperience": self.work_experience,
            "publications": self.publications,
            "awards": self.awards,
            "resume": self.resume,
            "timeline": self.timeline,
            "techStack": self.tech_stack,
            "contacts": self.contacts,
        }

    def _create_page(self, project: dict[str, Any], *, template: str) -> ProjectPage:
        project_id = str(project["id"])
        if project_id in self._pages_added:
            raise ValueError(f"Project {project_id} already has a page")
        headings = {
            "case-study": [("Overview", "概览"), ("My Role", "我的职责"), ("Challenge", "挑战"), ("Approach", "方法"), ("Results", "结果"), ("Evidence", "证据")],
            "research": [("Abstract", "摘要"), ("Research Question", "研究问题"), ("Method", "方法"), ("Experiment", "实验"), ("Findings", "结论"), ("Limitations", "局限")],
            "competition": [("Objective", "目标"), ("Responsibilities", "职责"), ("System Design", "系统设计"), ("Results", "结果"), ("Awards", "奖项")],
            "minimal": [],
        }
        if template not in headings: raise ValueError(f"Unknown template: {template}")
        self._pages_added.add(project_id)
        project["hasDetailPage"] = True
        page = ProjectPage(project, template)
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
        root_path = Path(root)
        report = validate_document(self.document(), root=root_path)
        profile_report = validate_profile_assets(self.profile, root=root_path)
        report.errors.extend(profile_report.errors)
        report.warnings.extend(profile_report.warnings)
        education_report = validate_education_items(self.education)
        report.errors.extend(education_report.errors)
        report.warnings.extend(education_report.warnings)
        work_report = validate_work_experience_items(self.work_experience)
        report.errors.extend(work_report.errors)
        report.warnings.extend(work_report.warnings)
        if self.favicon:
            if str(self.favicon).startswith("http://"):
                report.errors.append("favicon 仅允许 https URL 或本地文件")
            elif not str(self.favicon).startswith("https://") and not (root_path / self.favicon).is_file():
                report.errors.append(f"favicon 文件不存在: {self.favicon}")
        return report

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
        active_pages = {str(root_path / str(project["page"])) for project in self.projects if project.get("hasDetailPage") is True}
        page_directory = root_path / "pages" / "projects"
        if page_directory.is_dir():
            for candidate in page_directory.glob("*.html"):
                if str(candidate) not in active_pages and "<!-- Generated by portfolio.py; do not edit. -->" in candidate.read_text(encoding="utf-8"):
                    candidate.unlink()
        for project in self.projects:
            if project.get("hasDetailPage") is not True:
                continue
            destination = root_path / str(project["page"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            html = pretty_html(render_project(self, project))
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
                handle.write(html)
                temporary = Path(handle.name)
            os.replace(temporary, destination)
            written.append(destination)
        return written

    def write_static_fallbacks(self, *, root: str | os.PathLike[str] = ".") -> None:
        """Generate complete, readable home and CV pages."""
        root_path = Path(root)
        write_text_atomic(root_path / "index.html", pretty_html(render_home(self)))
        write_text_atomic(root_path / "pages" / "cv.html", pretty_html(render_cv(self)))

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
        return render_project(self, project)
