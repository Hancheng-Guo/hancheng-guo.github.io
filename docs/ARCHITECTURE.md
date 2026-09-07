# 个人项目主页架构文档

## 1. 架构目标

目标架构保持 GitHub Pages 友好的纯静态运行方式，同时增加一个离线 Python 内容层：

```text
维护者的 Python 配置
        │
        ▼
portfolio_content 生成器 ── 校验 Schema / 路径 / URL / 多语言
        │
        ▼
标准化 JSON + 完整静态首页、CV 页与项目详情页
        │
        ▼
浏览器 ES Modules ── 渐进增强国际化 / 主题 / 导航 / 灯箱
        │
        ▼
GitHub Pages 静态发布
```

Python 仅在内容编辑阶段运行，不进入线上请求链路。

## 2. 当前架构评估

### 2.1 已有优势

- 无框架、无运行时后端，部署简单。
- 项目内容集中于 `assets/data/projects.json`。
- JavaScript 已按主题、国际化、导航、主页、详情页和灯箱拆分。
- 详情页通过 `data-project-id` 复用同一渲染逻辑。

### 2.2 当前技术债

- `projects.json` 没有机器可校验的 schema。
- 详情内容结构仍是 `sections + gallery`，渲染器通过图片索引决定章节插入位置。
- 四个详情页的 nav、资源引用和 footer 重复。
- 项目数据通过字符串插入 `innerHTML`，没有清理或上下文转义。
- 数据请求错误没有传递到 UI，`initLanguage()` 和项目加载也没有统一启动状态。
- 历史版本使用 Marked 和 Font Awesome CDN；当前版本已移除运行时 CDN 请求。Markdown 解析器保存在 `assets/vendor/marked/`，实际使用的图标则以独立 SVG 保存在 `assets/icons/`，不再加载图标字体。
- 没有构建、测试、格式化、链接检查或部署前门禁。

## 3. 目标目录

```text
portfolio/
├── index.html
├── pages/projects/*.html           # Python 生成的完整静态详情页
├── assets/
│   ├── css/
│   │   ├── tokens.css              # 颜色、字号、间距、圆角
│   │   ├── base.css                # reset、排版、无障碍基础
│   │   ├── components.css          # nav、card、button、dialog
│   │   └── pages.css               # 首页与详情页布局
│   ├── data/
│   │   ├── site.json               # 个人资料、经历、技能、联系
│   │   └── projects.json           # 生成后的项目数据
│   ├── images/
│   ├── vendor/                     # 必须本地化的第三方依赖
│   └── js/
│       ├── app.js
│       ├── core/                    # store、router、errors、sanitizer
│       ├── data/                    # repositories、schema version adapter
│       ├── features/                # theme、i18n、navigation、lightbox
│       ├── pages/                   # home、project
│       └── ui/                      # 可复用渲染组件
├── content/
│   ├── portfolio.py                # 客户主要编辑入口
│   └── images/                      # 可选的原始图片入口
├── portfolio_content/
│   ├── __init__.py
│   ├── builder.py
│   ├── models.py
│   ├── blocks.py
│   ├── validators.py
│   ├── serializers.py
│   ├── templates.py
│   └── cli.py
├── schemas/
│   ├── site.schema.json
│   └── projects.schema.json
├── scripts/
│   ├── build_content.py
│   ├── preview.py
│   └── check_links.py
├── tests/
│   ├── python/
│   ├── unit/
│   └── e2e/
└── docs/
```

每个项目固定生成 `pages/projects/<project-id>.html`。这些页面由同一 Python renderer 生成，保留稳定 URL，但不存在多份手工维护的 HTML 正文。

## 4. 数据架构

### 4.1 分层原则

- `site.json`：站点级个人信息、时间线、技能、联系、简历链接。
- `projects.json`：项目列表和详情内容。
- `lang/*.json`：只保留组件级通用界面文案；不保存项目正文。

当前实现还生成 `site.json`，其中包含 `site`、`profile`、`education`、`workExperience`、`publications`、`awards`、`resume`、`timeline`、`techStack` 和 `contacts`。`site` 保存双语网站名称、作者、版权文字及最后更新日期，`profile` 表达全站身份信息；论文必须进入 `publications`。所有履历条目的日期均保存为 `{start, end?}`，由前端按语言格式化。未确认资料应使用明确的 Test 占位文字。
- CSS 和 JS 不保存业务文本。

### 4.2 推荐项目 schema

```json
{
  "schemaVersion": 2,
  "projects": [
    {
      "id": "quadruped-robot",
      "slug": "quadruped-robot",
      "year": 2025,
      "order": 10,
      "featured": true,
      "thumbnail": {
        "src": "assets/images/quadruped/cover.webp",
        "width": 1600,
        "height": 900,
        "alt": {
          "en": "Quadruped robot on the competition field",
          "zh": "比赛场地中的四足机器人"
        }
      },
      "tags": ["Robotics", "Reinforcement Learning"],
      "links": [
        { "type": "github", "url": "https://github.com/example/repo" }
      ],
      "locales": {
        "en": {
          "title": "Quadruped Robot",
          "summary": "...",
          "blocks": [
            { "type": "heading", "level": 2, "text": "My Role" },
            { "type": "paragraph", "text": "..." },
            { "type": "metrics", "items": [{ "label": "Position error", "value": "±5 mm" }] },
            { "type": "image", "asset": "result-image" }
          ]
        },
        "zh": {
          "title": "四足机器人",
          "summary": "...",
          "blocks": []
        }
      },
      "assets": {
        "result-image": {
          "src": "assets/images/quadruped/result.webp",
          "width": 1600,
          "height": 900,
          "alt": { "en": "...", "zh": "..." }
        }
      }
    }
  ]
}
```

图片资源从正文块中通过 key 引用，可以避免中英文重复保存路径，同时强制集中维护尺寸和 alt。

### 4.3 版本与兼容

- JSON 顶层必须包含 `schemaVersion`。
- 浏览器数据仓储层负责拒绝未知的大版本，或调用明确的迁移 adapter。
- Python 工具升级 schema 时提供 `migrate`，不得静默改变字段语义。

## 5. Python 内容工具设计

### 5.1 公共 API

```python
class Portfolio:
    @classmethod
    def load(cls, path: str) -> "Portfolio": ...
    def add_project(self, *, project_id, title, summary, thumbnail, tags=(), featured=False) -> "Project": ...
    def remove_project(self, project_id: str) -> None: ...
    def validate(self) -> "ValidationReport": ...
    def write(self, output: str) -> None: ...

class ProjectPage:
    def __init__(self, project: "Project", template: str = "case-study"): ...
    def add_heading(self, text, *, level=2): ...
    def add_paragraph(self, text): ...
    def add_image(self, src, *, alt, caption=None): ...
    def add_gallery(self, images, *, columns="auto"): ...
    def add_list(self, items, *, ordered=False): ...
    def add_quote(self, text, *, source=None): ...
    def add_metrics(self, items): ...
    def add_video(self, url, *, poster=None, title=None): ...
    def add_github_link(self, url, *, label=None): ...
    def add_doc_link(self, url, *, label=None): ...
    def add_bilibili_link(self, url, *, label=None): ...
    def add_youtube_link(self, url, *, label=None): ...
```

所有添加函数返回 `self`，允许链式调用。传入文本接受 `str` 或 `{"en": str, "zh": str}`；内部统一转换为多语言模型。四个类型化链接函数的可选 `label` 会原样进入项目数据，并由静态和运行时渲染器按当前语言安全解析 Markdown。

### 5.2 模板机制

模板只规定默认块顺序和必填内容，不保存客户正文：

- `case-study`：Overview → My Role → Challenge → Approach → Results → Evidence。
- `research`：Abstract → Research Question → Method → Experiment → Findings → Limitations。
- `competition`：Objective → Responsibilities → System Design → Results → Awards。
- `minimal`：自由排列内容块。

`add_project_page(template="case-study")` 应创建一个可继续填充的页面对象，而不是把正文拼接成 HTML 字符串。

### 5.3 校验流水线

```text
Python 类型校验
  → JSON Schema 校验
  → 业务规则（唯一 ID、默认语言、字段长度）
  → 文件规则（图片存在、尺寸可读取）
  → URL 语法检查
  → 输出临时文件
  → 重新读取并校验
  → 原子替换正式 JSON
```

错误示例应面向客户：

```text
[project quadruped-robot] 缺少英文 summary。
位置：portfolio.py:18
建议：在 summary 参数中增加 {"en": "..."}。
未修改 assets/data/projects.json。
```

### 5.4 CLI

```text
python portfolio.py validate
python portfolio.py build
python portfolio.py preview --port 8000
```

`preview` 先执行校验和生成，再启动本地静态服务器；不应要求维护者理解模块 MIME 或浏览器跨域问题。

## 6. 浏览器模块设计

### 6.1 启动流程

```text
读取已保存主题并立即应用
  → 加载界面语言和 site.json
  → 根据 page type 选择页面控制器
  → 加载项目数据
  → 保留 Python 已生成的静态内容并用当前语言数据增强 / error
  → 绑定可访问交互
```

入口函数必须 `await` 初始化并捕获异常，避免未处理 Promise。

### 6.2 组件职责

- `BackLink`：固定回到首页项目区；文案国际化。
- `ProjectCard`：整卡为原生链接，含标题、摘要、标签和图片。
- `ContentBlockRenderer`：以白名单映射 block type，不允许任意类型执行 HTML。
- `ExternalLinks`：过滤空 URL，并提供外链标识。
- `LightboxDialog`：使用 `<dialog>` 或等价 ARIA dialog，负责焦点生命周期。
- `StatusView`：统一 loading、empty、error 和 retry。

### 6.3 安全边界

- 纯文本一律用 `textContent`。
- 所有面向访客显示的自定义文字统一视为 Markdown：标题、标签和按钮使用行内模式，正文使用块级 GitHub Flavored Markdown。行内扩展将 `_文字_` 重载为 `<u>` 下划线，`*文字*` 保持标准斜体。前端统一经过本地 Markdown 模块解析，并移除脚本、事件属性和危险协议；邮箱、URL、日期、资源路径及图标名称保持结构化数据语义，不参与 Markdown 解析。
- URL 只允许 `https:`、`mailto:` 和站内相对路径；禁止 `javascript:` 和数据 URL。
- Python 生成器做第一层校验，浏览器仍需做防御性校验。

## 7. 导航设计

详情页头部建议：

```text
Lain-Ego                         EN / 中    Theme

< Back to Projects
Project title
```

- Logo 保持品牌首页入口。
- 返回链接靠近详情内容，降低识别成本。
- 返回链接目标为相对主页路径加 `#projects`。
- 首页项目区可读取 URL hash；从详情返回后将焦点移至对应项目卡片，并尽量恢复浏览位置。

## 8. CSS 架构

- `tokens.css` 只定义设计变量，深浅主题覆盖相同 token。
- `base.css` 负责语义元素和无障碍基线。
- `components.css` 组件样式不依赖具体页面 DOM 深度。
- `pages.css` 只负责页面布局。
- 所有颜色使用 token；正文 JSON 中禁止内联样式。
- 断点至少覆盖 480、768、1024；组件优先使用容器自身宽度。

## 9. 测试与发布

### 9.1 测试层次

- Python 单元测试：builder、validator、serializer、template。
- JS 单元测试：数据仓储、block renderer、URL 过滤、i18n fallback。
- 端到端测试：首页 → 详情 → 返回、语言、主题、移动菜单、灯箱、错误状态。
- 静态检查：JSON Schema、HTML、ESLint、Stylelint、内部链接、图片引用。
- 质量检查：axe、Lighthouse、不同视口截图回归。

### 9.2 CI 门禁

```text
format/lint
  → Python tests
  → content build + schema validation
  → link and asset checks
  → browser E2E + accessibility
  → production preview + Lighthouse
  → deploy GitHub Pages
```

任何生成文件必须由 CI 重新生成并检查工作区无差异，防止提交的 JSON 与 Python 内容源不一致。

## 10. 迁移方案

1. 为当前 JSON 增加 schemaVersion 和 schema，不改变 UI。
2. 实现 Python models、builder、validator 和当前 schema serializer。
3. 使用根目录 `portfolio.py` 载入现有项目数据，并对生成结果做快照测试。
4. 引入 blocks v2 和 block renderer，逐个迁移项目。
5. 为所有项目生成完整的 `pages/projects/<project-id>.html` 静态详情页。
6. 拆分 CSS、补齐状态/无障碍/SEO。
7. 增加 CI 后再允许非技术维护者使用生成流程。

每一步都应保持网站可部署，避免一次性重写。
