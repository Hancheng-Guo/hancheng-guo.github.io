# 使用 Python 管理个人主页内容

这份教程面向不熟悉前端的内容维护者。日常添加、修改或删除项目时，不需要编辑 HTML、CSS 或 JavaScript；只需修改项目根目录的 `portfolio.py`，再运行一条生成命令。

## 1. 准备环境

安装 Python 3.10 或更新版本。在终端进入本项目根目录，然后确认 Python 可用：

```bash
python --version
```

Windows 如果无法识别 `python`，可尝试 `py`，并将后续命令中的 `python` 替换为 `py`。

## 2. 三条常用命令

所有命令都应在项目根目录运行：

```bash
# 只检查内容，不修改网站数据
python portfolio.py validate

# 检查通过后，生成网站读取的数据
python portfolio.py build

# 生成数据并启动本地预览
python portfolio.py preview
```

执行 `preview` 后，在浏览器打开 `http://127.0.0.1:8000/`。按 `Ctrl+C` 停止预览。需要更换端口时使用：

```bash
python portfolio.py preview --port 8080
```

入口会先读取 `assets/data/projects.json` 中的全部现有项目，因此尚未添加代码时执行 `build` 不会把正式内容替换成示例。生成过程会先校验数据；校验失败时，原数据文件不会被覆盖。

## 3. 新增一个项目

先把封面和正文图片放入 `assets/images/`。推荐每个项目使用独立目录，例如：

```text
assets/images/my-robot/cover.jpg
assets/images/my-robot/result.jpg
```

然后打开根目录的 `portfolio.py`，在“在此处编写内容”区域加入：

```python
project = portfolio.add_project(
    project_id="my-robot",
    title={"en": "My Robot", "zh": "我的机器人"},
    summary={
        "en": "A robot designed for underwater inspection.",
        "zh": "一款用于水下巡检的机器人。",
    },
    thumbnail="assets/images/my-robot/cover.jpg",
    tags=("Robotics", "Python"),
    featured=True,
    year=2026,
)

page = portfolio.add_project_page("my-robot", template="minimal")
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
page.add_link("github", "https://github.com/your-name/my-robot")
```

`project_id` 必须是唯一的，建议只使用小写英文字母、数字和连字符。中英文内容使用 `{"en": "...", "zh": "..."}` 的形式填写；若传入单个字符串，两种语言会显示相同内容。

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
page.add_link("github", "https://github.com/your-name/my-robot")
page.add_link("paper", "https://example.com/paper.pdf", label={"en": "Paper", "zh": "论文"})
```

外部链接必须使用 `https://`。

## 5. 修改或删除已有项目

根入口每次都会先载入当前项目数据。删除已有项目可以写：

```python
portfolio.remove_project("要删除的-project-id")
```

当前 API 更适合“新增完整项目”。如果要大幅修改已有项目，建议先在 `portfolio.py` 中删除旧项目，再用相同的 `project_id` 重新添加：

```python
portfolio.remove_project("my-robot")
# 随后调用 add_project(...) 和 add_project_page(...) 重新创建
```

不要同时保留两个相同 `project_id`，校验器会将其报告为错误。

## 6. 页面模板

`add_project_page()` 支持四种模板：

- `minimal`：空白页面，最灵活，推荐初次使用。
- `case-study`：预置概览、职责、挑战、方法、结果和证据标题。
- `research`：预置摘要、研究问题、方法、实验、发现和局限标题。
- `competition`：预置目标、职责、系统设计、结果和奖项标题。

示例：

```python
page = portfolio.add_project_page("my-robot", template="research")
```

预置标题会先集中出现，因此需要完全控制内容顺序时请使用 `minimal`，并自行调用 `add_heading()`。

## 7. 常见错误

- “图片不存在”：检查路径大小写和扩展名，路径应从项目根目录开始，例如 `assets/images/a.jpg`。
- “Duplicate project id”：两个项目用了相同的 `project_id`，请删除或更名其中一个。
- “Unknown project”：`add_project_page()` 中的 ID 与 `add_project()` 不一致。
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
- `assets/data/projects.json`：网页实际读取的生成结果，不建议手工与 Python 内容同时维护。
- `assets/images/`：项目图片。
- `docs/PYTHON_GUIDE.md`：本教程。
