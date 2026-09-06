# Lain-Ego's Homepage
这是一个轻量化、响应式的个人主页网站，支持暗黑/亮色主题切换、多语言切换，包含项目展示、时间线、技术栈和联系方式等核心模块。
CSS由vibecoding实现。

## 规划与交付文档

- [项目需求文档](docs/PROJECT_REQUIREMENTS.md)
- [项目架构文档](docs/ARCHITECTURE.md)
- [验收标准文档](docs/ACCEPTANCE_CRITERIA.md)
- [Python 内容管理完整教程](docs/PYTHON_GUIDE.md)

## 目录
- [源码构成](#源码构成)
- [环境要求](#环境要求)
- [使用指南](#使用指南)
- [目录结构详解](#目录结构详解)
- [核心功能说明](#核心功能说明)
- [自定义配置](#自定义配置)

## 源码构成
本项目为纯前端静态网站，无后端依赖，核心由 HTML 结构、CSS 样式、JavaScript 交互三部分组成，模块职责清晰：

### 1. 核心 HTML（index.html）
整个网站的骨架，包含：
- 页面元信息（编码、视口、标题）
- 主题初始化脚本（读取本地存储/系统偏好设置，设置亮色/暗黑主题）
- 导航栏（Logo、导航链接、语言切换、主题切换按钮）
- 核心板块（个人简介、项目、开源贡献、时间线、技术栈、联系方式）
- 页脚
- 外部/内部脚本/样式引入

### 2. CSS 样式（assets/css/style.css）
- 响应式布局（适配移动端/桌面端）
- 主题样式（light/dark 两套主题变量）
- 组件样式（导航栏、头像、各板块、按钮、网格布局等）
- 动效样式（头像光晕、渐变文字、背景装饰等）

### 3. JavaScript 交互
#### (1) 国际化（assets/js/modules/i18n.js）
- 实现多语言切换（如示例中的中文/英文）
- 基于 `data-i18n` 属性匹配语言文案，替换页面文本

#### (2) 模块化交互（assets/js/）
- `app.js`：统一入口，根据页面类型加载主页或详情页逻辑
- `modules/theme.js`：主题切换与偏好保存
- `modules/navigation.js`：语言切换和平滑滚动
- `modules/home.js`：主页项目、时间线、技能和联系方式渲染
- `modules/project-detail.js`：项目详情页渲染
- `modules/project-data.js`：集中读取项目数据
- `modules/lightbox.js`：项目图片预览

### 4. 集中项目数据（assets/data/projects.json）
项目卡片、详情正文、图片、标签和外部链接均由这一份文件提供。修改项目内容时无需再同步编辑 `main.js` 和多个语言文件。

### 5. 静态资源
- `assets/images/`：头像（Avatar.jpg）等图片资源
- 第三方依赖：Font Awesome 图标库（CDN 引入）

## 环境要求
无需复杂环境，满足以下任一条件即可运行：
- 现代浏览器（Chrome/Firefox/Safari/Edge 最新版）
- 静态文件服务器（如 Nginx、Live Server 插件、Python SimpleHTTPServer）
- GitHub Pages/Gitee Pages 等静态页面托管平台

## 使用指南
### 1. 源码拉取
```bash
# 克隆仓库
git clone https://github.com/Lain-Ego0/Lain-Ego0.github.io.git
cd Lain-Ego0.github.io
```

### 2. 使用 Python 维护项目内容

编辑项目根目录的 `portfolio.py`，通过 `Portfolio`、`add_project()`、`add_project_page()` 和各类 `add_*()` 函数填写内容，无需编辑 HTML。该入口默认载入现有正式数据，直接执行不会用示例清空项目列表。

```bash
python portfolio.py validate
python portfolio.py build
python portfolio.py preview --port 8000
```

`validate` 只检查内容；`build` 在校验通过后以 UTF-8 稳定生成 `assets/data/projects.json`；`preview` 生成后启动本地预览。校验失败不会覆盖现有 JSON。

新增项目、图片、段落、列表、指标、视频及双语内容的具体写法见 [Python 内容管理完整教程](docs/PYTHON_GUIDE.md)。

### 3. 本地运行
#### 方式1：直接打开（简单测试）
双击 `index.html` 文件，通过浏览器直接打开（部分交互可能因跨域/本地路径问题受限）。

#### 方式2：静态服务器运行（推荐）
```bash
# 方法1：使用 Python 3 启动简易服务器
python -m http.server 8080

# 方法2：使用 Node.js http-server（需先安装：npm install -g http-server）
http-server -p 8080

# 方法3：VS Code 安装 Live Server 插件，右键 index.html → "Open with Live Server"
```
访问地址：`http://localhost:8080`

### 4. 部署上线
#### 方式1：GitHub Pages（推荐）
1. 将代码推送到 GitHub 仓库（仓库名：`[用户名].github.io`）；
2. 进入仓库 → Settings → Pages → 选择 `main` 分支 → 保存；
3. 等待几分钟后，访问 `https://[用户名].github.io` 即可。

#### 方式2：自定义服务器（Nginx）
1. 将源码上传到服务器；
2. 配置 Nginx 指向源码目录：
```nginx
server {
    listen 80;
    server_name your-domain.com; # 替换为你的域名
    root /path/to/Lain-Ego0.github.io; # 替换为源码路径
    index index.html;

    # 支持 SPA 路由（如需）
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```
3. 重启 Nginx：`nginx -s reload`。

## 目录结构详解
```
Lain-Ego0.github.io/
├── index.html               # 核心HTML页面（网站入口）
├── assets/                  # 静态资源目录
│   ├── css/                 # 样式目录
│   │   └── style.css        # 全局样式（含主题、布局、组件样式）
│   ├── js/                  # 脚本目录
│   │   ├── app.js           # 应用统一入口
│   │   └── modules/         # 功能模块
│   │       ├── home.js
│   │       ├── i18n.js
│   │       ├── lightbox.js
│   │       ├── navigation.js
│   │       ├── project-data.js
│   │       ├── project-detail.js
│   │       ├── site-data.js
│   │       └── theme.js
│   ├── data/
│   │   └── projects.json    # 项目唯一数据源
│   └── images/              # 图片目录
│       ├── Avatar.jpg       # 个人头像（当前未启用）
│       └── Portfolio-*.png  # 项目展示图片
├── lang/                    # 国际化文案
│   ├── zh.json              # 中文
│   └── en.json              # 英文
├── pages/projects/          # 项目详情页
│   ├── project1.html
│   ├── project2.html
│   ├── project3.html
│   └── project4.html
├── project.html             # Python 新增项目共用的详情页
├── portfolio.py             # 根目录 Python 内容与命令入口
├── portfolio_content/       # 离线 Python 内容生成包
├── schemas/                 # 内容数据 Schema
├── tests/python/            # Python 自动化测试
└── README.md                # 项目说明
```

## 核心功能说明
### 1. 主题切换
- 初始化：读取 localStorage 中的主题偏好，无已保存偏好时默认为深色；
- 切换逻辑：点击导航栏「月亮/太阳」图标，切换 `data-theme` 为 `dark/light`，并同步到 localStorage。

### 2. 多语言切换
- 点击导航栏「中文/English」按钮，通过语言模块替换所有带 `data-i18n` 属性的元素文本；
- 无已保存偏好时默认使用英文；通用界面文案位于 `lang/zh.json` 和 `lang/en.json`。

### 3. 核心板块
- 「Intro」：个人简介（标题、描述）；
- 「Projects」：项目展示（由 `assets/data/projects.json` 动态渲染）；
- 「Timeline」：时间线（经历/里程碑）；
- 「Skills」：技术栈展示；
- 「Contact」：联系方式（社交链接等）。

## 自定义配置
### 1. 修改个人信息
- 头像：如需启用，可在 `index.html` 的 `.avatar-container` 中添加头像标签；
- 页面标题/简介：修改 `index.html` 中 `title`、`intro.title`、`intro.desc` 等 `data-i18n` 对应的文案（需同步修改 `i18n.js` 中的语言包）；
- 页脚版权：修改 `index.html` 中 footer 的 `data-i18n` 文案。

### 2. 新增/修改板块内容
- 项目：统一修改 `assets/data/projects.json`；时间线文案修改 `lang/*.json`，技能和联系方式配置修改 `assets/js/modules/site-data.js`。

### 3. 自定义主题
- 修改 `assets/css/style.css` 中的 `:root`（light 主题）和 `[data-theme="dark"]`（dark 主题）下的 CSS 变量（如颜色、字体、间距等）。

### 4. 新增语言
- 在 `lang/` 中增加对应 JSON，并在 `assets/data/projects.json` 的每个项目中增加相同语言的 `locales` 数据；
- 扩展 `assets/js/modules/i18n.js` 中的语言切换规则。
---
