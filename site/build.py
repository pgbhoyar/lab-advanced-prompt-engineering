#!/usr/bin/env python3
"""Build the browsable workshop site.

Renders all workshop Markdown (labs, docs, rubrics, datasets, offline-fallback, prompts,
solutions, evaluation, top-level README, constitution) into styled HTML under site/, mirroring
the repository structure. Copies data files (.json/.jsonl) alongside. Rewrites in-content links
so `.md` becomes `.html` and everything stays inside the site.

The hand-written landing (site/index.html) and per-lab pages (site/labs/*/index.html) are NOT
regenerated; instead their outbound repository links are repointed to the in-site HTML mirror.

Run from the repository root:  python site/build.py
Markdown is the single source of truth — re-run this after editing any lab/doc Markdown.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

# Directories whose .md files are rendered to HTML (mirrored under site/).
MD_DIRS = ["docs", "rubrics", "labs", "datasets", "offline-fallback", "prompts", "solutions",
           "evaluation", "specs/001-advanced-prompt-workshop/contracts"]
# Individual extra Markdown files to render.
MD_EXTRA = ["README.md", "SECURITY.md", "CONTRIBUTING.md", ".specify/memory/constitution.md"]
# Plain files copied as-is so in-content links resolve.
COPY_FILES = ["LICENSE", ".gitignore"]
# Data files copied as-is (they render fine in a browser and stay linkable).
DATA_GLOBS = ["schemas/**/*.json", "datasets/**/*.jsonl", "prompts/**/*.json", "rubrics/**/*.json",
              "prompts/**/*.yaml"]

HREF_RE = re.compile(r'(href|src)="([^"]+)"')


def rel_prefix(rel_dir: Path) -> str:
    """Relative path from a page in rel_dir back to the site root."""
    depth = len(rel_dir.parts)
    return "../" * depth if depth else ""


def rewrite_link(url: str) -> str:
    """Rewrite an in-content link so it stays inside the site (.md -> .html)."""
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    path, _, frag = url.partition("#")
    if path.endswith(".md"):
        path = path[:-3] + ".html"
    return path + ("#" + frag if frag else "")


def rewrite_body_links(html: str) -> str:
    return HREF_RE.sub(lambda m: f'{m.group(1)}="{rewrite_link(m.group(2))}"', html)


_FENCE_OPEN = re.compile(r"^(\s*)(```+|~~~+)")


def dedent_fences(md_text: str) -> str:
    """Dedent fenced code blocks to column 0 so Python-Markdown renders them as code.

    The lab Markdown often nests ``` fences under list items (indented), which the fenced_code
    extension does not recognize. We strip only the common leading indentation of the fence, so
    code content's relative indentation is preserved.
    """
    out: list[str] = []
    in_fence = False
    indent = 0
    fence_char = ""
    for line in md_text.split("\n"):
        if not in_fence:
            m = _FENCE_OPEN.match(line)
            if m:
                in_fence = True
                indent = len(m.group(1))
                fence_char = m.group(2)[0]
                out.append(line[indent:] if line[:indent].strip() == "" else line.lstrip())
            else:
                out.append(line)
        else:
            j = 0
            while j < indent and j < len(line) and line[j] == " ":
                j += 1
            dedented = line[j:]
            out.append(dedented)
            if dedented.strip().startswith(fence_char * 3):
                in_fence = False
    return "\n".join(out)


def to_html(md_text: str) -> str:
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])
    return rewrite_body_links(md.convert(dedent_fences(md_text)))


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · Advanced Prompt Engineering</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
  <nav class="topbar" aria-label="Primary">
    <div class="topbar-left">
      <a href="{prefix}index.html">Advanced Prompt Engineering Labs</a>
    </div>
    <div class="topbar-right">
      <button type="button" class="theme-toggle" id="themeToggle" title="Toggle theme">🌙</button>
    </div>
  </nav>
  <main class="lab-page">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="{prefix}index.html">Home</a> / {crumb}
    </nav>
    <section class="lab-section">
{body}
    </section>
  </main>
  <script src="{prefix}assets/site.js"></script>
</body>
</html>
"""


def render_md(src: Path):
    rel = src.relative_to(ROOT)
    # Lab READMEs already have a hand-built index.html; render README.md as README.html beside it.
    out_rel = rel.with_suffix(".html")
    out = SITE / out_rel
    out.parent.mkdir(parents=True, exist_ok=True)

    md_text = src.read_text(encoding="utf-8")
    body = to_html(md_text)

    title = src.stem.replace("-", " ").title()
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    if m:
        title = m.group(1).strip()

    html = PAGE_TEMPLATE.format(
        title=title, prefix=rel_prefix(out_rel.parent), crumb=title, body=body
    )
    out.write_text(html, encoding="utf-8")
    return out


def copy_data(src: Path):
    rel = src.relative_to(ROOT)
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out)


def repoint(page: Path, up_from: str):
    """Repoint outbound repo links in a hand-written index page to the in-site mirror.

    up_from is the leading path the hand-written page uses to escape into the repo
    (e.g. "../../../" from site/labs/NN/, or "../" from site/). Dropping one level keeps
    the link inside site/, and .md -> .html points at the rendered mirror.
    """
    text = page.read_text(encoding="utf-8")
    text = text.replace(f'="{up_from}', f'="{up_from[3:]}')  # drop one leading ../
    text = re.sub(r'="([^"]+?)\.md(#[^"]*)?"', lambda m: f'="{m.group(1)}.html{m.group(2) or ""}"', text)
    page.write_text(text, encoding="utf-8")


def main():
    rendered = 0
    for d in MD_DIRS:
        for src in sorted((ROOT / d).rglob("*.md")):
            render_md(src)
            rendered += 1
    for extra in MD_EXTRA:
        p = ROOT / extra
        if p.exists():
            # constitution/README render to site/<name>.html at site root or mirrored path.
            rel = p.relative_to(ROOT)
            if len(rel.parts) > 1:
                render_md(p)
            else:
                body = to_html(p.read_text(encoding="utf-8"))
                # Root-level pages (README/SECURITY) reference site/ pages relatively.
                body = body.replace('="site/', '="')
                (SITE / rel.with_suffix(".html")).write_text(
                    PAGE_TEMPLATE.format(title=p.stem, prefix="", crumb=p.stem, body=body),
                    encoding="utf-8",
                )
            rendered += 1

    copied = 0
    for pattern in DATA_GLOBS:
        for src in sorted(ROOT.glob(pattern)):
            copy_data(src)
            copied += 1
    for name in COPY_FILES:
        p = ROOT / name
        if p.exists():
            shutil.copy2(p, SITE / name)
            copied += 1

    # Repoint hand-written pages to the in-site mirror.
    repoint(SITE / "index.html", "../")
    for idx in sorted((SITE / "labs").glob("*/index.html")):
        repoint(idx, "../../../")

    print(f"Rendered {rendered} Markdown page(s); copied {copied} data file(s).")


if __name__ == "__main__":
    main()
