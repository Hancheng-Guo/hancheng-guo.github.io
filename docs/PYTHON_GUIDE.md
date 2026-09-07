# 使用 Python 管理个人主页内容

这份教程面向不熟悉前端的内容维护者。日常添加、修改或删除项目时，不需要编辑 HTML、CSS 或 JavaScript；只需修改项目根目录的 `portfolio.py`，再运行一条生成命令。

## 1. 准备环境

安装 Python 3.10 或更新版本。在终端进入本项目根目录，然后确认 Python 可用：

```bash
python --version
```

Windows 如果无法识别 `python`，可尝试 `py`，并将后续命令中的 `python` 替换为 `py`。

## 2. 四条常用命令

所有命令都应在项目根目录运行：

```bash
# 只检查内容，不修改网站数据
python portfolio.py validate

# 检查通过后，生成网站读取的数据
python portfolio.py build

# 生成数据并启动本地预览
python portfolio.py preview

# 删除上一次构建生成的网页项目数据
python portfolio.py clean
```

执行 `preview` 后，在浏览器打开 `http://127.0.0.1:8000/`。按 `Ctrl+C` 停止预览。需要更换端口时使用：

```bash
python portfolio.py preview --port 8080
```

`clean` 删除生成的 JSON、首页、CV 页以及带有 Python 生成标记的项目详情页，不会删除 `portfolio.py`、项目图片或任何手写 HTML。运行 `python portfolio.py build` 即可全部重新生成并恢复。

根目录 `portfolio.py` 已包含当前网站的全部项目，是项目内容的唯一人工维护源。生成过程会先校验数据；校验失败时，现有 JSON 不会被覆盖。

## 3. 新增一个项目

先把封面和正文图片放入 `assets/images/`。推荐每个项目使用独立目录，例如：

```text
assets/images/my-robot/cover.jpg
assets/images/my-robot/result.jpg
```

然后打开根目录的 `portfolio.py`，在“在此处编写内容”区域加入：

```python
project = portfolio.add_project(
    title={"en": "My Robot", "zh": "我的机器人"},
    summary={
        "en": "A robot designed for underwater inspection.",
        "zh": "一款用于水下巡检的机器人。",
    },
    thumbnail="assets/images/my-robot/cover.jpg",
    tags=("Robotics", "Python"),
    featured=True,
    date=dict(
        start="2026-01",
        end="2026-06",
    ),
)

page = project.add_page(template="minimal")
page.add_heading({"en": "Overview", "zh": "项目概览"})
page.add_paragraph({
    "en": "Explain the problem, your role, and the outcome.",
    "zh": "说明项目问题、你的职责和最终成果。",
})
page.add_image(
    "assets/images/my-robot/result.jpg",
    alt={"en": "Robot test result", "zh": "机器人测试结果"},
    caption={"en": "Field test", "zh": "现场测试"},
)
page.add_github_link(
    url="https://github.com/your-name/my-robot",
    label={"en": "**Source code**", "zh": "**源代码**"},
)
```

构建器按添加顺序自动分配 `project1`、`project2`、`project3` 等 ID，并维护 `pages/projects/<id>.html`，用户无需填写路径或 ID。请不要随意调整已有项目的添加顺序，否则其 URL 会随编号变化。中英文内容使用 `{"en": "...", "zh": "..."}` 的形式填写；若传入单个字符串，两种语言会显示相同内容。

添加后依次执行：

```bash
python portfolio.py validate
python portfolio.py preview
```

在浏览器中确认英文、中文、桌面端和手机尺寸均显示正常，再提交代码。

## 4. 可用的页面内容模块

所有模块都通过 `page.add_*()` 添加，并按照调用顺序显示。

### 标题与正文

```python
page.add_heading({"en": "My Role", "zh": "我的职责"}, level=2)
page.add_paragraph({"en": "English text", "zh": "中文正文"})
```

### 单张图片

```python
page.add_image(
    "assets/images/my-robot/detail.jpg",
    alt={"en": "Mechanical structure", "zh": "机械结构"},
    caption={"en": "Prototype", "zh": "原型机"},
)
```

`alt` 是图片无法显示时的替代说明，也用于无障碍阅读，不能省略。

### 图片组

```python
page.add_gallery([
    {"src": "assets/images/my-robot/a.jpg", "alt": {"en": "Front", "zh": "正面"}},
    {"src": "assets/images/my-robot/b.jpg", "alt": {"en": "Side", "zh": "侧面"}},
])
```

### 列表与引用

```python
page.add_list([
    {"en": "Designed the controller", "zh": "设计控制器"},
    {"en": "Completed field tests", "zh": "完成现场测试"},
])

page.add_quote(
    {"en": "A short conclusion.", "zh": "一句简短结论。"},
    source={"en": "Test report", "zh": "测试报告"},
)
```

有序列表可传入 `ordered=True`。

### 成果指标

```python
page.add_metrics([
    {"label": {"en": "Accuracy", "zh": "精度"}, "value": "±5 mm"},
    {"label": {"en": "Runtime", "zh": "续航"}, "value": "4 h"},
])
```

指标应当真实、可验证，不要填写无法证明的数字。

### 视频与外部链接

```python
page.add_video(
    "https://example.com/demo.mp4",
    poster="assets/images/my-robot/video-cover.jpg",
    title={"en": "Demo video", "zh": "演示视频"},
)
page.add_github_link(
    url="https://github.com/your-name/my-robot",
    label={"en": "**Source code**", "zh": "**源代码**"},
)
page.add_doc_link(
    url="https://example.com/paper.pdf",
    label={"en": "Read _paper_", "zh": "阅读 _论文_"},
)
page.add_bilibili_link(
    url="https://www.bilibili.com/video/example",
    label={"en": "**Watch on Bilibili**", "zh": "**在哔哩哔哩观看**"},
)
page.add_youtube_link(
    url="https://www.youtube.com/watch?v=example",
    label={"en": "Watch _demo_", "zh": "观看 _演示_"},
)
```

四个链接方法都接受可选的 `label`：可传入单个 Markdown 字符串，或传入 `{"en": "...", "zh": "..."}` 为两种语言分别设置可见按钮文字。省略 `label` 时会使用对应的默认文字。外部链接必须使用 `https://`。

## 5. 修改或删除已有项目

已有项目均在根目录 `portfolio.py` 中通过 `add_project()` 和内容块函数定义。修改时直接找到对应代码；删除时移除该项目的整段构建代码。也可以临时调用：

```python
portfolio.remove_project("要删除的-project-id")
```

不要同时保留两个相同 `project_id`，校验器会将其报告为错误。

## 6. 页面模板

`project.add_page()` 支持四种模板：

- `minimal`：空白页面，最灵活，推荐初次使用。
- `case-study`：预置概览、职责、挑战、方法、结果和证据标题。
- `research`：预置摘要、研究问题、方法、实验、发现和局限标题。
- `competition`：预置目标、职责、系统设计、结果和奖项标题。

示例：

```python
page = project.add_page(template="research")
```

预置标题会先集中出现，因此需要完全控制内容顺序时请使用 `minimal`，并自行调用 `add_heading()`。

## 7. 常见错误

- “图片不存在”：检查路径大小写和扩展名，路径应从项目根目录开始，例如 `assets/images/a.jpg`。
- “Duplicate project id”：两个项目用了相同的 `project_id`，请删除或更名其中一个。
- “already has a page”：同一个项目调用了两次 `add_page()`；每个项目只能有一个详情页。
- “Invalid URL”：外部地址不是 `https://`。
- 中文乱码：用 UTF-8 编码保存 `portfolio.py`。
- 浏览器直接打开页面但项目没有显示：不要双击 HTML，请运行 `python portfolio.py preview`。

## 8. 发布前检查

```bash
python portfolio.py validate
python -m unittest discover -s tests/python -v
```

然后检查：主页项目卡片、每个详情页、语言切换、深浅主题、返回按钮、图片预览和移动端菜单。确认无误后，将 `portfolio.py`、生成的 `assets/data/projects.json` 和新增图片一并提交并推送到 GitHub Pages。

## 9. 文件职责

- `portfolio.py`：内容维护与命令入口，日常主要编辑此文件。
- `portfolio_content/`：生成器实现，一般用户无需修改。
- `assets/data/projects.json`：网页实际读取的生成结果；请勿手工修改，下一次构建会覆盖它。
- `assets/images/`：项目图片。
- `docs/PYTHON_GUIDE.md`：本教程。

## 10. 申请资料与简历模块

站点级资料同样写在 `portfolio.py`：`set_profile()` 保存姓名、简介、地点和联系方式；工作经历使用 `add_work_experience()`，论文使用 `add_publication(publication_type="journal"|"conference")`，奖项使用 `add_award()`。这些数据同时供首页一级板块和 `pages/cv.html` 使用。研究类项目详情仍可使用 `project.add_page(template="research")` 创建，它与站点级资料字段无关。

首页 Portfolio 与 CV 页左侧的个人信息共用 `set_profile()` 数据。推荐至少传入 `name`、`summary` 和 `email`，也可以传入 `location`。如需在首页显示 **Download CV** 按钮，为 `set_resume()` 分别提供中英文简历文件路径；未提供当前语言的 `url` 时不会生成按钮：

```python
portfolio.set_resume(
    label=dict(
        zh="下载简历",
        en="Download CV",
    ),
    url=dict(
        zh="assets/documents/简历测试.pdf",
        en="assets/documents/CVTest.pdf",
    ),
)
```

网站名称、作者和页脚文字在创建 `Portfolio` 时设置，并为所有显示文字提供中英文。所有显示文字都可以使用 Markdown；标题、标签等采用行内 Markdown，`add_paragraph()` 正文采用完整的 GitHub Flavored Markdown：

```python
portfolio = Portfolio(
    site_name=dict(
        zh="示例作品集",
        en="Example Portfolio",
    ),
    author=dict(
        zh="示例名称",
        en="Example Name",
    ),
    copyright_text=dict(
        zh="保留所有权利。",
        en="All rights reserved.",
    ),
    last_update_date="2026-09-07",
)
```

例如：

```python
page.add_paragraph(
    text=dict(
        zh=(
            "这是 **加粗内容**，也可以添加 [项目链接](https://example.com)。\n\n"
            "- 第一项\n"
            "- 第二项"
        ),
        en=(
            "This is **bold**, with a [project link](https://example.com).\n\n"
            "- First item\n"
            "- Second item"
        ),
    ),
)
```

项目额外约定 `_文字_` 表示下划线；标准斜体请写成 `*文字*`，`__文字__` 和 `**文字**` 均仍表示粗体。邮箱、网址、日期、图片路径和图标名称属于结构化参数，不按 Markdown 解析。联系方式当前可使用本地 SVG 图标名称 `github`。

Education、Work Experience、Awards & Scholarships 和 Timeline 的每一项都必须提供结构化日期；Publications 和 Projects 的日期可选。未给 Publication 日期时不会显示日期或多余分隔符；给 Project 日期时会显示在首页卡片 footer 的 `View Details` 同行右侧。无日期项目保留同样高度的隐藏日期槽，避免卡片尺寸或 hydration 发生跳动。单月使用 `date="YYYY-MM"`；时间段使用：

```python
date=dict(
    start="2025-10",
    end="2026-03",
)
```

构建器会拒绝非法月份或结束时间早于开始时间的输入。网页会根据当前语言将日期格式化为 `Oct 2025 – Mar 2026` 或 `2025年10月 – 2026年3月`。
