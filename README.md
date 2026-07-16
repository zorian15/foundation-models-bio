# Foundation Models for Biology

A static, bookdown-style textbook on how foundation models are applied to
biology — proteins, genomes, and cells — written for an **ML practitioner
learning the biology**. Every chapter runs one spine: *problem → models that
attempt it → what they do well + what is still hard*.

The book is generated from Markdown by a small Python build (no framework).

## Status

Scaffolded, not yet drafted. Every chapter renders as a navigable stub from its
outline in `toc.py`. The scope, structure, researched modality→model map, and
citation seed live in **`PLANNING.md`**. Authoring conventions live in
**`CLAUDE.md`** — read both before writing.

## Build

```bash
pip install markdown pymdown-extensions pygments matplotlib   # once
python figures/make_figures.py    # regenerate figures, cover, and icons
python build.py                   # regenerate docs/
python -m http.server -d docs     # preview at http://localhost:8000
```

`docs/` is build output and is gitignored; CI regenerates it on every push.

## Layout

| Path | Role |
|---|---|
| `PLANNING.md` | Scoped design, TOC, modality→model map, citation seed |
| `CLAUDE.md` | Authoring guide and conventions |
| `toc.py` | Single source of truth for structure |
| `references.py` / `quizzes.py` / `glossary.py` | Single sources of truth for citations, quizzes, glossary |
| `content/<slug>.md` | One Markdown file per drafted chapter (optional) |
| `figures/make_figures.py` | Generates every figure as SVG, plus cover/icons |
| `build.py` | The generator |

## Deploy

See `DEPLOY.md`. In short: push to a public GitHub repo, set **Settings → Pages
→ Source → GitHub Actions**, and the workflow builds and publishes on every push
to `main`.
