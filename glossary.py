"""Single source of truth for the book's glossary.

This book crosses two jargon-dense fields, so **every term or abbreviation is
defined inline the first time it appears in the prose, and also added here**.
`build.py` renders the `glossary` appendix from `GLOSSARY`, alphabetically.

Keep each definition to one or two plain sentences aimed at an ML practitioner —
enough to unblock the reader, not a textbook entry. Cross-reference other terms
by name rather than restating them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    """One glossary entry.

    `term` is shown as written (keep the canonical casing, e.g. "RNA-seq");
    sorting is case-insensitive. `definition` is one or two plain sentences.
    """

    term: str
    definition: str

    def __post_init__(self) -> None:
        assert self.term.strip(), "Glossary term is empty."
        assert self.definition.strip(), f"Term {self.term!r} has an empty definition."
        assert not self.term.startswith(" "), f"Term {self.term!r} has leading space."


# A small seed drawn from the modality/data research (see PLANNING.md). Grow this
# as chapters are drafted — the convention is: define on first use, add here.
_TERMS: tuple[Term, ...] = (
    Term(
        "allele frequency spectrum",
        "The distribution of genetic variants by how common they are in a "
        "population; rare variants tend to carry larger effects because "
        "selection removes strongly harmful common ones.",
    ),
    Term(
        "ATAC-seq",
        "An assay that measures chromatin accessibility — which stretches of "
        "DNA are open and therefore available for regulation.",
    ),
    Term(
        "CAGE",
        "Cap Analysis of Gene Expression: measures transcription start-site "
        "activity by capturing the capped 5' ends of transcripts.",
    ),
    Term(
        "ChIP-seq",
        "An assay that maps where a specific protein (a transcription factor or "
        "a histone modification) binds the genome.",
    ),
    Term(
        "DMS",
        "Deep mutational scanning: measures the functional effect of thousands "
        "of variants of one protein or element in parallel, yielding a fitness "
        "map used to benchmark variant-effect predictors.",
    ),
    Term(
        "GWAS",
        "Genome-wide association study: tests each common variant across the "
        "genome for statistical association with a trait, producing per-variant "
        "effect sizes and p-values.",
    ),
    Term(
        "Hi-C",
        "An assay that measures the three-dimensional contact frequency between "
        "genomic loci, revealing chromatin loops and domains.",
    ),
    Term(
        "linkage disequilibrium",
        "The correlation between nearby genetic variants inherited together; it "
        "is why a GWAS hit is usually a tag for, not the cause of, a signal.",
    ),
    Term(
        "PDB",
        "Protein Data Bank: the archive of experimentally determined 3D "
        "macromolecular structures that trains and evaluates structure models.",
    ),
    Term(
        "RNA-seq",
        "An assay that measures transcript abundance — how much each gene is "
        "expressed — by sequencing RNA in a sample.",
    ),
)


def _sorted(terms: tuple[Term, ...]) -> tuple[Term, ...]:
    """Return terms sorted case-insensitively, failing on duplicates."""
    seen: set[str] = set()
    for term in terms:
        key = term.term.lower()
        assert key not in seen, f"Duplicate glossary term: {term.term!r}."
        seen.add(key)
    return tuple(sorted(terms, key=lambda t: t.term.lower()))


GLOSSARY: tuple[Term, ...] = _sorted(_TERMS)
