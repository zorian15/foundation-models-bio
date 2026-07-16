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
    body += node_box(
        24, 76, 150, 84, "unlabeled corpus", fill=PAPER, font_size=13, weight=600
    )
    body.append(
        f'<text x="99" y="128" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">proteins · DNA</text>'
    )
    body.append(
        f'<text x="99" y="143" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">· cells ·</text>'
    )
    body.append(
        f'<line x1="174" y1="118" x2="222" y2="118" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw)"/>'
    )
    body += node_box(
        224, 76, 156, 84, "self-supervised", fill=PAPER, font_size=13, weight=600
    )
    body.append(
        f'<text x="302" y="128" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">pretraining:</text>'
    )
    body.append(
        f'<text x="302" y="143" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">predict masked token</text>'
    )
    body.append(
        f'<line x1="380" y1="118" x2="428" y2="118" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arw)"/>'
    )
    body += node_box(
        430,
        76,
        186,
        84,
        "foundation model",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=13,
        weight=600,
    )
    body.append(
        f'<text x="523" y="135" text-anchor="middle" font-family="{SANS}" font-size="10" fill="{MUTED}">reusable representations</text>'
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
    body += node_box(
        24,
        60,
        258,
        104,
        "molecular / therapeutic",
        fill=PAPER,
        font_size=14,
        weight=600,
    )
    body.append(
        f'<text x="153" y="120" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">proteins · structure</text>'
    )
    body.append(
        f'<text x="153" y="138" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">binding · design</text>'
    )
    body += node_box(
        358, 60, 258, 104, "genomic / regulatory", fill=PAPER, font_size=14, weight=600
    )
    body.append(
        f'<text x="487" y="120" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">DNA · expression</text>'
    )
    body.append(
        f'<text x="487" y="138" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">variants · splicing</text>'
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
    w, h = 640, 210
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
        f'<text x="320" y="180" font-size="11" text-anchor="middle" fill="{MUTED}">what stays hard reframes the next problem</text>'
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
        pts = " ".join(f"{418 + k * 16},{ty + offs[k]}" for k in range(11))
        body.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.6"/>'
        )
        body.append(
            f'<text x="612" y="{ty + 4}" font-size="10" text-anchor="end" fill="{MUTED}">{name}</text>'
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
    w, h = 640, 300
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
    for r in range(3):
        for c in range(3 - r):
            body.append(
                f'<rect x="{x0 + c * 18 + r * 9}" y="{hy - 6 + r * 16}" width="16" height="14" fill="{shades[(r + c) % 3]}" stroke="{PAPER}" stroke-width="1"/>'
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
        176,
        48,
        "credible set: a few high-PIP SNPs",
        fill=ACCENT_SOFT,
        stroke=ACCENT,
        font_size=11,
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


FIGURES = (
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
