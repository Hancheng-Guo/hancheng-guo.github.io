import json
import importlib.util
import unittest
from pathlib import Path
from portfolio_content import Portfolio
from portfolio_content.validators import validate_document
from portfolio_content.cli import clean_generated_output, clean_generated_pages

class BuilderTests(unittest.TestCase):
  def test_clean_removes_only_generated_output_and_is_idempotent(self):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      generated = Path(folder) / "projects.json"
      unrelated = Path(folder) / "image.jpg"
      generated.write_text("{}", encoding="utf-8")
      unrelated.write_text("keep", encoding="utf-8")
      self.assertTrue(clean_generated_output(generated))
      self.assertFalse(generated.exists())
      self.assertTrue(unrelated.exists())
      self.assertFalse(clean_generated_output(generated))

  def test_project_owns_one_automatically_located_page(self):
    project = Portfolio().add_project(
      title={"en": "My Robot Project", "zh": "我的机器人"},
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
    )
    self.assertEqual(project.id, "project1")
    self.assertEqual(project.data["page"], "pages/projects/project1.html")
    project.add_page(template="minimal")
    with self.assertRaises(ValueError):
      project.add_page(template="minimal")

  def test_generated_page_can_be_built_and_cleaned(self):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      portfolio = Portfolio(
        copyright_text={
          "en": "Powered by [**Example**](https://example.com)",
          "zh": "由 [**Example**](https://example.com) 提供支持",
        },
      )
      project = portfolio.add_project(project_id="demo", title="Demo", summary="Summary", thumbnail="assets/images/Avatar.jpg")
      project.add_page(template="minimal").add_paragraph("Body")
      pages = portfolio.write_pages(root=folder)
      self.assertEqual(len(pages), 1)
      generated = pages[0].read_text(encoding="utf-8")
      self.assertIn('data-project-id="demo"', generated)
      self.assertIn('<a href="https://example.com"><strong>Example</strong></a>', generated)
      self.assertEqual(clean_generated_pages(folder), pages)
      self.assertFalse(pages[0].exists())

  def test_root_python_source_matches_runtime_project_data(self):
    source = Path("portfolio.py")
    spec = importlib.util.spec_from_file_location("portfolio_source_regression", source)
    self.assertIsNotNone(spec)
    self.assertIsNotNone(spec.loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    runtime_data = json.loads(Path("assets/data/projects.json").read_text(encoding="utf-8"))
    self.assertEqual(module.portfolio.document(), runtime_data)
    runtime_site = json.loads(Path("assets/data/site.json").read_text(encoding="utf-8"))
    self.assertEqual(module.portfolio.site_document(), runtime_site)

  def test_builder_is_chainable_and_validates(self):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      portfolio = Portfolio()
      portfolio.add_project(project_id="demo", title={"en": "Demo", "zh": "演示"}, summary={"en": "A demo", "zh": "演示"}, thumbnail="assets/images/Avatar.jpg")
      portfolio.add_project_page("demo").add_paragraph("Hello").add_heading("Results")
      self.assertTrue(portfolio.validate(root='.').ok)
      output = __import__('pathlib').Path(folder) / "projects.json"
      portfolio.write(output, root='.')
      self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["schemaVersion"], 2)

  def test_duplicate_ids_fail_validation(self):
    portfolio = Portfolio()
    for _ in range(2): portfolio.add_project(project_id="demo", title="Demo", summary="Summary", thumbnail="x.png")
    self.assertFalse(portfolio.validate().ok)

  def test_invalid_url_unknown_block_missing_image_and_missing_english(self):
    base = {"schemaVersion": 2, "projects": [{"id": "demo", "tags": [], "thumbnail": {"src": "no.png"}, "locales": {"en": {"title": "", "summary": "", "blocks": [{"type": "nope"}]}, "zh": {"title": "演示", "summary": "演示", "blocks": []}}, "links": [{"type": "x", "url": "javascript:alert(1)"}]}]}
    report = validate_document(base)
    self.assertFalse(report.ok)
    self.assertGreaterEqual(len(report.errors), 4)

  def test_deterministic_output_and_template_localization(self):
    one = Portfolio(); one.add_project(project_id="demo", title={"en": "Demo", "zh": "演示"}, summary={"en": "Summary", "zh": "摘要"}, thumbnail="assets/images/Avatar.jpg")
    one.add_project_page("demo", template="research").add_paragraph({"en": "English", "zh": "中文"})
    two = Portfolio(); two.add_project(project_id="demo", title={"en": "Demo", "zh": "演示"}, summary={"en": "Summary", "zh": "摘要"}, thumbnail="assets/images/Avatar.jpg")
    two.add_project_page("demo", template="research").add_paragraph({"en": "English", "zh": "中文"})
    self.assertEqual(one.document(), two.document())
    blocks = one.document()["projects"][0]["locales"]
    self.assertEqual([block["text"] for block in blocks["en"]["blocks"][:6]], ["Abstract", "Research Question", "Method", "Experiment", "Findings", "Limitations"])
    self.assertEqual(blocks["zh"]["blocks"][-1]["text"], "中文")

  def test_nested_gallery_and_metrics_are_localized(self):
    portfolio = Portfolio()
    portfolio.add_project(project_id="demo", title="Demo", summary="Summary", thumbnail="assets/images/Avatar.jpg")
    page = portfolio.add_project_page("demo", template="minimal")
    page.add_gallery([{"src": "assets/images/Avatar.jpg", "alt": {"en": "Avatar", "zh": "头像"}}])
    page.add_metrics([{"label": {"en": "Accuracy", "zh": "精度"}, "value": "±5 mm"}])
    locales = portfolio.document()["projects"][0]["locales"]
    self.assertEqual(locales["en"]["blocks"][0]["images"][0]["alt"], "Avatar")
    self.assertEqual(locales["zh"]["blocks"][0]["images"][0]["alt"], "头像")
    self.assertEqual(locales["zh"]["blocks"][1]["items"][0]["label"], "精度")

  def test_failed_write_does_not_overwrite(self):
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as folder:
      target = Path(folder) / "data.json"; target.write_text("original", encoding="utf-8")
      bad = Portfolio(); bad.add_project(project_id="demo", title="Demo", summary="Summary", thumbnail="missing.png")
      with self.assertRaises(ValueError): bad.write(target, root=folder)
      self.assertEqual(target.read_text(encoding="utf-8"), "original")

  def test_site_identity_and_dates_are_structured(self):
    portfolio = Portfolio(
      site_name={"en": "Example Portfolio", "zh": "示例作品集"},
      author={"en": "Example", "zh": "示例"},
      copyright_text={"en": "All rights reserved.", "zh": "保留所有权利。"},
      last_update_date="2026-09-07",
    )
    portfolio.add_timeline_event(date={"start": "2025-01", "end": "2025-03"}, title="Event", description="Description")
    portfolio.add_education(date="2024-09", institution="School", degree="Degree")
    site = portfolio.site_document()
    self.assertEqual(site["site"]["author"]["zh"], "示例")
    self.assertEqual(site["site"]["lastUpdateDate"], "2026-09-07")
    self.assertEqual(site["timeline"][0]["date"], {"start": "2025-01", "end": "2025-03"})
    self.assertEqual(site["education"][0]["date"], {"start": "2024-09"})
    with self.assertRaises(ValueError):
      portfolio.add_award(date="September 2025", title="Award")
    with self.assertRaises(ValueError):
      Portfolio(last_update_date="2026-02-30").site_document()

if __name__ == '__main__': unittest.main()
