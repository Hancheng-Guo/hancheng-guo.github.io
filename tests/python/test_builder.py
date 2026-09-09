import json
import importlib.util
import unittest
from pathlib import Path
from portfolio_content import Portfolio
from portfolio_content.static_renderer import format_date_range, markdown_inline, pretty_html, render_cv, render_home, render_project
from portfolio_content.validators import validate_document
from portfolio_content.cli import clean_generated_output, clean_generated_pages

class BuilderTests(unittest.TestCase):
  def test_translation_json_has_no_duplicate_keys(self):
    def reject_duplicates(pairs):
      result = {}
      for key, value in pairs:
        if key in result:
          raise ValueError(f"Duplicate translation key: {key}")
        result[key] = value
      return result

    for path in (Path("lang/en.json"), Path("lang/zh.json")):
      with self.subTest(path=path):
        json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)

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

  def test_static_html_is_readable_indented_and_deterministic(self):
    import tempfile
    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
      portfolio = Portfolio()
      portfolio.add_project(title={"en": "**Demo**", "zh": "演示"}, summary="Summary", thumbnail="assets/images/Avatar.jpg").add_page(template="minimal").add_paragraph("Body")
      portfolio.write_static_fallbacks(root=first)
      portfolio.write_pages(root=first)
      first_build = {relative: (Path(first) / relative).read_bytes() for relative in ("index.html", "pages/cv.html", "pages/projects/project1.html")}
      portfolio.write_static_fallbacks(root=first)
      portfolio.write_pages(root=first)
      portfolio.write_static_fallbacks(root=second)
      portfolio.write_pages(root=second)
      for relative in ("index.html", "pages/cv.html", "pages/projects/project1.html"):
        left = (Path(first) / relative).read_text(encoding="utf-8")
        right = (Path(second) / relative).read_text(encoding="utf-8")
        self.assertEqual((Path(first) / relative).read_bytes(), first_build[relative])
        self.assertEqual(left, right)
        self.assertNotRegex(left, r"[ \t]+\n")
        self.assertIn("\n  <head>", left)
        self.assertIn("\n    <meta ", left)
        self.assertIn("\n  <body", left)
        self.assertIn("\n    <nav>", left)
        self.assertRegex(left, r"\n    <title>[^\n]+</title>")
        self.assertNotRegex(left, r"<title>[^\n]*\n\s*</title>")
        self.assertRegex(left, r"\n\s+<h[1-3][^>]*>[^\n]+</h[1-3]>")
        self.assertNotRegex(left, r"<h[1-3][^>]*>[^<\n]*\n\s+</h[1-3]>")
        self.assertRegex(left, r"\n    <script[^>]*>[^\n]*</script>\n")
        self.assertRegex(left, r"\n\s+<div class=\"nav-actions\">\n")
        self.assertRegex(left, r"\n\s+<button [^\n]+>\n")
        if relative.endswith("project1.html"):
          self.assertIn("<strong>Demo</strong>", left)
        self.assertIn('<script type="module"', left)

  def test_project_card_uses_a_plain_detail_cue_and_a_keyboard_operable_card(self):
    portfolio = Portfolio()
    portfolio.add_project(title="Demo", summary="Summary", thumbnail="assets/images/Avatar.jpg").add_page(template="minimal")
    home = render_home(portfolio)
    self.assertIn('<article class="card project-card-detail" tabindex="0" role="link" aria-label="View Details: Demo"', home)
    self.assertIn('<span class="project-link">View Details', home)
    self.assertNotIn('<a class="project-link"', home)

  def test_project_without_add_page_has_a_non_operable_card_and_generates_no_detail_page(self):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      portfolio = Portfolio()
      without_page = portfolio.add_project(project_id="card-only", title="Card only", summary="Summary", thumbnail="assets/images/Avatar.jpg")
      with_page = portfolio.add_project(project_id="with-page", title="With page", summary="Summary", thumbnail="assets/images/Avatar.jpg")
      with_page.add_page(template="minimal")
      self.assertFalse(without_page.data["hasDetailPage"])
      self.assertTrue(with_page.data["hasDetailPage"])
      home = render_home(portfolio)
      self.assertIn('<article class="card project-card-coming-soon" tabindex="0"><div class="project-thumbnail-wrapper"><img class="project-thumbnail"', home)
      title_position = home.index('<h3>Card only</h3>')
      card_only = home[home.rfind('<article', 0, title_position):home.index('</article>', title_position)]
      self.assertIn('tabindex="0"', card_only)
      self.assertNotIn('role="link"', card_only)
      self.assertNotIn('data-project-href=', card_only)
      self.assertIn('<span class="project-link project-status">Details Coming Soon ...</span>', card_only)
      self.assertNotIn('View Details', card_only)
      self.assertNotIn('chevron-right', card_only)
      stale = Path(folder) / "pages" / "projects" / "card-only.html"
      stale.parent.mkdir(parents=True)
      stale.write_text("<!-- Generated by portfolio.py; do not edit. -->", encoding="utf-8")
      pages = portfolio.write_pages(root=folder)
      self.assertEqual([page.name for page in pages], ["with-page.html"])
      self.assertFalse(stale.exists())

  def test_pretty_html_preserves_inline_and_raw_payloads(self):
    script = 'const comparison = left > right; const markup = "<tag data-value=\'>\'>";\n  keepThisIndent();'
    style = '.example::before { content: ">"; }\n  .example { white-space: pre; }'
    source = f'<!DOCTYPE html><html><head><title>Example title</title><script>{script}</script><style>{style}</style></head><body><nav><a href="/x?value=>"><span>Link</span></a><button type="button"><span>Go</span></button></nav><main><h2>Simple <strong>heading</strong></h2><p>Inline <em>text</em> and <a href="https://example.com?a=>b">link</a>.</p><pre>  preserve\n    every space</pre></main></body></html>'
    formatted = pretty_html(source)
    self.assertIn('<title>Example title</title>', formatted)
    self.assertIn('<h2>Simple <strong>heading</strong></h2>', formatted)
    self.assertIn('<p>Inline <em>text</em> and <a href="https://example.com?a=>b">link</a>.</p>', formatted)
    self.assertIn(f'<script>{script}</script>', formatted)
    self.assertIn(f'<style>{style}</style>', formatted)
    self.assertIn('<pre>  preserve\n    every space</pre>', formatted)
    self.assertNotRegex(formatted, r"[ \t]+\n")

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

  def test_clean_removes_generated_home_and_cv_but_preserves_manual_html(self):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      root = Path(folder)
      portfolio = Portfolio()
      portfolio.write_static_fallbacks(root=root)
      manual = root / "manual.html"
      manual.write_text("manual", encoding="utf-8")
      removed = clean_generated_pages(root)
      self.assertEqual(set(removed), {root / "index.html", root / "pages" / "cv.html"})
      self.assertTrue(manual.exists())

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

  def test_project_heading_level_is_limited_to_two_through_five(self):
    portfolio = Portfolio()
    project = portfolio.add_project(title="Demo", summary="Summary", thumbnail="assets/images/Avatar.jpg")
    page = project.add_page(template="minimal")
    for level in (2, 3, 4, 5):
      page.add_heading("Heading", level=level)
    for level in (1, 6, 2.5, True, "3"):
      with self.assertRaises(ValueError):
        page.add_heading("Invalid", level=level)
    html = render_project(portfolio, project.data)
    for level in (2, 3, 4, 5):
      self.assertIn(f'<h{level} class="project-content-heading">Heading</h{level}>', html)
    self.assertNotIn("<h1>", html)
    self.assertNotIn("<h6>", html)

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
    self.assertEqual(site["education"][0]["date"], {"start": "2024-09", "end": "2024-09"})
    with self.assertRaises(ValueError):
      portfolio.add_award(date="September 2025", title="Award")
    with self.assertRaises(ValueError):
      Portfolio(last_update_date="2026-02-30").site_document()

  def test_education_uses_a_structured_three_line_format_with_legacy_compatibility(self):
    portfolio = Portfolio()
    portfolio.add_education(
      date={"start": "2022-04", "end": "2026-06"},
      position={"en": "Ph.D. in **Robotics**", "zh": "机器人学博士"},
      institute={"en": "ETH Zurich", "zh": "苏黎世联邦理工学院"},
      location={"en": "Switzerland", "zh": "瑞士"},
      detail={"en": "Research focus: *Legged robotics*", "zh": "研究方向：**足式机器人**"},
    )
    item = portfolio.site_document()["education"][0]
    self.assertEqual(item["date"], {"start": "2022-04", "end": "2026-06"})
    self.assertEqual(item["position"]["en"], "Ph.D. in **Robotics**")
    html = render_cv(portfolio)
    expected = '<article class="content-entry education-entry"><h3 class="education-heading"><strong>Ph.D. in <strong>Robotics</strong></strong>, ETH Zurich, Switzerland</h3><time class="entry-date">Apr 2022 – Jun 2026</time><p class="education-detail">Research focus: <em>Legged robotics</em></p></article>'
    self.assertIn(expected, html)
    self.assertLess(html.index('education-heading'), html.index('entry-date'))
    self.assertLess(html.index('entry-date'), html.index('education-detail'))

    optional = Portfolio()
    optional.add_education(date="2024-09", position="M.Sc. & <Robotics>", institute="Example Institute")
    optional_html = render_cv(optional)
    self.assertIn('<strong>M.Sc. &amp; &lt;Robotics&gt;</strong>, Example Institute', optional_html)
    self.assertNotIn('Example Institute, </h3>', optional_html)
    self.assertNotIn('education-detail', optional_html)

    legacy = Portfolio()
    legacy.add_education(date="2024-09", institution="Legacy University", degree="Legacy Degree")
    legacy_item = legacy.site_document()["education"][0]
    self.assertEqual(legacy_item["position"], {"en": "Legacy Degree", "zh": "Legacy Degree"})
    self.assertEqual(legacy_item["institute"], {"en": "Legacy University", "zh": "Legacy University"})
    self.assertIn('<strong>Legacy Degree</strong>, Legacy University', render_cv(legacy))
    invalid = Portfolio()
    invalid.education.append({"date": {"start": "2024-09"}})
    self.assertIn('必须提供 position', invalid.validate(root='.').format())

  def test_ongoing_dates_and_work_experience_three_line_format(self):
    self.assertEqual(format_date_range({"start": "2022-04"}), "Since Apr 2022")
    self.assertEqual(format_date_range({"start": "2022-04"}, "zh"), "2022年4月 至今")
    self.assertEqual(format_date_range("2022-04"), "Apr 2022")
    self.assertEqual(format_date_range({"start": "2022-04", "end": "2022-04"}), "Apr 2022")
    portfolio = Portfolio()
    portfolio.add_project(title="Project", summary="Summary", thumbnail="assets/images/Avatar.jpg", date={"start": "2024-01"})
    portfolio.add_timeline_event(date={"start": "2024-01"}, title="Timeline", description="Detail")
    portfolio.add_education(date={"start": "2024-01"}, position="Student")
    portfolio.add_work_experience(
      date={"start": "2024-01"}, position="Robotics **Engineer**", company="Example Co.", location="Zurich", detail="Built *robots*"
    )
    portfolio.add_publication(publication_type="journal", date={"start": "2024-01"}, title="Paper", venue="Venue")
    portfolio.add_award(date={"start": "2024-01"}, title="Award")
    self.assertEqual(portfolio.add_award(date="2024-02", title="Single month").awards[-1]["date"], {"start": "2024-02", "end": "2024-02"})
    home, cv = render_home(portfolio), render_cv(portfolio)
    self.assertGreaterEqual(home.count("Since Jan 2024"), 3)  # project, publication, timeline
    self.assertGreaterEqual(cv.count("Since Jan 2024"), 4)  # education, work, publication, award
    expected = '<article class="content-entry work-entry"><h3 class="work-heading"><strong>Robotics <strong>Engineer</strong></strong>, Example Co., Zurich</h3><time class="entry-date">Since Jan 2024</time><p class="work-detail">Built <em>robots</em></p></article>'
    self.assertIn(expected, cv)
    with self.assertRaises(TypeError):
      Portfolio().add_work_experience(date="2024-01", title="Legacy role")
    rejected = Portfolio()
    rejected.work_experience.append({"date": {"start": "2024-01"}, "position": "Role", "title": "Rejected"})
    self.assertIn('workExperience[0].title 已不支持', rejected.validate(root='.').format())
    optional = Portfolio()
    optional.add_work_experience(date={"start": "2024-01"}, position="Role")
    optional_html = render_cv(optional)
    self.assertNotIn('work-detail', optional_html)
    self.assertNotIn('Role, </h3>', optional_html)

  def test_long_form_markdown_lists_are_safe_and_do_not_change_plain_details(self):
    portfolio = Portfolio()
    items = "- **Bold** item\n- *Italic* [safe](https://example.com) [bad](javascript:alert(1)) <script>alert(1)</script>"
    portfolio.add_education(date={"start": "2024-01"}, position="Student", detail=items)
    portfolio.add_work_experience(date={"start": "2024-01"}, position="Engineer", detail=items)
    portfolio.add_timeline_event(date={"start": "2024-01"}, title="Event", description=items)
    project = portfolio.add_project(title="Project", summary="Summary", thumbnail="assets/images/Avatar.jpg")
    project.add_page(template="minimal").add_paragraph(items)
    cv, home, project_html = render_cv(portfolio), render_home(portfolio), render_project(portfolio, project.data)
    for html in (cv, home, project_html):
      self.assertIn('<ul>', html)
      self.assertIn('<li><strong>Bold</strong> item</li>', html)
      self.assertIn('<em>Italic</em> <a href="https://example.com">safe</a>', html)
      self.assertNotIn('javascript:', html)
      self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)
    plain = Portfolio()
    plain.add_education(date={"start": "2024-01"}, position="Student", detail="A - plain inline hyphen")
    plain_html = render_cv(plain)
    self.assertIn('<p class="education-detail">A - plain inline hyphen</p>', plain_html)
    self.assertNotIn('<ul>', plain_html)

  def test_optional_publication_date_and_markdown_venue(self):
    portfolio = Portfolio()
    portfolio.add_publication(
      publication_type="journal",
      title={"en": "A **paper**", "zh": "一篇 **论文**"},
      venue={"en": "*Nature* [site](https://example.com)", "zh": "*期刊*"},
    )
    home = render_home(portfolio)
    cv = render_cv(portfolio)
    for html in (home, cv):
      self.assertIn("<em>Nature</em>", html)
      self.assertIn('<a href="https://example.com">site</a>', html)
      self.assertNotIn('class="entry-date"', html)
      self.assertNotIn('class="entry-separator"', html)

  def test_optional_project_date_is_rendered_only_when_present(self):
    portfolio = Portfolio()
    portfolio.add_project(
      title="Dated",
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
      date={"start": "2025-10", "end": "2026-03"},
    )
    portfolio.add_project(
      title="Undated",
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
    )
    html = render_home(portfolio)
    self.assertEqual(html.count('class="project-date"'), 2)
    self.assertIn("Oct 2025 – Mar 2026", html)
    self.assertIn('<time class="project-date" hidden></time>', html)
    self.assertTrue(portfolio.validate(root=".").ok)

  def test_favicon_is_optional_on_all_static_pages(self):
    without = Portfolio()
    project_without = without.add_project(
      title="Demo",
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
    )
    self.assertNotIn('rel="icon"', render_home(without))
    self.assertNotIn('rel="icon"', render_cv(without))
    self.assertNotIn('rel="icon"', render_project(without, project_without.data))
    self.assertNotIn("favicon", without.site_document()["site"])

    configured = Portfolio(favicon="assets/images/Avatar.jpg")
    project_configured = configured.add_project(
      title="Demo",
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
    )
    self.assertIn('href="assets/images/Avatar.jpg"', render_home(configured))
    self.assertIn('href="../assets/images/Avatar.jpg"', render_cv(configured))
    self.assertIn('href="../../assets/images/Avatar.jpg"', render_project(configured, project_configured.data))
    missing = Portfolio(favicon="assets/icons/missing.svg")
    self.assertFalse(missing.validate(root=".").ok)

  def test_profile_images_are_explicit_optional_assets(self):
    without = Portfolio()
    without.set_profile(name="No images")
    home_without = render_home(without)
    cv_without = render_cv(without)
    self.assertNotIn('avatar-container', home_without)
    self.assertNotIn('bg-decoration', home_without)
    self.assertNotIn('class="avatar"', home_without)
    self.assertNotIn('data-hero-background', home_without)
    self.assertNotIn('Portfolio-01-3.png', home_without)
    self.assertNotIn('resume-avatar-wrap', cv_without)
    self.assertNotIn('resume-profile-avatar', cv_without)
    self.assertNotIn('Avatar.jpg', cv_without)
    self.assertNotIn('avatar', without.site_document()['profile'])
    self.assertNotIn('hero_background', without.site_document()['profile'])

    configured = Portfolio()
    configured.set_profile(
      name="Images configured",
      avatar="assets/images/Avatar.jpg",
      hero_background="assets/images/Portfolio-01-3.png",
    )
    home_configured = render_home(configured)
    cv_configured = render_cv(configured)
    self.assertIn('class="avatar-container"', home_configured)
    self.assertIn('class="bg-decoration"', home_configured)
    self.assertIn('src="assets/images/Avatar.jpg"', home_configured)
    self.assertIn('data-hero-background="true"', home_configured)
    self.assertIn('url(&quot;../images/Portfolio-01-3.png&quot;)', home_configured)
    self.assertIn('class="resume-avatar-wrap"', cv_configured)
    self.assertIn('src="../assets/images/Avatar.jpg"', cv_configured)
    self.assertEqual(configured.site_document()['profile']['avatar'], 'assets/images/Avatar.jpg')
    self.assertEqual(configured.site_document()['profile']['hero_background'], 'assets/images/Portfolio-01-3.png')
    self.assertTrue(configured.validate(root='.').ok)

    configured.set_profile(avatar=None, hero_background=None)
    self.assertNotIn('avatar-container', render_home(configured))
    self.assertNotIn('data-hero-background', render_home(configured))

  def test_contact_renders_from_a_safe_local_svg_path(self):
    portfolio = Portfolio()
    portfolio.add_contact(
      label={"en": "ORCID", "zh": "ORCID 学术档案"},
      icon="assets/icons/orcid.svg",
      url="https://orcid.org/0009-0005-2213-1604",
    )
    document = portfolio.site_document()
    self.assertEqual(document["contacts"][0]["url"], "https://orcid.org/0009-0005-2213-1604")
    self.assertEqual(document["contacts"][0]["icon"], "assets/icons/orcid.svg")
    self.assertEqual(document["contacts"][0]["label"], {"en": "ORCID", "zh": "ORCID 学术档案"})
    for html in (render_home(portfolio), render_cv(portfolio)):
      self.assertIn('class="svg-icon svg-icon--inline"', html)
      self.assertNotIn('icon-orcid', html)
      self.assertIn('href="https://orcid.org/0009-0005-2213-1604"', html)
      self.assertIn('target="_blank" rel="noopener noreferrer"', html)
      self.assertIn('aria-label="ORCID"', html)
      self.assertNotIn('<?xml', html)
      self.assertNotIn('Uploaded to: SVG Repo', html)

  def test_contact_icon_must_be_a_repository_local_existing_svg(self):
    for icon, expected in (
      ("orcid", "必须使用 .svg 文件"),
      ("https://example.com/icon.svg", "不允许远程 URL"),
      ("/assets/icons/orcid.svg", "不允许绝对路径"),
      (r"C:\\assets\\icons\\orcid.svg", "不允许绝对路径"),
      ("../outside.svg", "仓库内 SVG"),
      ("assets/icons/orcid.png", "必须使用 .svg 文件"),
      ("assets/icons/missing.svg", "仓库内 SVG"),
    ):
      portfolio = Portfolio()
      portfolio.add_contact(label="Test", icon=icon, url="https://example.com")
      report = portfolio.validate(root=".")
      self.assertFalse(report.ok, icon)
      self.assertIn(expected, report.format(), icon)

    import tempfile
    with tempfile.TemporaryDirectory() as folder:
      icon_path = Path(folder) / "assets/icons/unsafe.svg"
      icon_path.parent.mkdir(parents=True)
      icon_path.write_text('<svg><script>alert(1)</script></svg>', encoding="utf-8")
      portfolio = Portfolio()
      portfolio.add_contact(label="Unsafe", icon="assets/icons/unsafe.svg", url="https://example.com")
      self.assertIn("不允许的内联内容", portfolio.validate(root=folder).format())

  def test_profile_name_and_empty_sections_follow_visible_content(self):
    empty = Portfolio()
    home = render_home(empty)
    cv = render_cv(empty)
    self.assertIn('id="profile"', home)
    self.assertIn('href="index.html#profile"', home)
    self.assertIn('data-i18n="nav.profile">Profile', home)
    self.assertIn('id="top"', home)  # Legacy #top links remain valid.

    navigable = Portfolio()
    project = navigable.add_project(title="Demo", summary="Summary", thumbnail="assets/images/Avatar.jpg")
    project.add_page(template="minimal")
    for html, href in (
      (render_home(navigable), 'index.html#projects'),
      (render_cv(navigable), '../index.html#projects'),
      (render_project(navigable, project.data), '../../index.html#projects'),
    ):
      self.assertIn(f'<a href="{href}" data-i18n="nav.projects">Projects</a>', html)
      self.assertNotIn('data-i18n="nav.project"', html)
    for section_id, title in (("projects", "Projects"), ("publications", "Publications"), ("timeline", "Timeline")):
      self.assertNotIn(f'id="{section_id}"', home)
      self.assertNotIn(f'>{title}<', home)
      self.assertNotIn(f'#{section_id}', home)
    for title in ("Education", "Work Experience", "Publications", "Tech Stack", "Awards &amp; Scholarships"):
      self.assertNotIn(f'>{title}<', cv)

    draft_only = Portfolio()
    draft_only.add_project(title="Draft", summary="Hidden", thumbnail="assets/images/Avatar.jpg", status="draft")
    self.assertNotIn('id="projects"', render_home(draft_only))
    self.assertNotIn('#projects', render_home(draft_only))

    journals = Portfolio()
    journals.add_publication(publication_type="journal", title="Journal", venue="Venue")
    journal_home, journal_cv = render_home(journals), render_cv(journals)
    for html in (journal_home, journal_cv):
      self.assertIn('Journal Articles', html)
      self.assertNotIn('Conference Papers', html)

    singles = Portfolio()
    singles.add_timeline_event(date="2025-01", title="Timeline", description="Visible")
    singles.add_education(date="2024-01", institution="School", degree="Degree")
    singles.add_work_experience(date="2024-01", position="Role", company="Org")
    singles.add_tech_group(title="Tools", items=[{"name": "Python"}])
    singles.add_award(date="2024-01", title="Award")
    self.assertIn('id="timeline"', render_home(singles))
    single_cv = render_cv(singles)
    for title in ("Education", "Work Experience", "Tech Stack", "Awards &amp; Scholarships"):
      self.assertIn(f'>{title}<', single_cv)

  def test_profile_image_paths_are_validated(self):
    missing_avatar = Portfolio(); missing_avatar.set_profile(avatar='assets/images/missing-avatar.png')
    self.assertIn('profile.avatar 文件不存在', missing_avatar.validate(root='.').format())
    missing_background = Portfolio(); missing_background.set_profile(hero_background='assets/images/missing-hero.png')
    self.assertIn('profile.hero_background 文件不存在', missing_background.validate(root='.').format())
    remote = Portfolio(); remote.set_profile(avatar='https://example.com/avatar.png')
    self.assertIn('profile.avatar 必须是本地文件', remote.validate(root='.').format())

  def test_typed_link_methods_cover_all_supported_icons(self):
    portfolio = Portfolio()
    project = portfolio.add_project(
      title="Demo",
      summary="Summary",
      thumbnail="assets/images/Avatar.jpg",
    )
    page = project.add_page(template="minimal")
    # First cover every default presentation, then verify each method carries
    # through an explicit (including bilingual Markdown) label.
    page.add_github_link(url="https://github.com/example/default")
    page.add_doc_link(url="https://example.com/default.pdf")
    page.add_bilibili_link(url="https://www.bilibili.com/video/default")
    page.add_youtube_link(url="https://www.youtube.com/watch?v=default")
    page.add_github_link(url="https://github.com/example/repo", label={"en": "**Source**", "zh": "**源码**"})
    page.add_doc_link(url="https://example.com/doc.pdf", label={"en": "Read _docs_", "zh": "阅读 _文档_"})
    page.add_bilibili_link(url="https://www.bilibili.com/video/example", label={"en": "**Watch**", "zh": "**观看**"})
    page.add_youtube_link(url="https://www.youtube.com/watch?v=example", label={"en": "Video _demo_", "zh": "视频 _演示_"})
    self.assertFalse(hasattr(page, "add_link"))
    self.assertEqual(
      [link["type"] for link in project.data["links"]],
      ["github", "techDoc", "bilibili", "youtube"] * 2,
    )
    html = render_project(portfolio, project.data)
    for icon in ("github", "file-pdf", "bilibili", "youtube"):
      self.assertIn(f"icon-{icon}", html)
    self.assertIn("<strong>Source</strong>", html)
    self.assertIn("Read <u>docs</u>", html)
    self.assertIn("<strong>Watch</strong>", html)
    self.assertIn("Video <u>demo</u>", html)
    self.assertEqual(project.data["links"][4]["label"]["zh"], "**源码**")
    self.assertEqual(project.data["links"][5]["label"]["zh"], "阅读 _文档_")
    self.assertEqual(project.data["links"][6]["label"]["zh"], "**观看**")
    self.assertEqual(project.data["links"][7]["label"]["zh"], "视频 _演示_")
    for default_label in (">Code<", ">Docs<", ">Bilibili<", ">YouTube<"):
      self.assertIn(default_label, html)

  def test_static_output_contains_content_without_loading_shell(self):
    portfolio = Portfolio()
    for number in range(9):
      portfolio.add_timeline_event(
        date=f"2025-{number + 1:02d}",
        title=f"Event {number + 1}",
        description="Description",
      )
    project = portfolio.add_project(
      title="**Static** project",
      summary="Readable before JavaScript",
      thumbnail="assets/images/Avatar.jpg",
    )
    project.add_page(template="minimal").add_paragraph("Body with _underline_ and *italic*.")
    home = render_home(portfolio)
    detail = render_project(portfolio, project.data)
    self.assertEqual(home.count("<main>"), 1)
    self.assertIn("<strong>Static</strong> project", home)
    self.assertEqual(home.count("timeline-extra"), 1)
    self.assertIn("<u>underline</u>", detail)
    self.assertIn("<em>italic</em>", detail)
    self.assertNotIn("Loading project", detail)
    self.assertIn('class="svg-icon motion-link-arrow link-chevron chevron-left svg-icon--inline', detail)

  def test_page_fields_normalize_filter_reorder_and_keep_profile(self):
    portfolio = Portfolio()
    portfolio.add_project(title="Project", summary="Summary", thumbnail="assets/images/Avatar.jpg")
    portfolio.add_publication(publication_type="journal", title="Journal", venue="Venue")
    portfolio.add_timeline_event(date="2025-01", title="Timeline", description="Event")
    portfolio.add_education(date="2020-01", position="Education")
    portfolio.add_work_experience(date="2021-01", position="Work")
    portfolio.add_tech_group(title="Skills", items=[{"name": "Python"}])
    portfolio.add_award(date="2022-01", title="Award")

    portfolio.set_home_field(["publications"])
    self.assertIs(portfolio.set_home_field([" TIMELINE ", "PROJECTS"]), portfolio)
    portfolio.set_cv_field(["publications"])
    self.assertIs(portfolio.set_cv_field(["work_experience", "PROFILE", "Awards-and-scholarships", "education"]), portfolio)
    self.assertEqual(portfolio.home_fields, ("profile", "timeline", "projects"))
    self.assertEqual(portfolio.cv_fields, ("profile", "work experience", "awards and scholarships", "education"))
    self.assertEqual(portfolio.site_document()["layout"], {
      "homeFields": ["profile", "timeline", "projects"],
      "cvFields": ["profile", "work experience", "awards and scholarships", "education"],
    })

    home, cv = render_home(portfolio), render_cv(portfolio)
    self.assertLess(home.index('id="timeline"'), home.index('id="projects"'))
    self.assertLess(home.index('data-i18n="nav.timeline"'), home.index('data-i18n="nav.projects"'))
    self.assertNotIn('id="publications"', home)
    self.assertNotIn('#publications', home)
    self.assertLess(cv.index('resume-work'), cv.index('resume-awards'))
    self.assertLess(cv.index('resume-awards'), cv.index('resume-education'))
    self.assertNotIn('resume-journals', cv)
    self.assertIn('resume-sidebar', cv)

  def test_page_field_validation_rejects_ambiguous_layouts(self):
    portfolio = Portfolio()
    for fields in ("projects", ("projects", "projects"), ("unknown",), (1,)):
      with self.subTest(fields=fields):
        with self.assertRaises(ValueError):
          portfolio.set_home_field(fields)
    with self.assertRaises(ValueError):
      portfolio.set_cv_field(("education", None))

  def test_markdown_escapes_html_and_preserves_snake_case(self):
    rendered = markdown_inline("snake_case _underlined_ <script>alert(1)</script>")
    self.assertIn("snake_case", rendered)
    self.assertIn("<u>underlined</u>", rendered)
    self.assertNotIn("<script>", rendered)

if __name__ == '__main__': unittest.main()
