# 个人项目主页验收标准

## 1. 验收原则

- 每条标准对应需求文档中的 ID。
- P0 全部通过才允许作为学校申请主页发布。
- 自动化检查负责可重复结论，人工检查负责内容真实性和视觉判断。
- 测试至少覆盖英文/中文、深色/浅色、桌面/移动端四组组合。

## 2. 内容与申请场景

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-APP-001 | 首屏无需滚动即可看到姓名、明确的研究/申请方向和至少一个主 CTA。 | 1440×900、390×844 人工截图检查。 |
| AC-APP-002 | 首页存在有效的联系入口；若提供简历，链接返回 200 且文件可打开。 | 自动链接检查 + 人工打开。 |
| AC-APP-003 | 每个发布项目都明确区分个人职责、方法和结果，并至少有一个可验证证据；确实没有证据时明确说明而非显示坏链接。 | 内容审阅。 |
| AC-APP-004 | 项目 1 英文详情不存在中文残片或 `www` 等占位文本。 | 搜索占位词 + 双语人工审阅。 |
| AC-APP-005 | 项目 3 和项目 4 不再错误复用同一套标题、图片和链接；若本质是同一项目，则合并为一个条目。 | 数据 diff + 人工审阅。 |

## 3. 导航与返回

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-NAV-001 | 所有项目详情标题上方均可见 `← Back to Projects` 或 `← 返回项目`。 | 遍历全部详情页。 |
| AC-NAV-002 | 点击返回链接进入首页并定位到 `#projects`，直接打开详情页时也成立。 | 新标签直接打开详情 URL 后点击。 |
| AC-NAV-003 | 左上角 `Lain-Ego` 仍进入首页，且不会与返回链接视觉混淆。 | 人工交互检查。 |
| AC-NAV-004 | 返回链接可用 Tab 聚焦、Enter 激活；其 HTML 元素为 `<a href="...">`。 | 键盘测试 + DOM 检查。 |
| AC-NAV-005 | 320–767px 下存在可操作的导航入口，所有桌面导航目的地均可到达。 | 320、390、768px E2E。 |
| AC-NAV-006 | 若实现前后项目导航，第一项不显示 Previous，最后一项不显示 Next，中间项顺序与数据一致。 | 数据驱动 E2E。 |

## 4. Python 内容生成器

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-PY-001 | Python 3.11+ 可执行 `import portfolio_content`，无须启动网站后端。 | 干净环境安装/导入测试。 |
| AC-PY-002 | 示例仅通过 Python 函数即可新增项目、标题、段落、图片、指标和链接，并成功生成网页数据。 | 运行示例集成测试。 |
| AC-PY-003 | `case-study`、`research`、`competition`、`minimal` 模板可创建详情页模型，模板不含客户正文。 | 模板单元测试和快照。 |
| AC-PY-004 | 重复项目 ID、非法 ID、缺少英文、未知 block、缺失图片、非法 URL 均导致非零退出码。 | 参数化负例测试。 |
| AC-PY-005 | 错误输出包含项目 ID、字段路径、原因和修复建议；非技术用户无需阅读 traceback。 | CLI 快照测试。 |
| AC-PY-006 | 校验失败后，已有 `projects.json` 哈希不变。 | 生成前后哈希测试。 |
| AC-PY-007 | 同一输入连续生成两次，输出文件字节完全一致。 | SHA-256 比较。 |
| AC-PY-008 | 输出为 UTF-8，有统一缩进，无绝对文件路径，通过 JSON Schema。 | 编码、文本和 schema 测试。 |
| AC-PY-009 | `preview` 命令启动本地服务并打印唯一访问 URL；停止命令后端口释放。 | CLI 集成测试。 |
| AC-PY-010 | 按维护指南新增一个标准项目，从编辑开始到看到本地预览不超过 15 分钟。 | 首次使用者可用性测试。 |

建议的最低自动化用例：

```python
def test_invalid_build_does_not_replace_output(tmp_path): ...
def test_duplicate_project_id_is_rejected(): ...
def test_missing_default_english_is_rejected(): ...
def test_unknown_block_type_is_rejected(): ...
def test_output_is_deterministic(): ...
def test_all_assets_exist(): ...
def test_all_external_urls_use_allowed_schemes(): ...
```

## 5. 数据与渲染

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-DATA-001 | `projects.json` 包含 schemaVersion，且所有项目 ID 唯一并符合 `^[a-z0-9]+(?:-[a-z0-9]+)*$`。 | JSON Schema。 |
| AC-DATA-002 | 首页卡片和详情页从同一项目对象读取标题、摘要、图片和链接，不存在第二份项目正文。 | 静态扫描 + 架构审查。 |
| AC-DATA-003 | 调整 blocks 顺序后，页面按新顺序渲染，不需要修改 JavaScript。 | 数据驱动测试。 |
| AC-DATA-004 | URL 为 null 或空字符串时不渲染按钮；非法协议被拒绝。 | 单元测试 + DOM 断言。 |
| AC-DATA-005 | 数据或语言加载失败时页面显示本地化错误信息和重试按钮，不出现永久空白或未处理 Promise。 | 网络拦截 E2E + console 断言。 |
| AC-DATA-006 | 空项目列表显示 empty state；单项目和 20 项目时布局均可用。 | fixture E2E。 |

## 6. 国际化与主题

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-I18N-001 | 清空 localStorage 后首次加载为英文、深色；刷新不闪现浅色主题。 | E2E 清状态并录屏/截图。 |
| AC-I18N-002 | 手动切换为中文或浅色后刷新，选择保持不变。 | E2E。 |
| AC-I18N-003 | 切换语言后导航、正文、返回链接、按钮、错误信息、图片 alt、document.title、description 和 `<html lang>` 同步更新。 | DOM 断言。 |
| AC-I18N-004 | 任一语言界面不存在翻译 key、`undefined`、`null` 或另一语言的明显残片。 | 文本扫描 + 人工审阅。 |
| AC-THEME-001 | 深浅主题下正文、按钮、链接和焦点环达到 WCAG AA 对比度；页面内容不包含写死的白色文本。 | axe/对比度工具 + 静态扫描。 |

## 7. 可访问性与交互

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-A11Y-001 | 只使用键盘可完成主导航、项目打开、返回、语言/主题切换、外链和灯箱关闭。 | 人工键盘测试。 |
| AC-A11Y-002 | 项目卡片本身是可聚焦的链接；Enter 打开详情，辅助技术能读出项目标题。 | DOM + Playwright + 屏幕阅读器抽查。 |
| AC-A11Y-003 | 所有交互元素在键盘聚焦时具有明显 focus-visible 样式。 | 截图检查。 |
| AC-A11Y-004 | 灯箱具有 dialog 语义；打开时焦点进入弹层，Tab 不逃逸，Escape 关闭，关闭后焦点回到原图。 | E2E。 |
| AC-A11Y-005 | 所有非装饰图片拥有准确 alt；同项目多张图不能全部使用“项目图片”这一通用描述。 | axe + 内容审阅。 |
| AC-A11Y-006 | axe 自动扫描无 critical 或 serious 级问题。 | CI axe。 |

## 8. 响应式与视觉

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-RWD-001 | 320、390、768、1024、1440、1920px 下无非预期横向滚动、文字遮挡或控件重叠。 | 视觉回归。 |
| AC-RWD-002 | 项目图片保持比例，灯箱关闭按钮始终可见，放大后仍可恢复和关闭。 | 移动/桌面交互测试。 |
| AC-RWD-003 | 中英文长标题不会溢出卡片、导航和按钮。 | 长文本 fixture。 |
| AC-MOTION-001 | 系统开启 reduced motion 后，平滑滚动、卡片位移和灯箱动画被关闭或显著减弱。 | 媒体查询 E2E。 |

## 9. SEO、性能和可靠性

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-SEO-001 | 首页和每个项目页拥有非空且唯一的 title、description、canonical 和 Open Graph title/description/image。 | 静态生成检查。 |
| AC-SEO-002 | favicon 返回 200，公开页面包含正确的 canonical、Open Graph 和结构化数据。 | HTTP/解析测试。 |
| AC-SEO-003 | 页面提供合法的 Person 或 CreativeWork JSON-LD。 | Schema.org validator。 |
| AC-PERF-001 | 移动端 Lighthouse Performance ≥ 90，Accessibility ≥ 95，Best Practices ≥ 95，SEO ≥ 95。 | CI Lighthouse，运行 3 次取中位数。 |
| AC-PERF-002 | 所有图片有 width/height；非首屏图片设置 lazy loading；不存在未使用的超大资源进入发布产物。 | DOM/构建产物检查。 |
| AC-REL-001 | 阻断 Marked 或图标 CDN 后，核心文字、导航和项目链接仍可使用。 | 请求拦截 E2E。 |
| AC-REL-002 | 页面加载与交互过程中 console 无 error、unhandled rejection 和 404。 | 全路径 E2E console 监听。 |

## 10. 浏览器矩阵

至少完成以下人工冒烟：

- Windows：当前 Chrome、Edge、Firefox。
- macOS/iOS：当前 Safari。
- Android：当前 Chrome。
- 视口：320×568、390×844、768×1024、1440×900、1920×1080。

## 11. 发布前检查清单

- [ ] 所有 P0 验收项通过。
- [ ] 中英文内容由申请者本人确认事实和翻译。
- [ ] 项目 1 占位英文、项目 3/4 重复问题已解决。
- [ ] 简历、邮箱、GitHub、文档、视频链接有效。
- [ ] Python 生成器从干净环境可复现输出。
- [ ] JSON Schema、单元测试、E2E、axe、链接检查全部通过。
- [ ] GitHub Pages 预发布地址完成桌面和移动端人工检查。
- [ ] 未提交隐私数据、密钥、本机绝对路径或临时文件。
- [ ] canonical、Open Graph、结构化数据和 favicon 已在生产域名验证。
