"""个人主页内容入口。

编辑本文件后，在项目根目录运行：
    python portfolio.py validate
    python portfolio.py build
    python portfolio.py preview

默认从现有 projects.json 载入全部项目，因此直接构建不会清空已有内容。
具体写法参见 docs/PYTHON_GUIDE.md。
"""

from pathlib import Path
import sys

from portfolio_content import Portfolio


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "assets" / "data" / "projects.json"

# 以当前网站数据为起点。已有项目会被完整保留。
portfolio = Portfolio.load(DATA_FILE)


# ── 在此处编写内容 ──────────────────────────────────────────────
#
# 新增项目示例（去掉每行开头的 # 后修改）：
#
# project = portfolio.add_project(
#     project_id="my-project",
#     title={"en": "My Project", "zh": "我的项目"},
#     summary={"en": "A short introduction.", "zh": "一句话项目简介。"},
#     thumbnail="assets/images/my-project/cover.jpg",
#     tags=("Robotics", "Python"),
#     featured=True,
#     year=2026,
# )
# page = portfolio.add_project_page("my-project", template="minimal")
# page.add_heading({"en": "Overview", "zh": "项目概览"})
# page.add_paragraph({"en": "Project details.", "zh": "项目详细介绍。"})
# page.add_image(
#     "assets/images/my-project/result.jpg",
#     alt={"en": "Project result", "zh": "项目成果"},
# )
# page.add_link("github", "https://github.com/your-name/your-project")
#
# 删除项目：portfolio.remove_project("project-id")


if __name__ == "__main__":
    # CLI 原本接收“命令 + 内容源”；根入口自动将自身作为内容源传入。
    from portfolio_content.cli import main

    if len(sys.argv) > 1 and sys.argv[1] in {"validate", "build", "preview"}:
        sys.argv.insert(2, str(Path(__file__).resolve()))
    raise SystemExit(main())
