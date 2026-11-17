"""Shared helpers for the docs generator: page chrome, code blocks and live example runner.

Every code example in the documentation is executed against the installed
package while the site is built, so the "Output" blocks are real.
"""
from __future__ import annotations

import contextlib
import html
import io
import keyword
import re
import tokenize

REPO = "https://github.com/udityamerit/Text-Processing-Package-For-Natural-Language-Processing"
PYPI = "https://pypi.org/project/nlp-text-preprocessing/"
AUTHOR = "https://udityanarayantiwari.netlify.app/"

I = {
    "home": "m3 10 9-7 9 7v10H3z M9 20v-7h6v7",
    "install": "M12 3v12 m-5-5 5 5 5-5 M4 16v4h16v-4",
    "bolt": "m14 2-10 12h7l-1 8L21 9h-8z",
    "flow": "M3 3h6v5H3z M15 16h6v5h-6z M6 8v8a2 2 0 0 0 2 2h7 M13 5h5v7",
    "table": "M3 4h18v16H3z M3 9h18 M9 9v11",
    "layers": "m12 3 9 5-9 5-9-5z M3 12l9 5 9-5 M3 16l9 5 9-5",
    "code": "m7 7-5 5 5 5 m10-10 5 5-5 5 m-4-14-4 18",
    "box": "m3 7 9-5 9 5-9 5z M3 7v10l9 5 9-5V7 M12 12v10 M7 5l9 5",
    "gh": "M9 20c-4 1-4-2-6-2 M15 22v-4c0-1 0-1.6-.7-2.2 3.1-.4 6.3-1.6 6.3-7A5.3 5.3 0 0 0 19.2 5c.2-1 .2-2.3-.3-3.1 0 0-1.2-.4-3.8 1.4a14 14 0 0 0-6.3 0C6.2 1.5 5 1.9 5 1.9 4.5 3 4.5 4.2 4.8 5a5.3 5.3 0 0 0-1.5 3.8c0 5.4 3.3 6.6 6.4 7-.6.6-.8 1.3-.8 2.2v4",
    "ext": "M7 17 18 6 M8 6h10v10",
    "chart": "M3 3v17h18 M7 15l4-5 4 2 5-7",
    "chev": "m9 5 7 7-7 7",
    "arrow": "M4 12h15 m-6-6 6 6-6 6",
    "term": "M3 4h18v16H3z M6 8l4 4-4 4 M13 16h4",
    "copy": "M8 8h12v13H8z M16 8V3H3v13h5",
    "book": "M3 4h7c1 0 2 1 2 2 0-1 1-2 2-2h7v15h-7c-1 0-2 1-2 2 0-1-1-2-2-2H3z M12 6v15",
    "info": "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0 M12 11v6 M12 7h.01",
    "search": "M16 16l5 5 M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0",
    "close": "m5 5 14 14 M19 5 5 19",
    "menu": "M3 6h18 M3 12h18 M3 18h18",
    "sun": "M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0 M12 1v3 M12 20v3 M1 12h3 M20 12h3 M4 4l2 2 M18 18l2 2 M4 20l2-2 M18 6l2-2",
    "moon": "M20 15A9 9 0 0 1 9 3a9 9 0 1 0 11 12z",
    "shield": "M12 2 4 5v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V5z",
    "cog": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M19 12l2-1-1-3-2 .5-1.5-1.5.5-2-3-1-1 2h-2L9.5 3l-3 1 .5 2L5.5 7.5 3.5 7l-1 3 2 1v2l-2 1 1 3 2-.5 1.5 1.5-.5 2 3 1 1-2h2l1 2 3-1-.5-2 1.5-1.5 2 .5 1-3-2-1z",
}


def icon(name: str) -> str:
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="{I[name]}"/></svg>'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def md(s: str) -> str:
    """Tiny inline markup: `code` and **bold**; everything else is escaped."""
    out = esc(s)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    return out


# --------------------------------------------------------------------------- code

def highlight(src: str) -> str:
    """Python syntax highlighting with the classes the stylesheet already defines."""
    src = src.rstrip("\n")
    lines = src.split("\n")
    marks = []  # (row, col_start, col_end, cls)
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src + "\n").readline):
            cls = None
            if tok.type == tokenize.STRING:
                cls = "str"
            elif tok.type == tokenize.COMMENT:
                cls = "comment"
            elif tok.type == tokenize.NUMBER:
                cls = "num"
            elif tok.type == tokenize.NAME and keyword.iskeyword(tok.string) and tok.string not in ("True", "False", "None"):
                cls = "kw"
            elif tok.type == tokenize.NAME and tok.string in ("True", "False", "None"):
                cls = "num"
            if cls and tok.start[0] == tok.end[0]:
                marks.append((tok.start[0] - 1, tok.start[1], tok.end[1], cls))
            elif cls:  # multi-line string
                for row in range(tok.start[0] - 1, tok.end[0]):
                    a = tok.start[1] if row == tok.start[0] - 1 else 0
                    b = tok.end[1] if row == tok.end[0] - 1 else len(lines[row])
                    marks.append((row, a, b, cls))
    except (tokenize.TokenError, IndentationError):
        pass
    by_row: dict[int, list] = {}
    for m in marks:
        by_row.setdefault(m[0], []).append(m)
    out = []
    for r, line in enumerate(lines):
        pos, buf = 0, []
        for _, a, b, cls in sorted(by_row.get(r, []), key=lambda m: m[1]):
            buf.append(esc(line[pos:a]))
            buf.append(f'<span class="{cls}">{esc(line[a:b])}</span>')
            pos = b
        buf.append(esc(line[pos:]))
        out.append("".join(buf))
    return "\n".join(out)


def highlight_shell(src: str) -> str:
    out = []
    for line in src.rstrip("\n").split("\n"):
        if line.lstrip().startswith("#"):
            out.append(f'<span class="comment">{esc(line)}</span>')
        else:
            out.append(esc(line))
    return "\n".join(out)


def copy_button(label: str) -> str:
    return (f'<button class="copy" type="button" aria-label="Copy {label} code">{icon("copy")} <span>Copy</span></button>')


def run_python(src: str, namespace: dict | None = None) -> str:
    """Execute an example and return what it printed (trailing whitespace trimmed)."""
    buf = io.StringIO()
    ns = namespace if namespace is not None else {}
    with contextlib.redirect_stdout(buf):
        exec(compile(src, "<example>", "exec"), ns)
    return buf.getvalue().rstrip()


class ExampleError(RuntimeError):
    pass


def code(src: str, lang: str = "Python", output: str | None = None, run: bool = True,
         namespace: dict | None = None, ctx: str = "") -> str:
    """A code block with copy button. Python blocks are executed to fill the Output panel."""
    src = src.strip("\n")
    if lang == "Python":
        if run and output is None:
            try:
                output = run_python(src, namespace)
            except Exception as exc:  # surface the broken example with context
                raise ExampleError(f"example failed ({ctx}): {type(exc).__name__}: {exc}\n---\n{src}") from exc
        body = highlight(src)
    elif lang in ("Terminal", "PowerShell", "Bash", "CMD"):
        body = highlight_shell(src)
    else:
        body = esc(src)
    result = ""
    if output:
        result = f'<div class="result"><span>Output</span><samp>{esc(output)}</samp></div>'
    icon_name = "term"
    return (f'<div class="code-block">\n<div class="code-bar"><span>{icon(icon_name)} {esc(lang)}</span>{copy_button(esc(lang))}</div>\n'
            f'<pre tabindex="0" translate="no"><code>{body}</code></pre>{result}</div>')


def note(text: str, kind: str = "info") -> str:
    return f'<aside class="note">{icon("info")}\n<div>{md(text)}</div></aside>'


def table(head: list[str], rows: list[list[str]], cls: str = "ref-table") -> str:
    h = "".join(f"<th scope=\"col\">{md(c)}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{md(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


# --------------------------------------------------------------------------- chrome

def nav_link(href: str, label: str, ic: str, ext: bool = False, current: bool = False) -> str:
    cur = ' aria-current="page"' if current else ""
    tail = icon("ext") if ext else ""
    return f'<a href="{href}"{cur}>{icon(ic)}{esc(label)}{tail}</a>'


def sidebar(page: str, version: str, api_groups: list[tuple[str, str]], guide_sections: list[tuple[str, str]]) -> str:
    g = "".join(nav_link(f"guide.html#{i}", t, "flow") for i, t in guide_sections)
    a = "".join(nav_link(f"api.html#{i}", t, "code") for i, t in api_groups)
    return f"""<aside id="sidebar" class="sidebar">
<nav aria-label="Documentation">
<div class="nav-section">
<h2>Getting started</h2>{nav_link("index.html", "Overview", "home", current=page == "index")}
{nav_link("installation.html", "Installation", "install", current=page == "installation")}
{nav_link("index.html#quick-start", "Quick start", "bolt")}</div>
<div class="nav-section">
<h2>User guide</h2>{g}</div>
<div class="nav-section">
<h2>API reference</h2>{nav_link("api.html", "All functions", "book", current=page == "api")}
{a}</div>
<div class="nav-section project">
<h2>Project</h2>{nav_link(PYPI, "PyPI package", "box", True)}
{nav_link(REPO, "Source code", "gh", True)}
{nav_link(REPO + "/blob/main/CHANGELOG.md", "Changelog", "layers", True)}
{nav_link("https://pepy.tech/projects/nlp-text-preprocessing", "Download statistics", "chart", True)}</div></nav>
<a class="release" href="{PYPI}{version}/"><span class="release-icon">{icon("layers")}</span><span>Package version<small>v{version}</small></span>{icon("ext")}</a></aside>"""


def page(*, name: str, title: str, description: str, crumb: tuple[str, str], body: str, version: str,
         api_groups, guide_sections, outline: list[tuple[str, str]] | None = None) -> str:
    sep = icon("chev")
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · nlp-text-preprocessing</title><meta name="theme-color" content="#ffffff"><meta name="color-scheme" content="light dark"><meta name="description" content="{esc(description)}">
<link rel="icon" href="mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="index.css">
<script>try {{ if (localStorage.getItem('docs-theme') === 'dark') document.documentElement.dataset.theme = 'dark'; }} catch {{}}</script>
<script src="search-index.js" defer></script><script src="app.js" defer></script>
<noscript><style>.menu,.search-open,.theme,.copy{{display:none}}</style></noscript>
</head><body>
<a href="#main-content" class="skip">Skip to content</a>
<header class="top"><button class="icon-btn menu" aria-label="Open navigation" aria-expanded="false" aria-controls="sidebar">{icon("menu")}</button>
<a class="brand" translate="no" href="index.html"><span class="mark" aria-hidden="true"></span><span>nlp-text-preprocessing</span></a><span class="header-tag">Docs</span>
<div class="utilities"><button class="search-open" aria-label="Search documentation">{icon("search")}<span>Search docs…</span><kbd>Ctrl K</kbd></button>
<a class="repo" href="{REPO}">{icon("gh")}<span>GitHub</span>{icon("ext")}</a><button class="icon-btn theme" aria-label="Switch to dark theme">{icon("sun")}{icon("moon")}</button></div></header><noscript>
<nav class="plain-nav" aria-label="Documentation pages"><a href="index.html">Overview</a>
<a href="installation.html">Installation</a>
<a href="guide.html">User guide</a>
<a href="api.html">API reference</a></nav></noscript>
<div class="layout">
{sidebar(name, version, api_groups, guide_sections)}
<main id="main-content" tabindex="-1">
<div class="content">
<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Docs</a>{sep}<span>{esc(crumb[0])}</span>{sep}<strong aria-current="page">{esc(crumb[1])}</strong></nav>
{body}
<footer><span><span class="mark" aria-hidden="true"></span> nlp-text-preprocessing v{version}</span><a href="{AUTHOR}">Uditya Narayan Tiwari {icon("ext")}</a></footer></div></main></div>
<dialog class="search-dialog" aria-labelledby="search-title">
<div class="search-head">
<h2 id="search-title">Search documentation</h2><button class="icon-btn close-search" aria-label="Close search">{icon("close")}</button></div>
<label class="search-field">{icon("search")}<input type="search" name="docs-search" autocomplete="off" spellcheck="false" placeholder="Try pipeline or word_count…" aria-label="Search guides and API functions"></label><p class="search-status" role="status"></p>
<div class="results"></div></dialog>
</body></html>
"""


def outline_nav(items: list[tuple[str, str]]) -> str:
    links = "\n".join(f'<a href="#{i}">{md(t)}</a>' for i, t in items)
    return f'<nav class="page-outline" aria-label="On this page">\n<h2>On this page</h2>{links}</nav>'


def reading(article: str, outline: list[tuple[str, str]]) -> str:
    return f'<div class="reading-layout">\n<article>\n{article}\n</article>\n{outline_nav(outline)}</div>'


def intro(h1: str, text: str) -> str:
    return f'<div class="article-intro">\n<h1>{esc(h1)}</h1><p>{md(text)}</p></div>'
