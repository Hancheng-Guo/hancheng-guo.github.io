# 个人项目主页需求文档（PRD）

## 1. 文档信息

- 产品名称：Lain-Ego Portfolio
- 产品形态：面向学校申请场景的双语静态个人主页
- 目标读者：产品设计、视觉设计、前端开发、内容维护人员、测试人员
- 当前基线：仓库现有首页、四个项目详情页、深浅色主题与中英文切换
- 优先级定义：P0 为发布必需，P1 为强烈建议，P2 为后续增强

## 2. 产品目标

网站需要让招生老师或潜在导师在 1 分钟内回答以下问题：

1. 申请者是谁，研究或工程方向是什么？
2. 申请者在项目中具体负责什么，而不只是参与过什么？
3. 有哪些可验证的成果、奖项、代码、文档或演示？
4. 如何查看完整履历并联系申请者？

网站同时需要让不熟悉前端的维护者，在不直接编辑 HTML 或 JavaScript 的情况下更新项目内容。

## 3. 目标用户与使用场景

### 3.1 主要访问者

- 招生委员会成员：快速浏览背景、项目质量与成果。
- 潜在导师：重点关注研究兴趣、技术深度、个人贡献和后续研究方向。
- 实验室成员或面试官：查看技术细节、代码和演示材料。

### 3.2 内容维护者

- 不熟悉 HTML、CSS、JavaScript。
- 能安装 Python，能复制图片并修改少量 Python 参数。
- 需要明确的错误提示、示例和可恢复的生成流程。

### 3.3 核心访问路径

1. 进入首页 → 认识申请者 → 浏览精选项目 → 打开项目详情 → 查看证据 → 返回项目列表。
2. 进入首页 → 查看经历、能力和申请方向 → 下载简历或发送邮件。
3. 通过分享链接直接进入详情页 → 理解页面所属网站 → 返回项目列表或主页。
4. 维护者填写 Python 配置 → 运行生成命令 → 校验数据 → 本地预览 → 发布。

## 4. 当前基线与主要缺点

### 4.1 产品表达

- 首屏只有通用自我介绍，没有明确说明申请方向、目标学位、研究兴趣和可用状态。
- 项目卡片强调技术描述，但缺少统一的“背景—职责—方法—量化结果—证据”叙事。
- 缺少教育经历、研究经历、代表奖项、论文/专利/出版物、简历下载和明确联系 CTA。
- 项目 1 的英文详情含明显占位或损坏内容；项目 3 与项目 4 的图片、文案和链接重复，不能作为正式申请材料发布。
- 部分外链为空时仍显示成按钮，容易让访问者误以为页面失效。

### 4.2 导航与交互

- 详情页左上角 `Lain-Ego` 虽能回首页，但它更像品牌标识，不足以表达“返回”。
- 移动端直接隐藏主导航，没有菜单或等价导航路径。
- 项目卡片使用可点击 `div`，键盘用户无法自然聚焦和触发整张卡片。
- 图片灯箱缺少焦点约束、焦点恢复、移动端手势说明和本地化的关闭标签。
- 页面数据加载失败时缺少可见的 loading、empty 和 error 状态。

### 4.3 内容维护

- 项目数据已经集中到 `assets/data/projects.json`，但 JSON 对非技术用户仍不友好。
- 详情布局将第 2 个章节与第 2 张图片的位置耦合，难以自由组合标题、段落、图片、视频和列表。
- 四个详情页 HTML 壳高度重复；新增项目仍需复制页面并手动填写 `data-project-id`。
- 没有数据 schema、生成器、预览命令或自动校验，错误路径和漏填翻译只能在浏览器中发现。

### 4.4 工程质量

- 依赖 CDN 提供 Marked 和 Font Awesome；网络受限时内容或图标可能降级。
- 文本通过 `innerHTML` 渲染，缺少 HTML 白名单清理。
- 图片缺少统一压缩、WebP/AVIF、尺寸属性和懒加载策略；仓库中还有未使用的大尺寸头像。
- 缺少 SEO/分享元数据、favicon、canonical、Open Graph、站点地图和结构化数据。
- 缺少自动测试、链接检查、无障碍检查和性能预算。

## 5. 功能需求

### 5.1 信息架构

| ID | 优先级 | 需求 |
|---|---:|---|
| PRD-IA-001 | P0 | 首页必须包含：个人定位、申请/研究方向、精选项目、经历时间线、技术能力、联系方式。 |
| PRD-IA-002 | P0 | 首屏必须提供一个主 CTA（查看项目）和一个次 CTA（下载简历或联系）。 |
| PRD-IA-003 | P0 | 每个项目详情必须包含概览、个人职责、关键挑战、方法、结果、技术栈和证据链接；无内容的区块不渲染。 |
| PRD-IA-004 | P1 | 增加 Education / Research / Awards 区块；若没有论文，不显示空的 Publications 区块。 |
| PRD-IA-005 | P1 | 提供可下载的英文简历，可选提供中文简历。 |

### 5.2 详情页返回与导航

| ID | 优先级 | 需求 |
|---|---:|---|
| PRD-NAV-001 | P0 | 详情正文顶部必须显示明确的 `← Back to Projects` / `← 返回项目` 链接，目标为首页 `#projects`。 |
| PRD-NAV-002 | P0 | 保留左上角品牌标识并继续链接首页；品牌归属与返回操作不得互相替代。 |
| PRD-NAV-003 | P0 | 返回链接必须使用原生 `<a>`，支持键盘、复制链接、在新标签打开和无 JavaScript 降级。 |
| PRD-NAV-004 | P1 | 详情页底部提供 Previous / Next Project，且项目顺序来自数据源。 |
| PRD-NAV-005 | P0 | 移动端必须提供菜单按钮或精简后的等价导航，不得简单隐藏所有主导航。 |

选择显式返回链接而不是只调用 `history.back()`：用户可能从邮件或搜索结果直接打开详情页，此时浏览器历史不一定属于本站。固定返回 `index.html#projects` 的行为更可预测。可把浏览器后退作为增强，但不能作为唯一实现。

### 5.3 项目内容模型

| ID | 优先级 | 需求 |
|---|---:|---|
| PRD-DATA-001 | P0 | 项目 ID 必须唯一且稳定，只允许小写字母、数字和连字符。 |
| PRD-DATA-002 | P0 | 项目必须支持中英文标题、摘要和内容；缺少默认英文时生成失败。 |
| PRD-DATA-003 | P0 | 正文改为有序 `blocks`，支持 `heading`、`paragraph`、`image`、`gallery`、`list`、`quote`、`video` 和 `metrics`。 |
| PRD-DATA-004 | P0 | 外链必须标明类型、URL 和可选标签；URL 为空时不渲染按钮。 |
| PRD-DATA-005 | P0 | 每张内容图片必须提供对应语言的 alt；纯装饰图片可显式标记为空 alt。 |
| PRD-DATA-006 | P1 | 项目支持 featured、排序权重、年份、状态和关键词，以便首页筛选与排序。 |

### 5.4 Python 内容生成工具

Python 程序只作为离线内容编码和校验工具，不作为网站运行时后端。生成完成后，网站仍可部署为纯静态站点。

| ID | 优先级 | 需求 |
|---|---:|---|
| PRD-PY-001 | P0 | 提供可导入的 Python 包，而不只是一次性脚本。 |
| PRD-PY-002 | P0 | 维护者可通过函数创建站点、项目和标准内容块，正文文本必须作为参数传入。 |
| PRD-PY-003 | P0 | 提供 `add_project()`、`add_heading()`、`add_paragraph()`、`add_image()`、`add_gallery()`、`add_metrics()`、`add_link()` 等模块化函数。 |
| PRD-PY-004 | P0 | 提供 `add_project_page(template=...)`，用于选择已定义的详情页模板；模板内容仍通过内容块函数填充。 |
| PRD-PY-005 | P0 | 输出前校验必填字段、重复 ID、语言缺失、图片路径、URL、块类型和字段长度。 |
| PRD-PY-006 | P0 | 生成采用临时文件加原子替换；校验失败时不得破坏现有可用数据。 |
| PRD-PY-007 | P0 | 相同输入必须产生稳定、格式化且 UTF-8 编码的 JSON。 |
| PRD-PY-008 | P1 | 提供 `preview` 和 `validate` 命令，并打印非技术用户可理解的错误位置和修复建议。 |
| PRD-PY-009 | P1 | 自动创建详情页壳，或在目标架构中改为一个通用详情页，从根本上取消复制 HTML。 |

建议的客户调用方式：

```python
from portfolio_content import Portfolio, ProjectPage

site = Portfolio.load("content/portfolio.json")

project = site.add_project(
    project_id="quadruped-robot",
    title={"en": "Quadruped Robot", "zh": "四足机器人"},
    summary={"en": "...", "zh": "..."},
    thumbnail="assets/images/quadruped/cover.webp",
    tags=["Robotics", "RL"],
    featured=True,
)

page = ProjectPage(project, template="case-study")
page.add_heading({"en": "My Role", "zh": "我的职责"}, level=2)
page.add_paragraph({"en": "...", "zh": "..."})
page.add_image(
    "assets/images/quadruped/result.webp",
    alt={"en": "Robot crossing an obstacle", "zh": "机器人跨越障碍"},
)
page.add_metrics([
    {"label": {"en": "Position error", "zh": "定位误差"}, "value": "±5 mm"}
])
page.add_link("github", "https://github.com/example/repo")

site.validate()
site.write("assets/data/projects.json")
```

### 5.5 国际化与主题

- PRD-I18N-001（P0）：首次访问默认英文和深色主题，已保存偏好优先。
- PRD-I18N-002（P0）：所有可见文字、按钮标签、错误提示、ARIA 标签均可本地化。
- PRD-I18N-003（P0）：切换语言后更新 `<html lang>`、页面标题和 description。
- PRD-I18N-004（P1）：对内嵌富文本进行白名单清理，禁止脚本、事件属性和危险 URL。
- PRD-THEME-001（P0）：深浅主题均满足可读性要求，内容中禁止写死 `color:white`。

### 5.6 可访问性、响应式和反馈

- PRD-A11Y-001（P0）：所有交互可使用键盘完成，有清晰的 `:focus-visible`。
- PRD-A11Y-002（P0）：整张项目卡片使用语义化链接，不能只依赖 `div.onclick`。
- PRD-A11Y-003（P0）：灯箱打开后焦点进入关闭按钮，Tab 不离开弹层，Escape 关闭，关闭后焦点返回原图片。
- PRD-A11Y-004（P0）：图标按钮具备随状态变化的可访问名称。
- PRD-RWD-001（P0）：支持 320px 至 1920px 视口，不出现非预期横向滚动。
- PRD-STATE-001（P0）：数据加载时显示 loading；失败时显示错误和重试；无项目时显示 empty state。
- PRD-MOTION-001（P1）：尊重 `prefers-reduced-motion`。

### 5.7 申请场景、SEO 与性能

- PRD-APP-001（P0）：首页明确展示申请方向、目标项目/学位、研究兴趣和联系邮箱。
- PRD-APP-002（P0）：项目结果尽量量化，并为奖项、代码、文档或视频提供证据链接。
- PRD-SEO-001（P0）：每页具有唯一 title、description、canonical、Open Graph 和 favicon。
- PRD-SEO-002（P1）：生成 sitemap.xml、robots.txt 和 Person/CreativeWork JSON-LD。
- PRD-PERF-001（P0）：首屏图片明确尺寸，非首屏图片 lazy-load；提供现代格式和合理 fallback。
- PRD-PERF-002（P1）：关键内容不能因第三方 CDN 失败而完全不可用，依赖应本地化或提供降级。

## 6. 非功能需求

- 兼容当前稳定版 Chrome、Edge、Firefox、Safari，以及 iOS Safari 和 Android Chrome。
- GitHub Pages 部署后不得依赖服务器端路由或 Python 运行环境。
- 数据生成器支持 Python 3.11 及以上版本。
- 所有生成内容使用 UTF-8，不包含机器相关的绝对路径。
- 维护者完成“新增标准项目并预览”的目标时间不超过 15 分钟。

## 7. 发布优先级

### Phase 1：申请可发布版本

- 修复全部项目中英文内容和重复项目。
- 增加显式返回、移动导航、简历/联系 CTA。
- 补齐 SEO、空链接处理、加载/失败状态和关键无障碍能力。
- 完成 Python 数据生成、schema 校验和基础测试。

### Phase 2：内容表现增强

- 结构化项目 blocks、量化指标组件、前后项目导航。
- Education / Research / Awards、项目筛选、结构化数据。
- 图片自动优化、性能预算和完整端到端测试。

### Phase 3：可选增强

- 可打印项目页、分析统计、更多语言、无代码表单界面。

## 8. 明确不做

- 不引入运行时后端、数据库、账号系统或在线 CMS。
- Python 工具不负责自动创作或改写申请内容，只编码、校验和生成用户提供的文本。
- 不为了动画牺牲首屏速度、可访问性或内容可读性。
