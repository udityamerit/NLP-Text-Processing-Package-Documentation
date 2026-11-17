"""Build the documentation site.

    python tools/build_docs.py

Requires the package (and its optional extras) to be importable, because every
example is executed and its real output is written into the page. Output goes
to the repository root: api.html, guide.html, installation.html, index.html and
search-index.js.
"""
from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import nlp_text_preprocessing as tp  # noqa: E402

import api_data  # noqa: E402
import layout as S  # noqa: E402

VERSION = tp.__version__
SEARCH: list[list[str]] = []   # [name, href, category, description]
IMPORT = "import nlp_text_preprocessing as tp"

GUIDE_SECTIONS: list[tuple[str, str]] = []   # filled by pages.py
API_GROUPS = [(g["id"], g["title"]) for g in api_data.GROUPS]


def in_tempdir(fn):
    old = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            return fn()
        finally:
            os.chdir(old)


def with_import(src: str) -> str:
    src = src.strip("\n")
    return src if IMPORT in src else f"{IMPORT}\n\n{src}"


def clean_type(t) -> str:
    t = str(t).strip("'\"")
    return t.replace("typing.", "").replace("Optional[", "Optional[")


def signature(entry) -> tuple[str, dict]:
    """Return (display signature, {param: (type, default)})."""
    obj = getattr(tp, entry["name"], None)
    meta: dict = {}
    if entry["sig"]:
        sig = entry["sig"]
        if obj is not None and "." not in entry["name"] and callable(obj):
            try:
                for p in inspect.signature(obj).parameters.values():
                    meta[p.name] = (clean_type(p.annotation) if p.annotation is not p.empty else "",
                                    None if p.default is p.empty else repr(p.default))
            except (TypeError, ValueError):
                pass
        if "." in entry["name"]:
            cls_name, meth = entry["name"].split(".", 1)
            fn = inspect.getattr_static(getattr(tp, cls_name), meth)
            fn = getattr(fn, "__func__", fn)
            for p in inspect.signature(fn).parameters.values():
                if p.name in ("self", "cls"):
                    continue
                meta[p.name] = (clean_type(p.annotation) if p.annotation is not p.empty else "",
                                None if p.default is p.empty else repr(p.default))
        return sig, meta
    s = inspect.signature(obj)
    parts = []
    for p in s.parameters.values():
        meta[p.name] = (clean_type(p.annotation) if p.annotation is not p.empty else "",
                        None if p.default is p.empty else repr(p.default))
        parts.append(p.name if p.default is p.empty else f"{p.name}={p.default!r}")
    return f"{entry['name']}({', '.join(parts)})", meta


def run_cli(argv: list[str], stdin: str | None) -> str:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONPATH=os.pathsep.join(sys.path))
    r = subprocess.run([sys.executable, "-m", "nlp_text_preprocessing", *argv], input=stdin, capture_output=True,
                       text=True, encoding="utf-8", env=env)
    return (r.stdout + r.stderr).rstrip()


def entry_html(e: dict, group_title: str) -> str:
    sig, meta = signature(e)
    ident = e["anchor"]
    rows = []
    for pname, pdesc in e["params"]:
        tname, default = meta.get(pname, ("", None))
        bits = []
        if tname and pname not in ("x", "x1", "x2", "text", "word"):
            bits.append(f"<code>{S.esc(tname)}</code>")
        elif pname in ("x", "x1", "x2", "text"):
            bits.append("<code>str</code>")
        if default is not None:
            bits.append(f"default <code>{S.esc(default)}</code>")
        prefix = " · ".join(bits)
        rows.append(f"<dt><code>{S.esc(pname)}</code></dt><dd>{prefix + ' — ' if prefix else ''}{S.md(pdesc)}</dd>")
    if e["returns"]:
        rows.append(f"<dt>Returns</dt><dd>{S.md(e['returns'])}</dd>")
    if e["needs"]:
        rows.append(f"<dt>Requires</dt><dd>{S.md(e['needs'])}</dd>")
    dl = f"<dl>\n{chr(10).join(rows)}</dl>" if rows else ""

    blocks = []
    if e["blocks"]:
        for lang, src, argv, stdin in e["blocks"]:
            out = run_cli(argv, (stdin + "\n") if stdin else None) if argv else None
            blocks.append(S.code(src, lang, output=out, run=False))
    else:
        py = with_import(e["code"])
        blocks.append(in_tempdir(lambda: S.code(py, "Python", run=e["run"], ctx=e["name"], namespace={})))
    note = f"\n{S.note(e['note'])}" if e["note"] else ""
    SEARCH.append([e["name"], f"api.html#{ident}", group_title, e["desc"]])
    return (f'<details class="entry" id="{ident}"><summary><span><code>{S.esc(sig)}</code><small>{S.md(e["desc"])}</small></span>{S.icon("chev")}</summary>\n'
            f'<div class="entry-body">\n{dl}\n{"".join(blocks)}{note}\n'
            f'<a class="permalink" href="#{ident}">Link to this entry</a></div></details>')


def build_api() -> str:
    all_names = {e["name"] for g in api_data.GROUPS for e in g["entries"]}
    missing = [n for n in tp.__all__ if n not in all_names and n != "__version__"]
    if missing:
        raise SystemExit(f"Undocumented public names: {missing}")
    total = sum(len(g["entries"]) for g in api_data.GROUPS)

    glance = []
    for g in api_data.GROUPS:
        chips = "".join(f'<a href="#{e["anchor"]}"><code>{S.esc(e["name"])}</code></a>' for e in g["entries"])
        glance.append(f'<h3><a href="#{g["id"]}">{S.esc(g["title"])}</a> <span class="count">{len(g["entries"])}</span></h3><div class="chips">{chips}</div>')
    sections = [f'<section class="doc-section" id="glance">\n<h2>All functions at a glance</h2>'
                f'<p>Select a name to jump to its entry. Every example below ran against version {VERSION}, and each output is real.</p>'
                f'{"".join(glance)}</section>']
    outline = [("glance", "At a glance")]
    for g in api_data.GROUPS:
        entries = "\n".join(entry_html(e, g["title"]) for e in g["entries"])
        sections.append(f'<section class="doc-section" id="{g["id"]}">\n<h2>{S.esc(g["title"])}</h2><p>{S.md(g["blurb"])}</p>\n'
                        f'<div class="entries">\n{entries}</div></section>')
        outline.append((g["id"], g["title"]))
        SEARCH.append([g["title"], f"api.html#{g['id']}", "API reference", g["blurb"]])
    body = S.intro("API reference", f"{total} functions, classes and commands in version {VERSION}. Open an entry for its parameters, return type and a runnable example.") \
        + S.reading("\n".join(sections), outline)
    return S.page(name="api", title="API reference", crumb=("Reference", "API reference"), version=VERSION,
                  description=f"Every function, class and command in nlp-text-preprocessing {VERSION}, with parameters, return types and runnable examples.",
                  body=body, api_groups=API_GROUPS, guide_sections=GUIDE_SECTIONS)


def write_search():
    rows = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in SEARCH)
    (ROOT / "search-index.js").write_text(
        f"// Generated by tools/build_docs.py for nlp-text-preprocessing {VERSION}. Do not edit by hand.\n"
        f"const documentationIndex = [\n{rows}\n];\n", encoding="utf-8")


def main():
    only_api = "--api-only" in sys.argv
    pages = {}
    try:
        import pages as P  # tools/pages.py (guide, installation, overview)
        GUIDE_SECTIONS[:] = P.GUIDE_SECTIONS
    except ImportError:
        P = None
    pages["api.html"] = build_api()
    if P and not only_api:
        pages.update(P.build(S, sys.modules[__name__]))
    for name, content in pages.items():
        (ROOT / name).write_text(content, encoding="utf-8", newline="\n")
        print("wrote", name, f"{len(content) // 1024} KB")
    write_search()
    print("wrote search-index.js", len(SEARCH), "entries")


if __name__ == "__main__":
    main()
