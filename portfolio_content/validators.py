from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse
import re

ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BLOCKS = {"heading", "paragraph", "image", "gallery", "list", "quote", "video", "metrics"}
LINK_TYPES = {"github", "techDoc", "bilibili", "youtube"}
MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _date_range(report: "ValidationReport", value: object, *, field: str) -> None:
    if not isinstance(value, dict) or not isinstance(value.get("start"), str):
        report.errors.append(f"{field} 必须包含 start")
        return
    start = value["start"]
    end = value.get("end")
    if not MONTH.fullmatch(start) or (end is not None and (not isinstance(end, str) or not MONTH.fullmatch(end))):
        report.errors.append(f"{field} 必须使用 YYYY-MM 格式")
    elif end and end < start:
        report.errors.append(f"{field}.end 不能早于 start")

def _local_asset(report: "ValidationReport", value: object, *, field: str, root: Path) -> None:
    if not isinstance(value, str) or not value.strip():
        report.errors.append(f"{field} 不能为空")
    elif value.startswith(("https://", "http://")):
        if not value.startswith("https://"): report.errors.append(f"{field} 仅允许 https URL")
    elif not (root / value).is_file():
        report.errors.append(f"{field} 文件不存在: {value}")


def validate_profile_assets(profile: object, *, root: Path) -> "ValidationReport":
    """Validate optional profile media paths with the same rules as thumbnails.

    These fields deliberately stay optional: their absence means the matching
    visual is omitted, rather than falling back to a bundled placeholder.
    """
    report = ValidationReport()
    if not isinstance(profile, dict):
        report.errors.append("profile 必须是对象")
        return report
    for key in ("avatar", "hero_background"):
        if key in profile:
            value = profile[key]
            if isinstance(value, str) and value.startswith(("https://", "http://")):
                report.errors.append(f"profile.{key} 必须是本地文件")
            else:
                _local_asset(report, value, field=f"profile.{key}", root=root)
    return report

def _https_url(report: "ValidationReport", value: object, *, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        report.errors.append(f"{field} 不能为空")
    elif urlparse(value).scheme != "https":
        report.errors.append(f"{field} 仅允许 https URL: {value}")

def _validate_block(report: "ValidationReport", block: object, *, field: str, root: Path) -> None:
    if not isinstance(block, dict):
        report.errors.append(f"{field} 必须是对象"); return
    kind = block.get("type")
    if kind not in BLOCKS:
        report.errors.append(f"{field}.type 类型不支持: {kind}"); return
    if kind in {"heading", "paragraph", "quote"} and not isinstance(block.get("text"), str):
        report.errors.append(f"{field}.text 必须是文本")
    if kind == "heading":
        level = block.get("level", 2)
        if not isinstance(level, int) or not 2 <= level <= 6:
            report.errors.append(f"{field}.level 必须是 2 到 6 之间的整数")
    if kind == "image":
        _local_asset(report, block.get("src"), field=f"{field}.src", root=root)
        if not isinstance(block.get("alt"), str): report.errors.append(f"{field}.alt 必须是文本")
    if kind == "gallery":
        images = block.get("images")
        if not isinstance(images, list) or not images: report.errors.append(f"{field}.images 必须是非空数组")
        else:
            for index, image in enumerate(images):
                if not isinstance(image, dict): report.errors.append(f"{field}.images[{index}] 必须是对象"); continue
                _local_asset(report, image.get("src"), field=f"{field}.images[{index}].src", root=root)
                if not isinstance(image.get("alt"), str): report.errors.append(f"{field}.images[{index}].alt 必须是文本")
    if kind == "list" and (not isinstance(block.get("items"), list) or not block["items"] or not all(isinstance(item, str) for item in block["items"])):
        report.errors.append(f"{field}.items 必须是非空文本数组")
    if kind == "metrics":
        items = block.get("items")
        if not isinstance(items, list) or not items: report.errors.append(f"{field}.items 必须是非空数组")
        elif any(not isinstance(item, dict) or not isinstance(item.get("label"), str) or not isinstance(item.get("value"), str) for item in items):
            report.errors.append(f"{field}.items 必须包含文本 label 和 value")
    if kind == "video": _https_url(report, block.get("url"), field=f"{field}.url")

@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    @property
    def ok(self) -> bool: return not self.errors
    def format(self) -> str: return "\n".join([*(f"ERROR: {x}" for x in self.errors), *(f"WARNING: {x}" for x in self.warnings)]) or "OK"

def validate_document(data: dict, *, root: Path = Path(".")) -> ValidationReport:
    report = ValidationReport()
    if data.get("schemaVersion") != 2: report.errors.append("schemaVersion 必须为 2")
    projects = data.get("projects")
    if not isinstance(projects, list): report.errors.append("projects 必须是数组"); return report
    seen: set[str] = set()
    for index, project in enumerate(projects):
        prefix = f"project[{index}]"
        pid = project.get("id")
        if not isinstance(pid, str) or not ID.fullmatch(pid): report.errors.append(f"{prefix}.id 必须使用小写字母、数字和连字符")
        elif pid in seen: report.errors.append(f"{prefix}.id 重复: {pid}")
        else: seen.add(pid)
        locales = project.get("locales", {})
        for lang in ("en", "zh"):
            if not isinstance(locales.get(lang), dict): report.errors.append(f"{prefix}.locales 缺少 {lang}")
        en = locales.get("en", {})
        for field in ("title", "summary"):
            if not isinstance(en.get(field), str) or not en[field].strip(): report.errors.append(f"{prefix}.locales.en.{field} 不能为空")
        thumbnail = project.get("thumbnail")
        src = thumbnail.get("src") if isinstance(thumbnail, dict) else thumbnail
        if not isinstance(src, str) or not src: report.errors.append(f"{prefix}.thumbnail.src 不能为空")
        else: _local_asset(report, src, field=f"{prefix}.thumbnail.src", root=root)
        if project.get("date") is not None:
            _date_range(report, project["date"], field=f"{prefix}.date")
        for link in project.get("links", []):
            url = link.get("url") if isinstance(link, dict) else None
            link_type = link.get("type") if isinstance(link, dict) else None
            if link_type not in LINK_TYPES:
                report.errors.append(f"{prefix}.links 类型不支持: {link_type}")
            if not url: continue
            parsed = urlparse(url)
            if parsed.scheme not in {"https", "mailto"}: report.errors.append(f"{prefix}.links URL 仅允许 https 或 mailto: {url}")
        tags = project.get("tags")
        if tags is None: tags = locales.get("en", {}).get("tags")
        if not isinstance(tags, list): report.errors.append(f"{prefix}.tags 必须是数组")
        for lang, content in locales.items():
            blocks = content.get("blocks", []) if isinstance(content, dict) else []
            if not isinstance(blocks, list): report.errors.append(f"{prefix}.locales.{lang}.blocks 必须是数组"); continue
            for block_index, block in enumerate(blocks):
                _validate_block(report, block, field=f"{prefix}.locales.{lang}.blocks[{block_index}]", root=root)
    return report
