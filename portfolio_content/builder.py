from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import os
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


@dataclass
class ProjectPage:
    project: dict[str, Any]
    template: str = "minimal"

    def _block(self, kind: str, **payload: Any) -> "ProjectPage":
        for lang in ("en", "zh"):
            localized = {"type": kind}
            for key, value in payload.items():
                localized[key] = _for_language(value, lang)
            self.project.setdefault("locales", {}).setdefault(lang, {}).setdefault("blocks", []).append(localized)
        return self

    def add_heading(self, text: str | dict[str, str], *, level: int = 2) -> "ProjectPage":
        return self._block("heading", level=level, text=_locales(text))

    def add_paragraph(self, text: str | dict[str, str]) -> "ProjectPage":
        return self._block("paragraph", text=_locales(text))

    def add_image(self, src: str, *, alt: str | dict[str, str], caption: str | dict[str, str] | None = None) -> "ProjectPage":
        item = {"src": src, "alt": _locales(alt)}
        if caption is not None:
            item["caption"] = _locales(caption)
        return self._block("image", **item)

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

    def add_link(self, link_type: str, url: str, *, label: str | dict[str, str] | None = None) -> "ProjectPage":
        link: dict[str, Any] = {"type": link_type, "url": url}
        if label is not None: link["label"] = _locales(label)
        self.project.setdefault("links", []).append(link)
        return self


@dataclass
class Portfolio:
    projects: list[dict[str, Any]] = field(default_factory=list)
    schema_version: int = 2

    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> "Portfolio":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(projects=data.get("projects", []), schema_version=data.get("schemaVersion", 2))

    def add_project(self, *, project_id: str, title: str | dict[str, str], summary: str | dict[str, str], thumbnail: str, tags: tuple[str, ...] | list[str] = (), featured: bool = False, year: int | None = None) -> dict[str, Any]:
        project = {"id": project_id, "slug": project_id, "page": f"project.html?id={project_id}", "featured": featured, "thumbnail": {"src": thumbnail, "alt": _locales(title)}, "tags": list(tags), "locales": {"en": {"title": _locales(title).get("en", ""), "summary": _locales(summary).get("en", ""), "blocks": []}, "zh": {"title": _locales(title).get("zh", _locales(title).get("en", "")), "summary": _locales(summary).get("zh", _locales(summary).get("en", "")), "blocks": []}}, "links": []}
        if year is not None: project["year"] = year
        self.projects.append(project)
        return project

    def add_project_page(self, project_id: str, *, template: str = "case-study") -> ProjectPage:
        project = next((p for p in self.projects if p.get("id") == project_id), None)
        if project is None: raise KeyError(f"Unknown project: {project_id}")
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
