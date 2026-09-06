from __future__ import annotations
import argparse
import importlib.util
from pathlib import Path
from .builder import Portfolio

def load_source(path: str) -> Portfolio:
    source = Path(path)
    if source.suffix == ".json": return Portfolio.load(source)
    spec = importlib.util.spec_from_file_location("portfolio_source", source)
    if not spec or not spec.loader: raise ValueError(f"无法加载内容源: {source}")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    portfolio = getattr(module, "portfolio", None)
    if not isinstance(portfolio, Portfolio): raise ValueError("内容文件必须暴露 portfolio = Portfolio(...)")
    return portfolio

def main() -> int:
    parser = argparse.ArgumentParser(prog="portfolio-content")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "build", "preview"): 
        command = sub.add_parser(name); command.add_argument("source"); command.add_argument("--output", default="assets/data/projects.json"); command.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    try:
        portfolio = load_source(args.source)
        report = portfolio.validate(root=Path.cwd())
        if not report.ok:
            print(report.format())
            return 1
        if args.command == "validate":
            print("内容校验通过")
            return 0
        portfolio.write(args.output, root=Path.cwd())
        print(f"已生成 {args.output}")
        if args.command == "preview":
            import functools
            import http.server
            print(f"预览地址：http://127.0.0.1:{args.port}/")
            http.server.test(HandlerClass=functools.partial(http.server.SimpleHTTPRequestHandler), port=args.port, bind="127.0.0.1")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}")
        return 1

if __name__ == "__main__": raise SystemExit(main())
