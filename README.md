# Hancheng Guo Homepage

一个由 Python 内容配置生成的双语静态个人主页，包含 Profile、Projects、Publications、Timeline 和独立 CV 页面。网站不需要后端或数据库，可直接部署到 GitHub Pages；构建后的核心内容在禁用 JavaScript 时仍可阅读。

![首页效果](assets/images/docs/home.png)

本项目早期版本基于 [Lain-Ego0/Lain-Ego0.github.io](https://github.com/Lain-Ego0/Lain-Ego0.github.io) 开发，其基础页面、视觉风格和前端实现为本项目提供了重要参考。当前仓库已独立维护，仓库关系变化不影响原项目的贡献归属。

## 你可以用它做什么

- 在一个 `portfolio.py` 中维护中英文个人资料、履历、论文、项目和时间线。
- 为项目选择“仅首页卡片”或“完整详情页”两种发布状态。
- 生成可直接部署的首页、CV、项目页和浏览器运行所需的 JSON。
- 使用本地主题、语言切换、响应式布局、项目图片预览和键盘交互。
- 在提交前校验日期、URL、本地资源和内容结构。

如果你只是要更新本站内容，从下面的“第一次修改”开始；如果要了解全部字段和内容块，直接阅读 [Portfolio Python 工具手册](docs/PYTHON_GUIDE.md)。

## 第一次运行

需要 Python 3.10 或更高版本：

```bash
git clone https://github.com/Hancheng-Guo/hancheng-guo.github.io.git
cd hancheng-guo.github.io

python portfolio.py validate
python portfolio.py preview
```

打开 <http://127.0.0.1:8000/>，按 `Ctrl+C` 停止预览。`preview` 会先构建网站，因此通常不需要提前单独运行 `build`。

## 第一次修改

1. 编辑根目录的 [`portfolio.py`](portfolio.py)。
2. 将引用的图片、PDF 等资源放入 `assets/` 对应目录。
3. 运行 `python portfolio.py validate` 修正内容或路径错误。
4. 运行 `python portfolio.py preview`，检查英文/中文、深色/浅色及桌面/移动布局。
5. 提交源码和重新生成的 HTML、JSON。

不要直接编辑 `index.html`、`pages/cv.html`、`pages/projects/*.html` 或 `assets/data/*.json`；它们会在下次构建时被覆盖。

## 项目卡片与详情页

`portfolio.add_project()` 始终创建首页项目卡片。是否调用返回对象的 `add_page()`，决定该项目是否有详情页：

| 配置方式 | 首页卡片 | 详情页 |
|---|---|---|
| 只调用 `add_project()` | 显示 “Details Coming Soon ...”；可聚焦，但不可点击或键盘激活，也不显示手型光标 | 不生成 |
| 再调用 `project.add_page()` | 显示 “View Details”；整张卡片支持点击、Enter 和 Space | 生成 `pages/projects/<project_id>.html` |

```python
project = portfolio.add_project(
    project_id="robot-demo",
    title=dict(zh="机器人项目", en="Robot Project"),
    summary=dict(zh="项目简介。", en="Project summary."),
    thumbnail="assets/images/robot-demo/cover.jpg",
)

# 准备好详情内容后再添加这一行：
page = project.add_page(template="minimal")
page.add_paragraph(dict(zh="项目正文。", en="Project details."))
```

移除已有的 `add_page()` 后再次构建，会删除该项目此前生成且带生成标记的详情页；手工 HTML 不会被删除。完整项目 API、模板和内容块见[工具手册的 Projects 章节](docs/PYTHON_GUIDE.md#projects)。

## 常用命令

```bash
# 只检查内容、格式与本地资源
python portfolio.py validate

# 校验并生成完整静态网站
python portfolio.py build

# 构建并启动本地服务器（默认 127.0.0.1:8000）
python portfolio.py preview
# 构建并启动本地服务器（指定端口8080）
python portfolio.py preview --port 8080

# 删除带生成标记的 HTML 与生成的 JSON
python portfolio.py clean
```

`clean` 不会删除 `portfolio.py`、构建器或静态资源；随后运行 `build` 即可恢复生成结果。构建采用临时文件和原子替换，校验失败时不会覆盖已有项目数据。

## 内容源与生成结果

人工维护：

- `portfolio.py`：全部站点内容与页面配置；
- `assets/images/`、`assets/documents/`：内容引用的图片和文档；

`python portfolio.py build` 生成：

- `index.html`：静态首页；
- `pages/cv.html`：静态 CV；
- `pages/projects/*.html`：仅包含调用过 `add_page()` 的项目；
- `assets/data/site.json`：站点、履历和联系方式；
- `assets/data/projects.json`：项目卡片、正文块和链接。

意图修改界面的开发者：

- `lang/`：界面级中英文文案；
- `assets/css/`、`assets/js/`：页面样式与交互实现。

## 项目结构

```text
.
├── portfolio.py                 # 内容配置与命令入口
├── portfolio_content/           # 数据模型、校验器与静态渲染器
├── docs/PYTHON_GUIDE.md         # 内容维护与 Python API 手册
├── index.html                   # 生成的首页
├── pages/
│   ├── cv.html                  # 生成的 CV
│   └── projects/                # 按需生成的项目详情页
├── assets/
│   ├── css/                     # 主题、组件和响应式样式
│   ├── data/                    # 生成的 JSON
│   ├── documents/               # CV 等下载文件
│   ├── icons/                   # 本地 SVG 图标
│   ├── images/                  # 头像、项目图片和文档截图
│   ├── js/                      # 浏览器入口与功能模块
│   └── vendor/                  # 本地前端依赖
├── lang/                        # 界面级中英文文案
├── schemas/                     # 生成数据的 JSON Schema
└── tests/                       # Python 与真实浏览器回归测试
```

## 测试与发布前检查

Python 测试不需要额外依赖：

```bash
python -m unittest discover -s tests/python -v
```

浏览器回归位于 `tests/browser/`，需要 Node.js、Playwright 和 Chromium/Edge。它们覆盖静态首屏、主题与语言、锚点导航、Timeline、项目卡片和详情页状态、CV 头像及响应式布局。具体运行环境和人工检查清单见[工具手册](docs/PYTHON_GUIDE.md#发布前检查)。

构建和测试通过后，将源码与生成结果一起提交。GitHub Pages 在仓库 **Settings → Pages** 中选择从目标分支的仓库根目录发布即可；部署端只提供静态文件，不需要安装 Python。
