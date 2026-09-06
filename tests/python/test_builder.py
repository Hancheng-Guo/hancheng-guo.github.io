import json
import unittest
from portfolio_content import Portfolio
from portfolio_content.validators import validate_document

class BuilderTests(unittest.TestCase):
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

if __name__ == '__main__': unittest.main()
