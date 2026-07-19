"""Generate every figure for *Foundation Models for Biology* as SVG.

Two kinds of figure live here. **Diagrams** (concepts) are hand-authored SVG
emitted from Python string templates. **Plots** (anything quantitative) are
matplotlib, saved transparent with `svg.fonttype: "none"` so their text inherits
the page fonts. Both draw from the palette constants below, which mirror
`assets/style.css` — keep them in sync.

Run with `python figures/make_figures.py`. Each `fig_*()` returns the path it
wrote and is listed in `FIGURES`; `main()` runs them all. The cover and icons
carry the book's visual identity (a folding sequence with contact arcs — a
sequence becoming a structure) and are written to the assets root.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "assets" / "figures"
ASSETS_DIR = ROOT / "assets"

# The book's palette, mirrored from assets/style.css. Keep these in sync.
PAPER = "#f4f3ee"
INK = "#17181b"
INK_SOFT = "#3b3d42"
MUTED = "#6a6d73"
RULE = "#e4e3dd"
RULE_STRONG = "#cfcdc4"
ACCENT = "#274b6d"
ACCENT_SOFT = "#eaf0f6"
AMBER = "#9c6b12"
VIOLET = "#6b4f9c"
BRICK = "#b04a3f"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "'Charter', 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif"
MONO = "'SF Mono', 'SFMono-Regular', ui-monospace, Menlo, Consolas, monospace"


def write_svg(name: str, svg: str) -> Path:
    """Write a raw SVG string to the figures directory and return its path."""
    assert name.endswith(".svg"), f"Figure name must end in .svg, got '{name}'."
    assert svg.lstrip().startswith("<svg"), f"Figure '{name}' is not an SVG document."
    path = OUTPUT_DIR / name
    path.write_text(svg, encoding="utf-8")
    return path


def write_root_asset(name: str, svg: str) -> Path:
    """Write a raw SVG string to the assets root (cover, icon) and return its path."""
    assert name.endswith(".svg"), f"Asset name must end in .svg, got '{name}'."
    assert svg.lstrip().startswith("<svg"), f"Asset '{name}' is not an SVG document."
    path = ASSETS_DIR / name
    path.write_text(svg, encoding="utf-8")
    return path


def svg_doc(width: float, height: float, label: str, body: list[str]) -> str:
    """Wrap SVG body elements in a document with the book's default font.

    `label` becomes the accessible description; keep it plain ASCII so it needs
    no escaping. `body` is the list of element strings, in draw order.
    """
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="{SANS}" role="img" aria-label="{label}">'
    )
    return "\n".join([head, *body, "</svg>"])


def arrow_marker(color: str, name: str) -> str:
    """Return a `<defs>` block holding one triangular arrowhead marker."""
    return (
        f'<defs><marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker></defs>'
    )


def node_box(
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    fill: str = "#ffffff",
    stroke: str = RULE_STRONG,
    text_fill: str = INK,
    font_size: float = 12,
    weight: int = 400,
) -> list[str]:
    """Return a rounded rectangle with centered text: the book's labelled chip."""
    stroke_attr = "none" if stroke == "none" else stroke
    return [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" '
        f'fill="{fill}" stroke="{stroke_attr}"/>',
        f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + font_size * 0.35:.1f}" '
        f'font-size="{font_size}" font-weight="{weight}" text-anchor="middle" '
        f'fill="{text_fill}">{text}</text>',
    ]


def eyebrow(x: float, y: float, text: str, fill: str = MUTED) -> str:
    """Return a small uppercase section label, as used across the diagrams."""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="11" font-weight="700" '
        f'fill="{fill}" letter-spacing="1">{text}</text>'
    )


def style_plot() -> None:
    """Apply the book's typographic style to matplotlib's global state."""
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
            "font.size": 9,
            "text.color": INK,
            "axes.edgecolor": RULE_STRONG,
            "axes.labelcolor": INK_SOFT,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "grid.color": RULE,
            "grid.linewidth": 0.8,
            "legend.frameon": False,
            "legend.fontsize": 8,
            "svg.fonttype": "none",  # Keep text as text so it inherits page fonts.
        }
    )


def save_plot(fig: plt.Figure, name: str) -> Path:
    """Save a matplotlib figure as a transparent SVG and close it."""
    assert name.endswith(".svg"), f"Figure name must end in .svg, got '{name}'."
    path = OUTPUT_DIR / name
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Example figure. One worked diagram so a drafter has a pattern to copy; it is
# not yet referenced by any chapter. Delete or replace it as real figures land.
# ---------------------------------------------------------------------------


def fig_example_modality_map() -> Path:
    """Diagram: the modality-to-model thread, as a data-then-model pipeline."""
    width, height = 640, 200
    body = [arrow_marker(ACCENT, "arrow")]
    body.append(eyebrow(24, 34, "THE COMMON THREAD"))

    stages = [
        ("Assay", "RNA-seq, DMS,\nATAC, Hi-C", ACCENT_SOFT),
        ("Modality", "sequence, structure,\ntracks, variation", "#ffffff"),
        ("Model", "protein & DNA\nfoundation models", ACCENT_SOFT),
    ]
    box_w, box_h, gap = 168, 96, 60
    x = 24
    for i, (title, detail, fill) in enumerate(stages):
        y = 66
        body.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="10" '
            f'fill="{fill}" stroke="{RULE_STRONG}"/>'
        )
        body.append(
            f'<text x="{x + box_w / 2:.1f}" y="{y + 30}" font-size="15" '
            f'font-weight="700" text-anchor="middle" fill="{INK}">{title}</text>'
        )
        for j, line in enumerate(detail.split("\n")):
            body.append(
                f'<text x="{x + box_w / 2:.1f}" y="{y + 54 + j * 18}" font-size="12" '
                f'text-anchor="middle" fill="{INK_SOFT}">{line}</text>'
            )
        if i < len(stages) - 1:
            ax = x + box_w + 6
            body.append(
                f'<line x1="{ax}" y1="{y + box_h / 2}" x2="{ax + gap - 12}" '
                f'y2="{y + box_h / 2}" stroke="{ACCENT}" stroke-width="2" '
                f'marker-end="url(#arrow)"/>'
            )
        x += box_w + gap

    return write_svg(
        "example-modality-map.svg",
        svg_doc(width, height, "Assay to modality to model pipeline.", body),
    )


# ---------------------------------------------------------------------------
# The cover and the icons.
#
# One motif carries the book's identity: a chain of residues that folds back on
# itself, with dashed contacts bridging parts that are far apart in sequence but
# close in space — a sequence becoming a structure. An amber node closes the
# chain, tying the visual identity to the companion LLM book.
# ---------------------------------------------------------------------------


def folding_chain_svg(
    points: list[tuple[float, float]],
    contacts: list[tuple[int, int]],
    node_r: float,
    stroke_w: float,
) -> str:
    """Emit the folding-chain motif: backbone, dashed contacts, graded nodes.

    `points` are node centers in draw order; `contacts` are index pairs joined by
    a dashed line (drawn behind the backbone). The final node is amber.
    """
    parts = []
    for i, j in contacts:
        xi, yi = points[i]
        xj, yj = points[j]
        parts.append(
            f'<line x1="{xi:.1f}" y1="{yi:.1f}" x2="{xj:.1f}" y2="{yj:.1f}" '
            f'stroke="{MUTED}" stroke-width="{stroke_w * 0.5:.2f}" '
            f'stroke-dasharray="4 3" opacity="0.5"/>'
        )
    path_d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    parts.append(
        f'<path d="{path_d}" fill="none" stroke="{ACCENT}" '
        f'stroke-width="{stroke_w:.2f}" stroke-linecap="round" '
        f'stroke-linejoin="round" opacity="0.85"/>'
    )
    n = len(points)
    for idx, (x, y) in enumerate(points):
        last = idx == n - 1
        fill = AMBER if last else ACCENT
        opacity = 1.0 if last else 0.42 + 0.58 * (idx + 1) / n
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r:.1f}" fill="{fill}" '
            f'opacity="{opacity:.2f}"/>'
        )
    return "\n".join(parts)


# A beta-hairpin fold: a top strand left-to-right, a turn, a bottom strand back,
# with cross-strand contacts. Shared by the cover and (scaled) the icons.
COVER_POINTS = [
    (110, 600),
    (178, 600),
    (246, 600),
    (314, 600),
    (382, 600),
    (450, 600),
    (500, 636),
    (450, 672),
    (382, 672),
    (314, 672),
    (246, 672),
    (178, 672),
]
COVER_CONTACTS = [(1, 11), (2, 10), (3, 9), (4, 8)]

ICON_POINTS = [
    (42, 72),
    (76, 72),
    (110, 72),
    (144, 72),
    (164, 90),
    (144, 108),
    (110, 108),
    (76, 108),
]
ICON_CONTACTS = [(1, 7), (2, 6)]


def fig_cover() -> Path:
    """The book cover: title over the folding-chain motif, framed like a monograph."""
    width, height = 640, 960
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="Book cover: Foundation Models for Biology. '
        f"A chain of residues folding back on itself with dashed contacts, a "
        f'sequence becoming a structure.">',
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
        f'<rect x="26" y="26" width="{width - 52}" height="{height - 52}" '
        f'fill="none" stroke="{RULE_STRONG}" stroke-width="1.5"/>',
        f'<text x="72" y="152" font-family="{SANS}" font-size="16" '
        f'font-weight="650" letter-spacing="5" fill="{ACCENT}">'
        f"FOR THE ML PRACTITIONER</text>",
    ]
    for i, line in enumerate(("Foundation", "Models for", "Biology")):
        parts.append(
            f'<text x="68" y="{232 + i * 72}" font-family="{SERIF}" font-size="58" '
            f'font-weight="700" fill="{INK}">{line}</text>'
        )

    parts.append(folding_chain_svg(COVER_POINTS, COVER_CONTACTS, node_r=14, stroke_w=3))

    parts.append(
        f'<path d="M 72 830 L 148 830" stroke="{RULE_STRONG}" stroke-width="1.5"/>'
    )
    for i, line in enumerate(
        ("How foundation models fit modern", "molecular biology and drug discovery.")
    ):
        parts.append(
            f'<text x="72" y="{862 + i * 23}" font-family="{SANS}" font-size="15.5" '
            f'fill="{MUTED}">{line}</text>'
        )
    parts.append("</svg>")
    return write_root_asset("cover.svg", "\n".join(parts))


def fig_icon() -> Path:
    """The favicon: the folding-chain motif alone on a rounded paper tile."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" role="img" '
        'aria-label="Site icon: a short residue chain folding back with contacts.">',
        f'<rect width="180" height="180" rx="36" fill="{PAPER}"/>',
        folding_chain_svg(ICON_POINTS, ICON_CONTACTS, node_r=8, stroke_w=2.4),
        "</svg>",
    ]
    return write_root_asset("icon.svg", "\n".join(parts))


def fig_touch_icon() -> Path:
    """The apple-touch-icon: the favicon motif, full-bleed PNG (iOS rounds it).

    iOS does not accept SVG here, so matplotlib re-draws the same geometry as
    `fig_icon` at exactly 180 by 180 pixels.
    """
    from matplotlib.lines import Line2D
    from matplotlib.patches import Circle, Rectangle

    dpi = 100
    fig = plt.figure(figsize=(1.8, 1.8), dpi=dpi)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_xlim(0, 180)
    ax.set_ylim(180, 0)  # Flip y so the geometry matches the SVG coordinates.
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 180, 180, facecolor=PAPER, edgecolor="none"))

    px = 72 / dpi  # One SVG stroke pixel is this many matplotlib points.

    for i, j in ICON_CONTACTS:
        xi, yi = ICON_POINTS[i]
        xj, yj = ICON_POINTS[j]
        ax.add_line(
            Line2D(
                [xi, xj],
                [yi, yj],
                color=MUTED,
                linewidth=1.2 * px,
                linestyle=(0, (4, 3)),
                alpha=0.5,
            )
        )

    xs = [p[0] for p in ICON_POINTS]
    ys = [p[1] for p in ICON_POINTS]
    ax.add_line(
        Line2D(
            xs,
            ys,
            color=ACCENT,
            linewidth=2.4 * px,
            solid_capstyle="round",
            solid_joinstyle="round",
            alpha=0.85,
        )
    )

    n = len(ICON_POINTS)
    for idx, (x, y) in enumerate(ICON_POINTS):
        last = idx == n - 1
        ax.add_patch(
            Circle(
                (x, y),
                radius=8,
                facecolor=AMBER if last else ACCENT,
                edgecolor="none",
                alpha=1.0 if last else 0.42 + 0.58 * (idx + 1) / n,
            )
        )

    path = ASSETS_DIR / "apple-touch-icon.png"
    fig.savefig(path, dpi=dpi, facecolor=PAPER)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Chapter figures (Part I), integrated from the drafting workflow.
# ---------------------------------------------------------------------------


def fig_pretrain_recipe() -> Path:
    w, h = 640, 262
    body = [arrow_marker(ACCENT, "arw")]
    body.append(eyebrow(24, 28, "ONE RECIPE, MANY MODALITIES"))
    # Draw each stage as the box rect plus a top-aligned title and detail lines
    # stacked below it, so the title never overlaps its subtitles.
    body.append(node_box(24, 76, 150, 84, "", fill=PAPER)[0])
    body.append(
        f'<text x="99" y="104" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">unlabeled corpus</text>'
    )
    body.append(
        f'<text x="99" y="128" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">proteins · DNA</text>'
    )
    body.append(
        f'<text x="99" y="145" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">· cells ·</text>'
    )
    body.append(
        f'<line x1="174" y1="118" x2="222" y2="118" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw)"/>'
    )
    body.append(node_box(224, 76, 156, 84, "", fill=PAPER)[0])
    body.append(
        f'<text x="302" y="104" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">self-supervised</text>'
    )
    body.append(
        f'<text x="302" y="128" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">pretraining:</text>'
    )
    body.append(
        f'<text x="302" y="145" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">predict masked token</text>'
    )
    body.append(
        f'<line x1="380" y1="118" x2="428" y2="118" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw)"/>'
    )
    body.append(node_box(430, 76, 186, 84, "", fill=ACCENT_SOFT, stroke=ACCENT)[0])
    body.append(
        f'<text x="523" y="104" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">foundation model</text>'
    )
    body.append(
        f'<text x="523" y="130" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">reusable representations</text>'
    )
    tasks = [(40, "structure"), (245, "variant effect"), (450, "design")]
    for tx, label in tasks:
        body += node_box(tx, 204, 150, 42, label, fill=PAPER, font_size=12)
        cx = tx + 75
        body.append(
            f'<line x1="523" y1="160" x2="{cx}" y2="202" stroke="{RULE_STRONG}" stroke-width="1.5" marker-end="url(#arw)"/>'
        )
    return write_svg(
        "pretrain-recipe.svg",
        svg_doc(
            w,
            h,
            "One recipe, many modalities: corpus to pretraining to model to tasks.",
            body,
        ),
    )


def fig_two_lobes() -> Path:
    w, h = 640, 276
    body = [arrow_marker(ACCENT, "arw2")]
    body.append(eyebrow(24, 28, "ONE JOURNEY, TWO LOBES"))
    # Draw each lobe as the box rect plus a top-aligned title and two detail
    # lines stacked below it, so the title never overlaps its subtitles.
    body.append(node_box(24, 60, 258, 104, "", fill=PAPER)[0])
    body.append(
        f'<text x="153" y="96" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{INK}">molecular / therapeutic</text>'
    )
    body.append(
        f'<text x="153" y="122" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">proteins · structure</text>'
    )
    body.append(
        f'<text x="153" y="140" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">binding · design</text>'
    )
    body.append(node_box(358, 60, 258, 104, "", fill=PAPER)[0])
    body.append(
        f'<text x="487" y="96" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{INK}">genomic / regulatory</text>'
    )
    body.append(
        f'<text x="487" y="122" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">DNA · expression</text>'
    )
    body.append(
        f'<text x="487" y="140" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">variants · splicing</text>'
    )
    body.append(
        f'<text x="320" y="105" text-anchor="middle" font-family="{SERIF}" font-size="12" font-style="italic" fill="{MUTED}">central</text>'
    )
    body.append(
        f'<text x="320" y="121" text-anchor="middle" font-family="{SERIF}" font-size="12" font-style="italic" fill="{MUTED}">dogma</text>'
    )
    body += node_box(
        210,
        218,
        220,
        44,
        "multimodal integration",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=13,
        weight=600,
    )
    body.append(
        f'<line x1="153" y1="164" x2="290" y2="216" stroke="{ACCENT}" stroke-width="1.5" marker-end="url(#arw2)"/>'
    )
    body.append(
        f'<line x1="487" y1="164" x2="350" y2="216" stroke="{ACCENT}" stroke-width="1.5" marker-end="url(#arw2)"/>'
    )
    return write_svg(
        "two-lobes.svg",
        svg_doc(
            w, h, "Molecular and genomic lobes bridged by multimodal integration.", body
        ),
    )


def fig_chapter_spine() -> Path:
    w, h = 640, 178
    body = [arrow_marker(ACCENT, "arw3")]
    body.append(eyebrow(24, 30, "THE SPINE OF EVERY PROBLEM CHAPTER"))
    body += node_box(
        24, 66, 170, 66, "the problem", fill=PAPER, font_size=14, weight=600
    )
    body.append(
        f'<text x="109" y="116" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">the biology to solve</text>'
    )
    body.append(
        f'<line x1="194" y1="99" x2="233" y2="99" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw3)"/>'
    )
    body += node_box(
        235, 66, 170, 66, "the models", fill=PAPER, font_size=14, weight=600
    )
    body.append(
        f'<text x="320" y="116" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">what attacks it now</text>'
    )
    body.append(
        f'<line x1="405" y1="99" x2="444" y2="99" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw3)"/>'
    )
    body += node_box(
        446,
        66,
        170,
        66,
        "what is still hard",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=14,
        weight=600,
    )
    body.append(
        f'<text x="531" y="116" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">the honest limits</text>'
    )
    return write_svg(
        "chapter-spine.svg",
        svg_doc(w, h, "Problem, then models, then what is still hard.", body),
    )


def fig_problem_map() -> Path:
    w, h = 640, 226
    body = [arrow_marker(ACCENT, "pmarw")]
    body.append(eyebrow(24, 32, "THE TEMPLATE BEHIND EVERY CHAPTER"))
    body += node_box(
        30,
        64,
        168,
        80,
        "the problem",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=14,
        weight=600,
    )
    body += node_box(236, 64, 168, 80, "the models", font_size=14, weight=600)
    body += node_box(
        442,
        64,
        168,
        80,
        "the gaps",
        fill="#fbf1df",
        stroke=AMBER,
        font_size=14,
        weight=600,
    )
    body.append(
        f'<line x1="198" y1="104" x2="236" y2="104" stroke="{ACCENT}" stroke-width="2" marker-end="url(#pmarw)"/>'
    )
    body.append(
        f'<line x1="404" y1="104" x2="442" y2="104" stroke="{ACCENT}" stroke-width="2" marker-end="url(#pmarw)"/>'
    )
    body.append(
        f'<path d="M 526 144 C 526 190, 114 190, 114 144" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#pmarw)"/>'
    )
    body.append(
        f'<text x="320" y="205" font-size="11" text-anchor="middle" fill="{MUTED}">what stays hard reframes the next problem</text>'
    )
    return write_svg(
        "problem-map.svg",
        svg_doc(w, h, "Problem feeds models feeds gaps, looping back.", body),
    )


def fig_molecular_pipeline() -> Path:
    w, h = 640, 205
    body = [arrow_marker(ACCENT, "mparw")]
    body.append(eyebrow(24, 30, "ONE THERAPEUTIC PIPELINE, FIVE PROBLEMS"))
    labels = [
        ("target", "Ch 6"),
        ("property", "Ch 7"),
        ("structure", "Ch 8"),
        ("design", "Ch 9"),
        ("cell", "Ch 10"),
    ]
    bw, gap = 104, 20
    for i, (name, ch) in enumerate(labels):
        bx = 16 + i * (bw + gap)
        fill = ACCENT_SOFT if i == 0 else "#ffffff"
        stroke = ACCENT if i == 0 else RULE_STRONG
        body += node_box(
            bx, 78, bw, 58, name, fill=fill, stroke=stroke, font_size=13, weight=600
        )
        body.append(
            f'<text x="{bx + bw / 2:.1f}" y="156" font-size="11" text-anchor="middle" fill="{MUTED}">{ch}</text>'
        )
    for i in range(len(labels) - 1):
        x1 = 16 + i * (bw + gap) + bw
        x2 = x1 + gap
        body.append(
            f'<line x1="{x1}" y1="107" x2="{x2}" y2="107" stroke="{ACCENT}" stroke-width="2" marker-end="url(#mparw)"/>'
        )
    body.append(
        f'<text x="320" y="186" font-size="11" text-anchor="middle" fill="{MUTED}">pick it, characterize it, see it, build it, put it to work</text>'
    )
    return write_svg(
        "molecular-pipeline.svg",
        svg_doc(w, h, "Five molecular problems along a therapeutic pipeline.", body),
    )


def fig_sequence_to_function() -> Path:
    w, h = 640, 235
    body = [arrow_marker(ACCENT, "s2farw")]
    body.append(eyebrow(24, 30, "SEQUENCE TO FUNCTION"))
    body += node_box(
        24,
        92,
        150,
        60,
        "~1 Mb DNA window",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=12,
        weight=600,
    )
    body += node_box(232, 92, 120, 60, "sequence model", font_size=12, weight=600)
    body.append(
        f'<line x1="174" y1="122" x2="232" y2="122" stroke="{ACCENT}" stroke-width="2" marker-end="url(#s2farw)"/>'
    )
    body.append(
        f'<line x1="352" y1="122" x2="408" y2="122" stroke="{ACCENT}" stroke-width="2" marker-end="url(#s2farw)"/>'
    )
    offs = [0, 7, -5, 9, -6, 4, -8, 6, -3, 7, 0]
    tracks = [
        ("RNA-seq", ACCENT),
        ("ATAC", VIOLET),
        ("ChIP-seq", AMBER),
        ("Hi-C", BRICK),
    ]
    for i, (name, color) in enumerate(tracks):
        ty = 72 + i * 38
        pts = " ".join(f"{418 + k * 14},{ty + offs[k]}" for k in range(11))
        body.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.6"/>'
        )
        body.append(
            f'<text x="566" y="{ty + 4}" font-size="10" text-anchor="start" fill="{MUTED}">{name}</text>'
        )
    return write_svg(
        "sequence-to-function.svg",
        svg_doc(w, h, "One DNA window predicts many regulatory tracks.", body),
    )


def fig_allele_frequency_spectrum() -> Path:
    w, h = 640, 300
    body = [arrow_marker(INK, "afsarw")]
    body.append(eyebrow(24, 30, "VARIANT TO MECHANISM ACROSS THE FREQUENCY SPECTRUM"))
    body.append(
        f'<line x1="96" y1="58" x2="96" y2="252" stroke="{RULE_STRONG}" stroke-width="1.5"/>'
    )
    body.append(
        f'<line x1="96" y1="252" x2="606" y2="252" stroke="{RULE_STRONG}" stroke-width="1.5"/>'
    )
    body.append(
        f'<text x="351" y="284" font-size="12" text-anchor="middle" fill="{INK_SOFT}">allele frequency:  rare  to  common</text>'
    )
    body.append(
        f'<text x="36" y="155" font-size="12" text-anchor="middle" fill="{INK_SOFT}" transform="rotate(-90 36 155)">effect size:  large  to  small</text>'
    )
    body.append(
        f'<path d="M 122 84 C 250 98, 300 222, 592 240" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    )
    for cx, cy in [(140, 96), (162, 112), (128, 120), (180, 100), (150, 132)]:
        body.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{BRICK}"/>')
    for cx, cy in [
        (470, 236),
        (502, 242),
        (540, 238),
        (562, 244),
        (432, 232),
        (410, 228),
    ]:
        body.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{ACCENT}"/>')
    body += node_box(
        150,
        150,
        214,
        28,
        "rare + large: Mendelian, AlphaMissense",
        fill="#fdecea",
        stroke=BRICK,
        font_size=10,
    )
    body += node_box(
        356,
        186,
        236,
        28,
        "common + small: GWAS, LD, fine-mapping",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=10,
    )
    return write_svg(
        "allele-frequency-spectrum.svg",
        svg_doc(w, h, "Rare large-effect versus common small-effect variants.", body),
    )


def fig_attention_context() -> Path:
    w, h = 640, 250
    body = [arrow_marker(RULE_STRONG, "af1")]
    body.append(eyebrow(24, 28, "TOKEN -> VECTOR -> CONTEXT-AWARE VECTOR"))
    residues = ["M", "K", "T", "A", "Y"]
    x0, step, bw = 70, 100, 56
    vy = 150
    for i, r in enumerate(residues):
        cx = x0 + i * step + bw // 2
        body += node_box(x0 + i * step, 52, bw, 38, r, font_size=15, weight=600)
        body.append(
            f'<line x1="{cx}" y1="90" x2="{cx}" y2="{vy}" '
            f'stroke="{RULE_STRONG}" stroke-width="1.5" marker-end="url(#af1)"/>'
        )
    for i in range(len(residues)):
        fill = ACCENT_SOFT if i == 2 else PAPER
        body += node_box(x0 + i * step, vy, bw, 36, "vec", fill=fill, font_size=11)
    center = x0 + 2 * step + bw // 2
    for i in range(len(residues)):
        if i == 2:
            continue
        cx = x0 + i * step + bw // 2
        mid = (center + cx) // 2
        body.append(
            f'<path d="M {center} {vy + 36} Q {mid} 235 {cx} {vy + 36}" '
            f'fill="none" stroke="{VIOLET}" stroke-width="1.5" opacity="0.55"/>'
        )
    return write_svg(
        "attention-context.svg",
        svg_doc(
            w,
            h,
            "A token becomes a vector, and attention blends the other positions into it.",
            body,
        ),
    )


def fig_model_families() -> Path:
    w, h = 640, 300
    body = [eyebrow(24, 28, "THREE FAMILIES, THREE JOBS")]
    cols = [
        (
            30,
            "Encoder",
            "masked fill-in",
            ["ESM-2, ESM C,", "Nucleotide Transf."],
            ["representations,", "variant scoring"],
            ACCENT_SOFT,
        ),
        (
            235,
            "Decoder",
            "next-token",
            ["ProGen2,", "Evo 2"],
            ["generation,", "naturalness scores"],
            PAPER,
        ),
        (
            440,
            "Diffusion",
            "iterative denoise",
            ["AlphaFold3,", "RFdiffusion"],
            ["structures,", "molecules"],
            PAPER,
        ),
    ]
    bw = 170
    for x, title, mech, models, good, fill in cols:
        cx = x + bw // 2
        body += node_box(x, 52, bw, 66, "", fill=fill)
        body.append(
            f'<text x="{cx}" y="80" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{INK}">{title}</text>'
        )
        body.append(
            f'<text x="{cx}" y="102" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{mech}</text>'
        )
        yy = 146
        for line in models:
            body.append(
                f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{INK_SOFT}">{line}</text>'
            )
            yy += 17
        body.append(
            f'<text x="{cx}" y="212" text-anchor="middle" font-family="{SANS}" font-size="10.5" letter-spacing="0.08em" fill="{ACCENT}">GOOD FOR</text>'
        )
        yy = 232
        for line in good:
            body.append(
                f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{INK}">{line}</text>'
            )
            yy += 17
    return write_svg(
        "model-families.svg",
        svg_doc(
            w,
            h,
            "Encoders represent, decoders generate, diffusion builds 3D structure.",
            body,
        ),
    )


def fig_pretrain_transfer() -> Path:
    w, h = 640, 250
    body = [arrow_marker(ACCENT, "apt")]
    body.append(eyebrow(24, 28, "PRETRAIN ONCE, TRANSFER MANY WAYS"))
    body += node_box(24, 90, 176, 64, "", fill=ACCENT_SOFT)
    body.append(
        f'<text x="112" y="118" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{INK}">unlabeled corpus</text>'
    )
    body.append(
        f'<text x="112" y="138" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">UniProt, genomes</text>'
    )
    body += node_box(250, 90, 150, 64, "foundation model", font_size=12, weight=600)
    body.append(
        f'<line x1="200" y1="122" x2="250" y2="122" stroke="{ACCENT}" stroke-width="2" marker-end="url(#apt)"/>'
    )
    body.append(
        f'<line x1="400" y1="112" x2="450" y2="66" stroke="{ACCENT}" stroke-width="2" marker-end="url(#apt)"/>'
    )
    body.append(
        f'<line x1="400" y1="132" x2="450" y2="182" stroke="{ACCENT}" stroke-width="2" marker-end="url(#apt)"/>'
    )
    body += node_box(450, 40, 166, 52, "")
    cx = 533
    body.append(
        f'<text x="{cx}" y="62" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{INK}">fine-tune</text>'
    )
    body.append(
        f'<text x="{cx}" y="80" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">+ small labeled set</text>'
    )
    body += node_box(450, 150, 166, 72, "")
    body.append(
        f'<text x="{cx}" y="172" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{INK}">zero-shot scoring</text>'
    )
    body.append(
        f'<text x="{cx}" y="190" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">mask a site, compare</text>'
    )
    body.append(
        f'<text x="{cx}" y="208" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{INK_SOFT}">log P(mut) - log P(wt)</text>'
    )
    return write_svg(
        "pretrain-transfer.svg",
        svg_doc(
            w,
            h,
            "Pretrain once, then transfer by fine-tuning or by zero-shot likelihood.",
            body,
        ),
    )


def fig_sequence_structure_fitness() -> Path:
    w, h = 640, 250
    body = [eyebrow(24, 28, "THREE VIEWS OF ONE PROTEIN")]
    # Panel 1: sequence (abundant).
    body += node_box(24, 56, 180, 130, "", fill=PAPER)
    body.append(
        f'<text x="114" y="80" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">sequence</text>'
    )
    body.append(
        f'<text x="114" y="116" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{ACCENT}">M K T A Y I</text>'
    )
    body.append(
        f'<text x="114" y="138" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{ACCENT}">A K L V F W</text>'
    )
    body.append(
        f'<text x="114" y="172" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">abundant / cheap</text>'
    )
    # Panel 2: structure (scarce).
    body += node_box(230, 56, 180, 130, "", fill=PAPER)
    body.append(
        f'<text x="320" y="80" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">structure</text>'
    )
    pts = [(268, 150), (292, 118), (324, 132), (348, 104), (372, 128)]
    path = " ".join(
        ("M" if i == 0 else "L") + f"{x} {y}" for i, (x, y) in enumerate(pts)
    )
    body.append(f'<path d="{path}" fill="none" stroke="{VIOLET}" stroke-width="3"/>')
    for x, y in pts:
        body.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{VIOLET}"/>')
    body.append(
        f'<text x="320" y="172" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">scarce / expensive</text>'
    )
    # Panel 3: fitness map (the label).
    body += node_box(436, 56, 180, 130, "", fill=PAPER)
    body.append(
        f'<text x="526" y="80" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">fitness map</text>'
    )
    cols = [AMBER, ACCENT_SOFT, BRICK, ACCENT_SOFT, AMBER, BRICK]
    for r in range(3):
        for c in range(6):
            fill = cols[(r + c) % len(cols)]
            body.append(
                f'<rect x="{462 + c * 20}" y="{94 + r * 16}" width="17" height="13" fill="{fill}" stroke="{PAPER}" stroke-width="1"/>'
            )
    body.append(
        f'<text x="526" y="172" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">mutation x position</text>'
    )
    return write_svg(
        "sequence-structure-fitness.svg",
        svg_doc(w, h, "Sequence, structure, and fitness for one protein.", body),
    )


def fig_regulatory_tracks() -> Path:
    w, h = 640, 360
    body = [eyebrow(24, 26, "ONE LOCUS, FIVE QUESTIONS")]
    lanes = [
        (
            "RNA-seq",
            "transcript abundance",
            [(150, 22), (180, 30), (210, 26), (240, 34), (270, 20)],
        ),
        ("ATAC", "open chromatin", [(140, 28), (300, 24), (400, 30)]),
        ("ChIP-seq", "protein binding", [(250, 34)]),
        ("CAGE", "start-site activity", [(150, 40)]),
    ]
    x0 = 150
    for i, (name, sub, peaks) in enumerate(lanes):
        base = 60 + i * 48
        body.append(
            f'<text x="24" y="{base - 4}" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">{name}</text>'
        )
        body.append(
            f'<text x="24" y="{base + 12}" font-family="{SANS}" font-size="10" fill="{MUTED}">{sub}</text>'
        )
        body.append(
            f'<line x1="{x0}" y1="{base + 14}" x2="616" y2="{base + 14}" stroke="{RULE}" stroke-width="1"/>'
        )
        for px, ph in peaks:
            body.append(
                f'<rect x="{px}" y="{base + 14 - ph}" width="16" height="{ph}" fill="{ACCENT}" rx="2"/>'
            )
    # Hi-C mini contact triangle.
    hy = 60 + 4 * 48
    body.append(
        f'<text x="24" y="{hy - 4}" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">Hi-C</text>'
    )
    body.append(
        f'<text x="24" y="{hy + 12}" font-family="{SANS}" font-size="10" fill="{MUTED}">3D contacts</text>'
    )
    shades = [VIOLET, ACCENT_SOFT, AMBER]
    tri_top = hy + 20
    for r in range(3):
        for c in range(3 - r):
            body.append(
                f'<rect x="{x0 + c * 18 + r * 9}" y="{tri_top + r * 16}" width="16" height="14" fill="{shades[(r + c) % 3]}" stroke="{PAPER}" stroke-width="1"/>'
            )
    # Shared genome axis.
    ay = h - 24
    body.append(
        f'<line x1="{x0}" y1="{ay}" x2="616" y2="{ay}" stroke="{RULE_STRONG}" stroke-width="2"/>'
    )
    body.append(
        f'<text x="{x0}" y="{ay + 16}" font-family="{SANS}" font-size="10" fill="{MUTED}">genomic position along the chromosome</text>'
    )
    return write_svg(
        "regulatory-tracks.svg",
        svg_doc(
            w, h, "Regulatory assays as stacked tracks over a shared genome axis.", body
        ),
    )


def fig_assay_to_signal() -> Path:
    w, h = 640, 280
    body = [arrow_marker(ACCENT, "a2s")]
    body.append(eyebrow(24, 26, "IS THE READOUT AN INPUT OR A TARGET?"))
    body.append(
        f'<text x="96" y="52" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">INPUT</text>'
    )
    body.append(
        f'<text x="320" y="52" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">MODEL</text>'
    )
    body.append(
        f'<text x="544" y="52" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">TARGET</text>'
    )
    rows = [
        ("DNA sequence", "Enformer / Borzoi", "regulatory tracks"),
        ("amino-acid sequence", "AlphaFold / ESMFold", "3D structure"),
        ("sequence + variant", "protein LM (ESM)", "fitness score"),
    ]
    for i, (inp, mdl, out) in enumerate(rows):
        y = 64 + i * 68
        body += node_box(24, y, 144, 46, inp, fill=PAPER, font_size=11)
        body += node_box(
            248, y, 144, 46, mdl, fill=ACCENT_SOFT, font_size=11, weight=600
        )
        body += node_box(472, y, 144, 46, out, fill=PAPER, font_size=11)
        body.append(
            f'<line x1="168" y1="{y + 23}" x2="248" y2="{y + 23}" stroke="{ACCENT}" stroke-width="2" marker-end="url(#a2s)"/>'
        )
        body.append(
            f'<line x1="392" y1="{y + 23}" x2="472" y2="{y + 23}" stroke="{ACCENT}" stroke-width="2" marker-end="url(#a2s)"/>'
        )
    return write_svg(
        "assay-to-signal.svg",
        svg_doc(
            w,
            h,
            "Three model families, each reading inputs and graded on targets.",
            body,
        ),
    )


def fig_ld_tag_not_cause() -> Path:
    w, h = 640, 300
    x0, yt, x1, yb = 90, 60, 610, 200
    body = [arrow_marker(ACCENT, "ld-arw")]
    body.append(eyebrow(24, 30, "THE TOP HIT IS A TAG, NOT THE CAUSE"))
    body.append(
        f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" '
        f'stroke="{RULE_STRONG}" stroke-width="1.5"/>'
    )
    body.append(
        f'<text x="{x0}" y="{yb + 20}" font-family="{SANS}" '
        f'font-size="11" fill="{MUTED}">genomic position</text>'
    )
    body.append(
        f'<text x="{x0 - 10}" y="{yt + 4}" text-anchor="end" '
        f'font-family="{SANS}" font-size="11" fill="{INK_SOFT}">assoc.</text>'
    )
    heights = [0.08, 0.12, 0.2, 0.45, 0.7, 0.95, 0.8, 0.6, 0.3, 0.15, 0.09]
    n = len(heights)
    causal_idx = 4
    top_idx = 5
    xs = []
    for i, ht in enumerate(heights):
        cx = x0 + (i + 0.5) * ((x1 - x0) / n)
        cy = yb - ht * (yb - yt)
        xs.append((cx, cy))
        if i == top_idx:
            col, r = ACCENT, 7
        elif i == causal_idx:
            col, r = AMBER, 7
        else:
            col, r = MUTED, 5
        body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{col}"/>')
    bx0 = xs[3][0] - 8
    bx1 = xs[7][0] + 8
    by = yb + 30
    body.append(
        f'<path d="M {bx0:.0f} {by} L {bx0:.0f} {by + 8} '
        f'L {bx1:.0f} {by + 8} L {bx1:.0f} {by}" '
        f'fill="none" stroke="{RULE_STRONG}" stroke-width="1.2"/>'
    )
    bmid = (bx0 + bx1) / 2
    body.append(
        f'<text x="{bmid:.0f}" y="{by + 24}" text-anchor="middle" '
        f'font-family="{SANS}" font-size="11" fill="{INK_SOFT}">'
        f"one LD block: these SNPs are correlated</text>"
    )
    body.append(
        f'<text x="{xs[top_idx][0]:.0f}" y="{xs[top_idx][1] - 12:.0f}" '
        f'text-anchor="middle" font-family="{SANS}" font-size="11" '
        f'fill="{ACCENT}" font-weight="600">lead SNP</text>'
    )
    body.append(
        f'<text x="{xs[causal_idx][0]:.0f}" y="{xs[causal_idx][1] - 12:.0f}" '
        f'text-anchor="middle" font-family="{SANS}" font-size="11" '
        f'fill="{AMBER}" font-weight="600">true cause</text>'
    )
    return write_svg(
        "ld-tag-not-cause.svg",
        svg_doc(
            w,
            h,
            "A GWAS peak lights up a whole correlated block; the tallest SNP need not be the causal one.",
            body,
        ),
    )


def fig_association_to_causation() -> Path:
    w, h = 640, 320
    body = [arrow_marker(ACCENT, "atc-arw"), arrow_marker(MUTED, "atc-mut")]
    body.append(eyebrow(24, 30, "THREE ROUTES FROM ASSOCIATION TO CAUSE"))
    cols = [(24, "Fine-mapping"), (232, "Colocalization"), (440, "Mendelian rand.")]
    for cx, title in cols:
        body.append(
            f'<text x="{cx}" y="64" font-family="{SANS}" font-size="12.5" '
            f'fill="{INK}" font-weight="600">{title}</text>'
        )
    # Panel A: fine-mapping.
    ax = 24
    for i in range(7):
        body.append(f'<circle cx="{ax + 12 + i * 23}" cy="100" r="5" fill="{MUTED}"/>')
    body.append(
        f'<text x="{ax}" y="124" font-family="{SANS}" font-size="10.5" '
        f'fill="{MUTED}">associated SNPs (LD)</text>'
    )
    body.append(
        f'<line x1="{ax + 88}" y1="134" x2="{ax + 88}" y2="158" '
        f'stroke="{ACCENT}" stroke-width="2" marker-end="url(#atc-arw)"/>'
    )
    body += node_box(
        ax,
        168,
        192,
        48,
        "credible set: a few high-PIP SNPs",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=10,
    )
    # Panel B: colocalization.
    bx = 232
    offsets = [
        (-80, 0.02),
        (-60, 0.08),
        (-40, 0.25),
        (-24, 0.55),
        (-12, 0.82),
        (0, 1.0),
        (12, 0.82),
        (24, 0.55),
        (40, 0.25),
        (60, 0.08),
        (80, 0.02),
    ]
    peak = bx + 88

    def _curve(base_y, amp, color):
        pts = " ".join(f"{peak + dx},{base_y - amp * hf:.0f}" for dx, hf in offsets)
        return (
            f'<polyline points="{pts}" fill="none" '
            f'stroke="{color}" stroke-width="2"/>'
        )

    body.append(
        f'<line x1="{peak}" y1="78" x2="{peak}" y2="170" '
        f'stroke="{RULE}" stroke-width="1" stroke-dasharray="3 3"/>'
    )
    body.append(_curve(150, 66, ACCENT))
    body.append(_curve(158, 66, VIOLET))
    body.append(
        f'<text x="{bx}" y="190" font-family="{SANS}" font-size="10.5" '
        f'fill="{ACCENT}">GWAS</text>'
    )
    body.append(
        f'<text x="{bx + 44}" y="190" font-family="{SANS}" font-size="10.5" '
        f'fill="{VIOLET}">eQTL</text>'
    )
    body.append(
        f'<text x="{bx}" y="208" font-family="{SANS}" font-size="10.5" '
        f'fill="{MUTED}">same peak = shared cause</text>'
    )
    # Panel C: Mendelian randomization.
    vx, ex, tx, cy = 440, 494, 556, 100
    body += node_box(vx, cy, 46, 32, "variant", font_size=10)
    body += node_box(ex, cy, 54, 32, "exposure", font_size=10)
    body += node_box(tx, cy, 44, 32, "trait", font_size=10)
    body.append(
        f'<line x1="{vx + 46}" y1="{cy + 16}" x2="{ex}" y2="{cy + 16}" '
        f'stroke="{ACCENT}" stroke-width="1.8" marker-end="url(#atc-arw)"/>'
    )
    body.append(
        f'<line x1="{ex + 54}" y1="{cy + 16}" x2="{tx}" y2="{cy + 16}" '
        f'stroke="{ACCENT}" stroke-width="1.8" marker-end="url(#atc-arw)"/>'
    )
    body += node_box(
        ex - 4,
        cy + 66,
        62,
        30,
        "confounder",
        fill="#ffffff",
        stroke=RULE,
        text_fill=MUTED,
        font_size=9.5,
    )
    body.append(
        f'<line x1="{ex + 24}" y1="{cy + 66}" x2="{ex + 20}" y2="{cy + 34}" '
        f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3" '
        f'marker-end="url(#atc-mut)"/>'
    )
    body.append(
        f'<line x1="{ex + 42}" y1="{cy + 66}" x2="{tx + 16}" y2="{cy + 34}" '
        f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3" '
        f'marker-end="url(#atc-mut)"/>'
    )
    body.append(
        f'<text x="{vx}" y="{cy - 10}" font-family="{SANS}" font-size="9.5" '
        f'fill="{MUTED}">random at conception</text>'
    )
    return write_svg(
        "association-to-causation.svg",
        svg_doc(
            w,
            h,
            "Fine-mapping narrows variants, colocalization ties them to a gene, and Mendelian randomization uses inheritance as an instrument.",
            body,
        ),
    )


# Part II chapter figures.


def fig_target_funnel():
    body = [arrow_marker(RULE_STRONG, "tf_arrow")]
    body.append(eyebrow(20, 26, "FROM DISEASE TO A TARGET YOU CAN ACT ON"))
    stages = [
        ("Disease", "a phenotype", 112),
        ("Associated genes", "hundreds of loci", 84),
        ("Causal genes", "tens survive", 56),
        ("Druggable + causal", "a handful", 34),
    ]
    xs = [18, 176, 334, 492]
    w = 130
    mid = 152
    for (title, sub, h), x in zip(stages, xs):
        y = mid - h / 2
        body += node_box(x, y, w, h, title, font_size=11, weight=600)
        body.append(
            f'<text x="{x + w / 2}" y="252" font-family="{SANS}" '
            f'font-size="11" fill="{MUTED}" text-anchor="middle">{sub}</text>'
        )
    for i in range(3):
        x1 = xs[i] + w + 3
        x2 = xs[i + 1] - 4
        body.append(
            f'<line x1="{x1}" y1="{mid}" x2="{x2}" y2="{mid}" '
            f'stroke="{RULE_STRONG}" stroke-width="1.5" marker-end="url(#tf_arrow)"/>'
        )
    return write_svg("target-funnel.svg", svg_doc(640, 288, "target funnel", body))


def fig_target_evidence_integration():
    body = [arrow_marker(RULE_STRONG, "ev_arrow")]
    body.append(eyebrow(20, 24, "MANY WEAK SIGNALS, ONE RANKED LIST"))
    sources = [
        "Human genetics: GWAS, Mendelian, MR",
        "Network and omics embeddings",
        "Perturb-seq functional readouts",
        "Literature / LLM evidence synthesis",
        "Known drugs and tractability",
    ]
    x, w, h, gap, y0 = 20, 252, 36, 13, 42
    ys = []
    for i, s in enumerate(sources):
        y = y0 + i * (h + gap)
        ys.append(y)
        body += node_box(x, y, w, h, s, font_size=11)
    rx, ry, rw, rh = 404, 108, 200, 84
    body += node_box(
        rx,
        ry,
        rw,
        rh,
        "Prioritized targets",
        font_size=14,
        weight=600,
        fill=ACCENT_SOFT,
    )
    body.append(
        f'<text x="{rx + rw / 2}" y="{ry + rh + 20}" font-family="{SANS}" '
        f'font-size="11" fill="{MUTED}" text-anchor="middle">causal and druggable, ranked</text>'
    )
    for y in ys:
        body.append(
            f'<line x1="{x + w + 3}" y1="{y + h / 2}" x2="{rx - 5}" y2="{ry + rh / 2}" '
            f'stroke="{RULE_STRONG}" stroke-width="1.2" marker-end="url(#ev_arrow)"/>'
        )
    return write_svg(
        "target-evidence-integration.svg",
        svg_doc(640, 300, "evidence integration", body),
    )


def fig_genetic_support_success():
    body = [eyebrow(20, 26, "GENETIC SUPPORT ROUGHLY DOUBLES CLINICAL SUCCESS")]
    baseline = 212
    bars = [
        (150, 110, 52, MUTED, "No genetic support", "1x baseline", 158),
        (380, 110, 124, ACCENT, "Human-genetics support", "~2 to 2.6x", 86),
    ]
    body.append(
        f'<line x1="96" y1="{baseline}" x2="560" y2="{baseline}" '
        f'stroke="{RULE_STRONG}" stroke-width="1.2"/>'
    )
    for bx, bw, bh, color, cat, val, valy in bars:
        body.append(
            f'<rect x="{bx}" y="{baseline - bh}" width="{bw}" height="{bh}" '
            f'fill="{color}" rx="2"/>'
        )
        body.append(
            f'<text x="{bx + bw / 2}" y="{valy}" font-family="{SANS}" '
            f'font-size="12" fill="{INK}" text-anchor="middle" font-weight="600">{val}</text>'
        )
        body.append(
            f'<text x="{bx + bw / 2}" y="{baseline + 20}" font-family="{SANS}" '
            f'font-size="11" fill="{MUTED}" text-anchor="middle">{cat}</text>'
        )
    body.append(
        f'<text x="96" y="{baseline + 44}" font-family="{SANS}" font-size="10" '
        f'fill="{MUTED}">Relative probability a target reaches approval (Nelson 2015; Minikel 2024).</text>'
    )
    return write_svg(
        "genetic-support-success.svg",
        svg_doc(640, 272, "genetic support success", body),
    )


def fig_property_axes():
    body = [arrow_marker(RULE_STRONG, "arr")]
    body.append(eyebrow(30, 28, "ONE MOLECULE, MANY MEASURABLE PROPERTIES"))
    body += node_box(30, 128, 150, 52, "one variant", fill=ACCENT_SOFT, weight=600)
    props = [
        (44, "fitness / variant effect"),
        (92, "folding stability (ddG)"),
        (140, "binding affinity (Kd)"),
        (188, "expression / solubility"),
        (236, "ADMET (small molecules)"),
    ]
    for y, label in props:
        body += node_box(380, y, 230, 38, label)
        body.append(
            f'<line x1="180" y1="154" x2="380" y2="{y + 19}" '
            f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr)"/>'
        )
    return write_svg(
        "property-axes.svg",
        svg_doc(640, 300, "one variant maps to many measurable properties", body),
    )


def fig_variant_scoring():
    body = [arrow_marker(RULE_STRONG, "arr2")]
    body.append(eyebrow(30, 28, "TWO WAYS TO SCORE A VARIANT"))
    body += node_box(30, 130, 130, 50, "variant sequence")
    body += node_box(210, 130, 120, 50, "protein LM", fill=ACCENT_SOFT, weight=600)
    body.append(
        f'<line x1="160" y1="155" x2="210" y2="155" '
        f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr2)"/>'
    )
    # Zero-shot arm (upper).
    body += node_box(410, 55, 210, 48, "log p(mut) - log p(wt)", font_size=12)
    body.append(eyebrow(410, 120, "ZERO-SHOT:", fill=MUTED))
    body.append(eyebrow(410, 136, "NO LABELS NEEDED", fill=MUTED))
    body.append(
        f'<line x1="330" y1="142" x2="410" y2="90" '
        f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr2)"/>'
    )
    # Supervised arm (lower).
    body += node_box(410, 205, 210, 48, "trained property head")
    body.append(eyebrow(410, 270, "SUPERVISED:", fill=MUTED))
    body.append(eyebrow(410, 286, "NEEDS LABELED ASSAY DATA", fill=MUTED))
    body.append(
        f'<line x1="330" y1="168" x2="410" y2="220" '
        f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr2)"/>'
    )
    return write_svg(
        "variant-scoring.svg",
        svg_doc(640, 300, "likelihood-ratio arm versus supervised head arm", body),
    )


def fig_epistasis():
    body = [arrow_marker(RULE_STRONG, "arr3")]
    body.append(eyebrow(30, 28, "WHY ADDING UP SINGLE MUTATIONS FAILS"))
    body += node_box(40, 105, 120, 50, "wild type")
    body += node_box(250, 45, 150, 46, "+A: more stable")
    body += node_box(250, 165, 150, 46, "+B: more stable")
    body += node_box(
        470, 105, 140, 50, "+A +B: unfolds", fill=BRICK, text_fill="#ffffff", weight=600
    )
    body.append(
        f'<line x1="160" y1="120" x2="250" y2="68" '
        f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr3)"/>'
    )
    body.append(
        f'<line x1="160" y1="140" x2="250" y2="188" '
        f'stroke="{RULE_STRONG}" stroke-width="1.4" marker-end="url(#arr3)"/>'
    )
    body.append(
        f'<line x1="400" y1="68" x2="470" y2="122" '
        f'stroke="{BRICK}" stroke-width="1.4" marker-end="url(#arr3)"/>'
    )
    body.append(
        f'<line x1="400" y1="188" x2="470" y2="138" '
        f'stroke="{BRICK}" stroke-width="1.4" marker-end="url(#arr3)"/>'
    )
    return write_svg(
        "epistasis.svg",
        svg_doc(
            640,
            240,
            "two beneficial single mutations combine to unfold the protein",
            body,
        ),
    )


def fig_coevolution_signal():
    W, H = 640, 260
    body = [arrow_marker(ACCENT, "coev_arrow")]
    body.append(eyebrow(30, 28, "MULTIPLE SEQUENCE ALIGNMENT"))
    # Alignment block background.
    body.append(
        f'<rect x="30" y="52" width="300" height="172" rx="6" '
        f'fill="#ffffff" stroke="{RULE_STRONG}"/>'
    )
    rows_y = [82, 110, 138, 166, 194]
    dots = "·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·"
    for y in rows_y:
        body.append(
            f'<text x="44" y="{y + 4}" font-family="{MONO}" font-size="13" '
            f'fill="{MUTED}">{dots}</text>'
        )
    # Two co-varying columns, drawn over the dot texture.
    xi, xj, bw = 118, 236, 24
    for xb in (xi, xj):
        body.append(
            f'<rect x="{xb}" y="52" width="{bw}" height="172" fill="{ACCENT_SOFT}"/>'
        )
    body.append(
        f'<text x="{xi + bw / 2:.1f}" y="46" font-size="12" font-weight="700" '
        f'text-anchor="middle" fill="{ACCENT}">i</text>'
    )
    body.append(
        f'<text x="{xj + bw / 2:.1f}" y="46" font-size="12" font-weight="700" '
        f'text-anchor="middle" fill="{ACCENT}">j</text>'
    )
    col_i = ["V", "I", "V", "L", "I"]
    col_j = ["S", "A", "S", "T", "A"]
    for k, y in enumerate(rows_y):
        body.append(
            f'<text x="{xi + bw / 2:.1f}" y="{y + 4}" font-family="{MONO}" '
            f'font-size="13" font-weight="700" text-anchor="middle" '
            f'fill="{ACCENT}">{col_i[k]}</text>'
        )
        body.append(
            f'<text x="{xj + bw / 2:.1f}" y="{y + 4}" font-family="{MONO}" '
            f'font-size="13" font-weight="700" text-anchor="middle" '
            f'fill="{BRICK}">{col_j[k]}</text>'
        )
    # Arrow to the folded chain.
    body.append(
        f'<line x1="338" y1="138" x2="384" y2="138" stroke="{ACCENT}" '
        f'stroke-width="2" marker-end="url(#coev_arrow)"/>'
    )
    body.append(eyebrow(408, 28, "A SPATIAL CONTACT"))
    # Folded backbone glyph.
    body.append(
        f'<path d="M 400 96 C 440 62, 486 128, 520 100 S 596 156, 560 196" '
        f'fill="none" stroke="{RULE_STRONG}" stroke-width="3" '
        f'stroke-linecap="round"/>'
    )
    ri = (470, 122)
    rj = (508, 108)
    body.append(
        f'<line x1="{ri[0]}" y1="{ri[1]}" x2="{rj[0]}" y2="{rj[1]}" '
        f'stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="3 3"/>'
    )
    body.append(f'<circle cx="{ri[0]}" cy="{ri[1]}" r="7" fill="{ACCENT}"/>')
    body.append(f'<circle cx="{rj[0]}" cy="{rj[1]}" r="7" fill="{BRICK}"/>')
    body.append(
        f'<text x="{ri[0] - 12}" y="{ri[1] + 24}" font-size="12" font-weight="700" '
        f'text-anchor="middle" fill="{ACCENT}">i</text>'
    )
    body.append(
        f'<text x="{rj[0] + 14}" y="{rj[1] - 10}" font-size="12" font-weight="700" '
        f'text-anchor="middle" fill="{BRICK}">j</text>'
    )
    body.append(
        f'<text x="480" y="224" font-size="11" text-anchor="middle" '
        f'fill="{MUTED}">distant in sequence, adjacent in space</text>'
    )
    return write_svg(
        "coevolution-signal.svg", svg_doc(W, H, "coevolution signal", body)
    )


def fig_structure_model_families():
    W, H = 640, 300
    body = []
    body.append(eyebrow(30, 30, "STRUCTURE PREDICTORS, 2024-2026"))
    cols = [
        {
            "x": 30,
            "eyebrow": "INPUT: MSA (HOMOLOGS)",
            "name": "AlphaFold2",
            "fill": ACCENT_SOFT,
            "below": [
                "reads co-evolution",
                "from an alignment",
                "chains + AF-Multimer",
            ],
        },
        {
            "x": 245,
            "eyebrow": "INPUT: ONE SEQUENCE",
            "name": "ESMFold",
            "fill": "#ffffff",
            "below": ["PLM embeddings,", "no alignment step", "fast; weaker on hard"],
        },
        {
            "x": 460,
            "eyebrow": "INPUT: SEQ + LIGAND + NA",
            "name": "AF3 / Boltz / Chai",
            "fill": ACCENT_SOFT,
            "below": ["all-atom diffusion", "decoder", "complexes, ions, ligands"],
        },
    ]
    bw, bh, by = 150, 56, 108
    for c in cols:
        x = c["x"]
        body.append(
            f'<text x="{x}" y="84" font-size="10" font-weight="700" '
            f'fill="{MUTED}" letter-spacing="0.5">{c["eyebrow"]}</text>'
        )
        body.extend(
            node_box(
                x,
                by,
                bw,
                bh,
                c["name"],
                fill=c["fill"],
                stroke=RULE_STRONG,
                font_size=13,
                weight=700,
            )
        )
        ty = by + bh + 26
        for i, line in enumerate(c["below"]):
            body.append(
                f'<text x="{x + bw / 2:.1f}" y="{ty + i * 18}" font-size="11.5" '
                f'text-anchor="middle" fill="{INK_SOFT}">{line}</text>'
            )
    body.append(
        f'<text x="{W / 2}" y="280" font-size="11" text-anchor="middle" '
        f'fill="{MUTED}">Ranked head-to-head at CASP, the biennial blind competition</text>'
    )
    return write_svg(
        "structure-model-families.svg", svg_doc(W, H, "structure model families", body)
    )


def fig_static_vs_ensemble():
    W, H = 640, 260
    body = []
    # Divider.
    body.append(
        f'<line x1="320" y1="40" x2="320" y2="220" stroke="{RULE}" stroke-width="1"/>'
    )
    body.append(eyebrow(30, 30, "WHAT THE MODEL RETURNS"))
    body.append(eyebrow(345, 30, "WHAT THE MOLECULE DOES"))

    def backbone(x0, dy, color, opacity, width=3):
        return (
            f'<path d="M {x0} {150 + dy} C {x0 + 50} {88 + dy}, '
            f'{x0 + 120} {186 + dy}, {x0 + 190} {120 + dy}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}" '
            f'stroke-linecap="round"/>'
        )

    # Left: single predicted state.
    body.append(backbone(48, 0, ACCENT, 1.0))
    body.append(f'<circle cx="48" cy="150" r="5" fill="{ACCENT}"/>')
    body.append(f'<circle cx="238" cy="120" r="5" fill="{ACCENT}"/>')
    body.append(
        f'<text x="160" y="212" font-size="12" text-anchor="middle" '
        f'fill="{INK_SOFT}">one most-likely fold</text>'
    )
    # Right: an ensemble of states.
    body.append(backbone(362, -14, ACCENT, 0.85))
    body.append(backbone(362, 8, VIOLET, 0.7))
    body.append(backbone(362, 26, AMBER, 0.7))
    # A disordered tail extending off the last conformation.
    body.append(
        f'<path d="M 552 146 q 16 -20 30 -2 q 14 18 28 -2 q 12 -16 22 4" '
        f'fill="none" stroke="{BRICK}" stroke-width="2" stroke-linecap="round"/>'
    )
    body.append(
        f'<text x="476" y="212" font-size="12" text-anchor="middle" '
        f'fill="{INK_SOFT}">an ensemble of states</text>'
    )
    body.append(
        f'<text x="580" y="128" font-size="10.5" text-anchor="middle" '
        f'fill="{BRICK}">disorder</text>'
    )
    return write_svg(
        "static-vs-ensemble.svg",
        svg_doc(W, H, "static structure versus ensemble", body),
    )


def fig_design_inverts_prediction():
    W, H = 640, 220
    defs = arrow_marker(ACCENT, "arrow_di")
    body = [defs]
    # Forward / prediction row.
    body.append(eyebrow(60, 40, "FORWARD  —  PREDICTION (CH. 8)"))
    body += node_box(60, 52, 150, 46, "Sequence", font_size=13)
    body += node_box(430, 52, 150, 46, "Structure", font_size=13)
    body.append(
        f'<line x1="215" y1="75" x2="425" y2="75" stroke="{ACCENT}" '
        f'stroke-width="2" marker-end="url(#arrow_di)"/>'
    )
    body.append(
        f'<text x="320" y="68" text-anchor="middle" font-family="{SANS}" '
        f'font-size="11" fill="{MUTED}">trained predictor</text>'
    )
    # Inverse / design row.
    body.append(eyebrow(60, 138, "INVERSE  —  DESIGN (THIS CHAPTER)"))
    body += node_box(60, 150, 150, 46, "Function / shape", font_size=12)
    body += node_box(430, 150, 150, 46, "Novel molecule", font_size=12)
    body.append(
        f'<line x1="215" y1="173" x2="425" y2="173" stroke="{ACCENT}" '
        f'stroke-width="2" marker-end="url(#arrow_di)"/>'
    )
    body.append(
        f'<text x="320" y="166" text-anchor="middle" font-family="{SANS}" '
        f'font-size="11" fill="{MUTED}">generative model + filter</text>'
    )
    svg = svg_doc(W, H, "Prediction versus design directions", body)
    return write_svg("design-inverts-prediction.svg", svg)


def fig_design_generate_filter_validate():
    W, H = 640, 240
    defs = arrow_marker(INK, "arrow_gfv") + arrow_marker(BRICK, "arrow_gfv_rej")
    body = [defs]
    body.append(eyebrow(20, 26, "GENERATE  →  FILTER  →  VALIDATE"))
    boxes = [
        (20, "Backbone", ACCENT_SOFT),
        (180, "Sequence", ACCENT_SOFT),
        (340, "Refold + score", ACCENT_SOFT),
        (500, "Wet lab", AMBER),
    ]
    by, bh, bw = 108, 50, 120
    for bx, title, fill in boxes:
        body += node_box(bx, by, bw, bh, title, fill=fill, font_size=12, weight=600)
    # Forward arrows between boxes.
    for x0 in (140, 300, 460):
        body.append(
            f'<line x1="{x0}" y1="133" x2="{x0 + 40}" y2="133" stroke="{INK}" '
            f'stroke-width="2" marker-end="url(#arrow_gfv)"/>'
        )
    # Captions below each box.
    caps = [
        (80, ["diffusion:", "RFdiffusion, Chroma"]),
        (240, ["inverse folding:", "ProteinMPNN"]),
        (400, ["self-consistency:", "AlphaFold / ESMFold"]),
        (560, ["express &amp;", "measure binding"]),
    ]
    for cx, lines in caps:
        body.append(
            f'<text x="{cx}" y="178" text-anchor="middle" font-family="{SANS}" '
            f'font-size="10" fill="{MUTED}">'
            f'<tspan x="{cx}" dy="0">{lines[0]}</tspan>'
            f'<tspan x="{cx}" dy="13">{lines[1]}</tspan></text>'
        )
    # Reject loop arc from score box back to backbone box.
    body.append(
        f'<path d="M400,108 C 400,50 80,50 80,108" fill="none" stroke="{BRICK}" '
        f'stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#arrow_gfv_rej)"/>'
    )
    body.append(
        f'<text x="240" y="48" text-anchor="middle" font-family="{SANS}" '
        f'font-size="10.5" fill="{BRICK}">rejected (low pLDDT / high RMSD) → resample</text>'
    )
    svg = svg_doc(W, H, "Generate, filter, validate loop", body)
    return write_svg("design-generate-filter-validate.svg", svg)


def fig_design_silico_to_wetlab_funnel():
    W, H = 640, 250
    body = []
    body.append(eyebrow(40, 28, "IN SILICO  →  WET LAB"))
    x0 = 40
    stages = [
        (560, ACCENT_SOFT, "~10,000 backbones generated"),
        (360, ACCENT, "hundreds pass the self-consistency filter"),
        (160, AMBER, "~10–40% of ordered designs bind (target-dependent)"),
        (60, BRICK, "a handful show genuine catalytic function"),
    ]
    y = 52
    bh = 30
    for w, fill, label in stages:
        body.append(
            f'<text x="{x0}" y="{y - 6}" font-family="{SANS}" font-size="11" '
            f'fill="{INK}">{label}</text>'
        )
        body.append(
            f'<rect x="{x0}" y="{y}" width="{w}" height="{bh}" rx="3" '
            f'fill="{fill}" stroke="{RULE_STRONG}" stroke-width="1"/>'
        )
        y += 50
    body.append(
        f'<text x="{x0}" y="{y + 4}" font-family="{SANS}" font-size="10" '
        f'fill="{MUTED}">Headline success rates are quoted at a late, narrow slice; end-to-end yield is far smaller.</text>'
    )
    svg = svg_doc(W, H, "In-silico to wet-lab attrition funnel", body)
    return write_svg("design-silico-to-wetlab-funnel.svg", svg)


def fig_cell_state_programming():
    W, H = 640, 230
    body = [arrow_marker(ACCENT, "csp1"), arrow_marker(BRICK, "csp2")]
    body.append(eyebrow(30, 28, "MENU OF PERTURBATIONS"))
    chips = ["Knock out a gene", "Turn a gene on (CRISPRa)", "Wire a gene circuit"]
    for i, t in enumerate(chips):
        y = 42 + i * 46
        body += node_box(
            30, y, 190, 34, t, fill=ACCENT_SOFT, stroke=RULE_STRONG, font_size=12
        )
    body.append(
        '<path d="M 228 105 L 285 105" stroke="%s" stroke-width="2" fill="none" marker-end="url(#csp1)"/>'
        % ACCENT
    )
    body += node_box(
        290,
        80,
        120,
        50,
        "Cell state A",
        fill="#ffffff",
        stroke=RULE_STRONG,
        font_size=13,
        weight=600,
    )
    body.append(
        '<text x="350" y="150" font-size="11" fill="%s" text-anchor="middle">where the cell is</text>'
        % MUTED
    )
    body.append(
        '<path d="M 413 105 L 470 105" stroke="%s" stroke-width="2" fill="none" marker-end="url(#csp2)"/>'
        % BRICK
    )
    body += node_box(
        475,
        80,
        130,
        50,
        "Cell state B",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=13,
        weight=600,
    )
    body.append(
        '<text x="540" y="150" font-size="11" fill="%s" text-anchor="middle">the therapeutic goal</text>'
        % MUTED
    )
    body.append(
        '<text x="345" y="196" font-size="12" fill="%s" text-anchor="middle">Which perturbations move A toward B?</text>'
        % INK_SOFT
    )
    return write_svg(
        "cell-state-programming.svg",
        svg_doc(W, H, "perturbation menu nudging a cell from state A to state B", body),
    )


def fig_perturbation_response_model():
    W, H = 640, 230
    body = [arrow_marker(ACCENT, "prm")]
    body.append(eyebrow(30, 26, "PERTURB-SEQ (CHAPTER 4)"))
    body += node_box(
        30,
        42,
        170,
        36,
        "CRISPR guide = input",
        fill=ACCENT_SOFT,
        stroke=RULE_STRONG,
        font_size=11,
    )
    body += node_box(
        30,
        92,
        170,
        36,
        "scRNA-seq = readout",
        fill=ACCENT_SOFT,
        stroke=RULE_STRONG,
        font_size=11,
    )
    body.append(
        '<text x="115" y="150" font-size="11" fill="%s" text-anchor="middle">many (perturbation, response) pairs</text>'
        % MUTED
    )
    body.append(
        '<path d="M 205 85 L 260 85" stroke="%s" stroke-width="2" fill="none" marker-end="url(#prm)"/>'
        % ACCENT
    )
    body.append(eyebrow(272, 26, "MODEL"))
    body += node_box(
        265,
        50,
        190,
        70,
        "Perturbation-response model",
        fill="#ffffff",
        stroke=ACCENT,
        font_size=11,
        weight=600,
    )
    body.append(
        '<text x="360" y="142" font-size="11" fill="%s" text-anchor="middle">GEARS graph / State latent shift</text>'
        % MUTED
    )
    body.append(
        '<path d="M 460 85 L 505 85" stroke="%s" stroke-width="2" fill="none" marker-end="url(#prm)"/>'
        % ACCENT
    )
    body.append(eyebrow(512, 26, "PREDICTION"))
    body += node_box(
        505,
        50,
        120,
        70,
        "Predicted shift",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=12,
        weight=600,
    )
    body.append(
        '<text x="565" y="138" font-size="11" fill="%s" text-anchor="middle">for a held-out perturbation</text>'
        % MUTED
    )
    return write_svg(
        "perturbation-response-model.svg",
        svg_doc(
            W,
            H,
            "perturb-seq pairs train a model to predict a held-out perturbations expression shift",
            body,
        ),
    )


def fig_generalization_ladder():
    W, H = 640, 270
    body = [eyebrow(30, 26, "GENERALIZATION GETS HARDER")]
    rungs = [
        ("Seen perturbation", "linear baselines already strong", ACCENT_SOFT, ACCENT),
        ("Unseen single gene", "deep models roughly tie the mean", PAPER, RULE_STRONG),
        ("Combinatorial or new cell type", "open frontier", PAPER, BRICK),
    ]
    x0, bw, gap = 30, 185, 15
    for i, (t, note, fill, stroke) in enumerate(rungs):
        x = x0 + i * (bw + gap)
        y = 170 - i * 45
        body += node_box(
            x, y, bw, 44, t, fill=fill, stroke=stroke, font_size=11, weight=600
        )
        body.append(
            '<text x="%d" y="%d" font-size="11" fill="%s" text-anchor="middle">%s</text>'
            % (x + bw / 2, y + 62, MUTED, note)
        )
    return write_svg(
        "generalization-ladder.svg",
        svg_doc(
            W,
            H,
            "three rungs of perturbation generalization from easy to open frontier",
            body,
        ),
    )


FIGURES = (
    fig_target_funnel,
    fig_target_evidence_integration,
    fig_genetic_support_success,
    fig_property_axes,
    fig_variant_scoring,
    fig_epistasis,
    fig_coevolution_signal,
    fig_structure_model_families,
    fig_static_vs_ensemble,
    fig_design_inverts_prediction,
    fig_design_generate_filter_validate,
    fig_design_silico_to_wetlab_funnel,
    fig_cell_state_programming,
    fig_perturbation_response_model,
    fig_generalization_ladder,
    fig_pretrain_recipe,
    fig_two_lobes,
    fig_chapter_spine,
    fig_problem_map,
    fig_molecular_pipeline,
    fig_sequence_to_function,
    fig_allele_frequency_spectrum,
    fig_attention_context,
    fig_model_families,
    fig_pretrain_transfer,
    fig_sequence_structure_fitness,
    fig_regulatory_tracks,
    fig_assay_to_signal,
    fig_ld_tag_not_cause,
    fig_association_to_causation,
    fig_example_modality_map,
    fig_cover,
    fig_icon,
    fig_touch_icon,
)


def main() -> None:
    """Regenerate every figure and report where it went."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for make in FIGURES:
        path = make()
        assert (
            path.exists()
        ), f"Figure function '{make.__name__}' did not write its file."
        print(f"  wrote {path.relative_to(ROOT)}")
    print(f"Generated {len(FIGURES)} figures.")


if __name__ == "__main__":
    main()
