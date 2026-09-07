# 实施状态矩阵

| 范围 | 状态 | 说明 |
|---|---|---|
| 详情页返回、移动导航、主题、双语 | 已实现 | 保留静态 GitHub Pages 兼容路径 |
| 项目 blocks、draft 过滤、上一项/下一项 | 已实现 | 草稿不进入公开项目导航 |
| Python 内容源、模板、原子写入、校验 | 已实现 | `portfolio.py validate/build/preview` |
| profile/education/workExperience/publications/awards/resume 数据模型 | 已实现 | 当前内容为明确标注的 TBD/draft 占位，不冒充事实 |
| SEO、canonical、OG、Person JSON-LD | 已实现 | `robots.txt` 与 `sitemap.xml` 属于可选搜索引擎配置，已按当前精简需求移除 |
| 第三方依赖本地化 | 已实现 | Markdown 解析器保存在 `assets/vendor/marked/`；6 个实际使用的 Font Awesome SVG 保存在 `assets/icons/`，页面不再加载图标字体或 CDN |
| Chromium 浏览器冒烟 | 已实现 | 已验证 390px 首页、项目详情、前后导航和中英文切换 |
| axe、Lighthouse、完整真实设备矩阵 | 未完成 | 仍需在发布 CI、Safari/iOS 和 Android 真机环境执行 |
| 真实教育/研究/奖项/简历内容 | 待资料 | 不得由工具臆造，需维护者提供并确认 |
