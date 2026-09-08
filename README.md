# Hancheng Guo Portfolio

一个由 Python 内容配置生成的双语静态个人主页，用于展示个人资料、项目、论文、时间线和 CV。网站无需后端或数据库，可以直接部署到 GitHub Pages。

![首页效果](assets/images/docs/home.png)

## 主要特性

- 默认英文和深色主题，并记住访客的语言与主题选择。
- 首页包含 Portfolio、Projects、Publications 和 Timeline。
- 独立 CV 页面包含个人信息、Education、Work Experience、Publications、Tech Stack 与 Awards & Scholarships。
- 每个项目拥有独立静态详情页、前后项目导航、图片预览和可选外部链接。
- Python 在构建阶段生成完整 HTML 和 JSON；禁用 JavaScript 时仍能阅读核心内容。
- JavaScript 只负责语言、主题、数据同步、平滑导航和交互增强。
- 图标与 Markdown 解析器均保存在仓库内，不依赖运行时 CDN。
- 响应式布局支持桌面和移动端，并尊重 `prefers-reduced-motion`。

## 快速开始

需要 Python 3.10 或更高版本：

```bash
git clone https://github.com/Hancheng-Guo/hancheng-guo.github.io.git
cd hancheng-guo.github.io

python portfolio.py validate
python portfolio.py build
python portfolio.py preview
```

打开 <http://127.0.0.1:8000/> 查看网站，按 `Ctrl+C` 停止预览。Windows 若没有 `python` 命令，可以将其替换为 `py`。

日常修改只需要编辑根目录的 [`portfolio.py`](portfolio.py)，不应手工修改生成的 HTML 或 JSON。完整 API、字段格式和示例见 [Python 工具手册](docs/PYTHON_GUIDE.md)。

## 常用命令

```bash
# 仅校验内容和资源路径
python portfolio.py validate

# 校验并生成完整静态网站
python portfolio.py build

# 构建后在本机启动预览
python portfolio.py preview --port 8000

# 删除生成的 HTML 与 JSON
python portfolio.py clean
```

`clean` 不会删除 `portfolio.py`、构建器或静态资源；随后执行 `build` 可以恢复全部生成文件。构建器采用临时文件和原子替换，校验失败时不会覆盖已有项目数据。

## 内容与生成结果

`portfolio.py` 是人工维护的唯一内容源。一次 `build` 会生成：

- `index.html`：完整静态首页；
- `pages/cv.html`：完整静态 CV 页面；
- `pages/projects/*.html`：项目详情页；
- `assets/data/site.json`：站点、履历和联系方式数据；
- `assets/data/projects.json`：项目列表、正文块与链接数据。

生成的 HTML 会按照 DOM 层级换行和缩进，便于检查，但下一次构建仍会覆盖它们。

## 项目结构

```text
.
├── portfolio.py                 # 内容配置与命令入口
├── index.html                   # 生成的首页
├── pages/
│   ├── cv.html                  # 生成的 CV 页面
│   └── projects/                # 生成的项目详情页
├── assets/
│   ├── css/style.css            # 主题、组件和响应式样式
│   ├── data/                    # 生成的 JSON
│   ├── documents/               # 中英文 CV 等下载文件
│   ├── icons/                   # 本地 SVG 图标
│   ├── images/                  # 头像、项目图和文档截图
│   ├── js/                      # 浏览器入口与功能模块
│   └── vendor/                  # 本地化的前端第三方依赖
├── portfolio_content/           # Python 构建器、校验器和渲染器
├── lang/                        # 通用界面中英文文案
├── schemas/                     # 生成数据的 JSON Schema
├── tests/                       # Python 与浏览器回归测试
└── docs/PYTHON_GUIDE.md         # 内容构建工具手册
```

## 测试

Python 测试不需要额外依赖：

```bash
python -m unittest discover -s tests/python -v
```

浏览器回归脚本位于 `tests/browser/`，覆盖静态首屏、语言与主题切换、Timeline、项目卡片稳定性、CV 头像、同页平滑滚动和跨页锚点。运行它们需要 Node.js、Playwright 和可用的 Chromium/Edge 浏览器环境。

## 部署

构建完成后，将源码与生成结果一起提交并推送到当前独立仓库。GitHub Pages 配置步骤：

1. 打开仓库的 **Settings → Pages**；
2. 选择从分支部署；
3. 选择发布分支和仓库根目录；
4. 等待部署完成后访问 <https://hancheng-guo.github.io/>。

部署端只提供静态文件，不需要安装 Python；Python 仅用于本地编辑和构建。
