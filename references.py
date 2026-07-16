"""Single source of truth for the book's references.

Chapters cite a work with `[@key]` in their markdown; `build.py` resolves each
key against `REFERENCES`, renders an author-year citation linked to the entry,
and appends a per-chapter References section listing exactly the works that
chapter cites. A citation whose key is missing here fails the build loudly.

Every entry should be verified against the actual paper (arXiv listing, venue
page) before it lands — a wrong citation is worse than no citation. See
`PLANNING.md` for a researched but not-yet-verified seed list to draw from.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

KEY_PATTERN = re.compile(r"^[a-z][a-z0-9]*$")
ARXIV_ID_PATTERN = re.compile(r"^\d{4}\.\d{4,5}$")


@dataclass(frozen=True)
class Reference:
    """One cited work.

    `authors` holds one "Lastname, F. M." string per author, in the paper's
    order; a corporate author (e.g. "DeepMind") is a single comma-free string.
    `truncated` marks an author list that is deliberately cut short (papers with
    dozens or hundreds of authors) and renders as "et al.". Exactly one of
    `arxiv` (a bare id like "1706.03762") and `url` may be set; both empty means
    the entry renders with no link.
    """

    key: str
    authors: tuple[str, ...]
    truncated: bool
    year: int
    title: str
    venue: str
    arxiv: str
    url: str

    def __post_init__(self) -> None:
        assert KEY_PATTERN.match(self.key), f"Bad reference key: {self.key!r}."
        assert self.authors, f"Reference '{self.key}' has no authors."
        assert all(a.strip() for a in self.authors), f"Empty author in '{self.key}'."
        assert 1900 < self.year <= 2100, f"Implausible year in '{self.key}'."
        assert self.title and not self.title.endswith(
            "."
        ), f"Title of '{self.key}' must be non-empty and carry no trailing period."
        assert self.venue, f"Reference '{self.key}' has no venue."
        assert not (
            self.arxiv and self.url
        ), f"Reference '{self.key}' sets both arxiv and url; pick one."
        if self.arxiv:
            assert ARXIV_ID_PATTERN.match(
                self.arxiv
            ), f"Bad arXiv id in '{self.key}': {self.arxiv!r}."

    def first_author_family(self) -> str:
        """Return the first author's family name (the part before the comma)."""
        first = self.authors[0]
        return first.split(",")[0].strip() if "," in first else first

    def in_text_label(self) -> str:
        """Return the author-year label, e.g. "Vaswani et al., 2017"."""
        family = self.first_author_family()
        if self.truncated or len(self.authors) >= 3:
            return f"{family} et al., {self.year}"
        if len(self.authors) == 2:
            second = self.authors[1]
            second_family = second.split(",")[0].strip() if "," in second else second
            return f"{family} & {second_family}, {self.year}"
        return f"{family}, {self.year}"

    def link(self) -> str:
        """Return the entry's URL, or "" when it has none."""
        if self.arxiv:
            return f"https://arxiv.org/abs/{self.arxiv}"
        return self.url


# No references yet. Add verified entries as chapters cite them; a researched
# seed list (identifiers still to be verified against each paper) is in
# PLANNING.md.
_ENTRIES: tuple[Reference, ...] = (
    Reference(
        key="abramson2024",
        authors=(
            "Abramson, J.",
            "Adler, J.",
            "Dunger, J.",
            "Evans, R.",
            "Green, T.",
            "Pritzel, A.",
            "Ronneberger, O.",
            "Willmore, L.",
        ),
        truncated=True,
        year=2024,
        title="Accurate structure prediction of biomolecular interactions with AlphaFold 3",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-024-07487-w",
    ),
    Reference(
        key="avsec2021",
        authors=(
            "Avsec, Z.",
            "Agarwal, V.",
            "Visentin, D.",
            "Ledsam, J. R.",
            "Grabska-Barwinska, A.",
            "Taylor, K. R.",
            "Assael, Y.",
            "Jumper, J.",
        ),
        truncated=True,
        year=2021,
        title="Effective gene expression prediction from sequence by integrating long-range interactions",
        venue="Nature Methods",
        arxiv="",
        url="https://doi.org/10.1038/s41592-021-01252-x",
    ),
    Reference(
        key="avsec2026",
        authors=(
            "Avsec, Z.",
            "Latysheva, N.",
            "Cheng, J.",
            "Novati, G.",
            "Taylor, K. R.",
            "Ward, T.",
            "Bycroft, C.",
            "Nicolaisen, L.",
        ),
        truncated=True,
        year=2026,
        title="Advancing regulatory variant effect prediction with AlphaGenome",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-025-10014-0",
    ),
    Reference(
        key="boyle2017",
        authors=(
            "Boyle, E. A.",
            "Li, Y. I.",
            "Pritchard, J. K.",
        ),
        truncated=False,
        year=2017,
        title="An Expanded View of Complex Traits: From Polygenic to Omnigenic",
        venue="Cell",
        arxiv="",
        url="https://doi.org/10.1016/j.cell.2017.05.038",
    ),
    Reference(
        key="brixi2026",
        authors=(
            "Brixi, G.",
            "Durrant, M. G.",
            "Ku, J.",
            "Naghipourfar, M.",
            "Poli, M.",
            "Sun, G.",
            "Brockman, G.",
            "Chang, D.",
        ),
        truncated=True,
        year=2026,
        title="Genome modelling and design across all domains of life with Evo 2",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-026-10176-5",
    ),
    Reference(
        key="cheng2023",
        authors=(
            "Cheng, J.",
            "Novati, G.",
            "Pan, J.",
            "Bycroft, C.",
            "Žemgulytė, A.",
            "Applebaum, T.",
            "Pritzel, A.",
            "Wong, L. H.",
        ),
        truncated=True,
        year=2023,
        title="Accurate proteome-wide missense variant effect prediction with AlphaMissense",
        venue="Science",
        arxiv="",
        url="https://doi.org/10.1126/science.adg7492",
    ),
    Reference(
        key="giambartolomei2014",
        authors=(
            "Giambartolomei, C.",
            "Vukcevic, D.",
            "Schadt, E. E.",
            "Franke, L.",
            "Hingorani, A. D.",
            "Wallace, C.",
            "Plagnol, V.",
        ),
        truncated=False,
        year=2014,
        title="Bayesian test for colocalisation between pairs of genetic association studies using summary statistics",
        venue="PLoS Genetics",
        arxiv="",
        url="https://doi.org/10.1371/journal.pgen.1004383",
    ),
    Reference(
        key="hayes2025",
        authors=(
            "Hayes, T.",
            "Rao, R.",
            "Akin, H.",
            "Sofroniew, N. J.",
            "Oktay, D.",
            "Lin, Z.",
            "Verkuil, R.",
            "Tran, V. Q.",
        ),
        truncated=True,
        year=2025,
        title="Simulating 500 million years of evolution with a language model",
        venue="Science",
        arxiv="",
        url="https://www.science.org/doi/10.1126/science.ads0018",
    ),
    Reference(
        key="huang2023",
        authors=(
            "Huang, C.",
            "Shuai, R. W.",
            "Baokar, P.",
            "Chung, R.",
            "Rastogi, R.",
            "Kathail, P.",
            "Ioannidis, N. M.",
        ),
        truncated=False,
        year=2023,
        title="Personal transcriptome variation is poorly explained by current genomic deep learning models",
        venue="Nature Genetics",
        arxiv="",
        url="https://doi.org/10.1038/s41588-023-01574-w",
    ),
    Reference(
        key="jumper2021",
        authors=(
            "Jumper, J.",
            "Evans, R.",
            "Pritzel, A.",
            "Green, T.",
            "Figurnov, M.",
            "Ronneberger, O.",
            "Tunyasuvunakool, K.",
            "Bates, R.",
        ),
        truncated=True,
        year=2021,
        title="Highly accurate protein structure prediction with AlphaFold",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-021-03819-2",
    ),
    Reference(
        key="lin2023",
        authors=(
            "Lin, Z.",
            "Akin, H.",
            "Rao, R.",
            "Hie, B.",
            "Zhu, Z.",
            "Lu, W.",
            "Smetanin, N.",
            "Verkuil, R.",
        ),
        truncated=True,
        year=2023,
        title="Evolutionary-scale prediction of atomic-level protein structure with a language model",
        venue="Science",
        arxiv="",
        url="https://www.science.org/doi/10.1126/science.ade2574",
    ),
    Reference(
        key="linder2025",
        authors=(
            "Linder, J.",
            "Srivastava, D.",
            "Yuan, H.",
            "Agarwal, V.",
            "Kelley, D. R.",
        ),
        truncated=False,
        year=2025,
        title="Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation",
        venue="Nature Genetics",
        arxiv="",
        url="https://doi.org/10.1038/s41588-024-02053-6",
    ),
    Reference(
        key="meier2021",
        authors=(
            "Meier, J.",
            "Rao, R.",
            "Verkuil, R.",
            "Liu, J.",
            "Sercu, T.",
            "Rives, A.",
        ),
        truncated=False,
        year=2021,
        title="Language models enable zero-shot prediction of the effects of mutations on protein function",
        venue="NeurIPS",
        arxiv="",
        url="https://proceedings.neurips.cc/paper/2021/hash/f51338d736f95dd42427296047067694-Abstract.html",
    ),
    Reference(
        key="notin2023",
        authors=(
            "Notin, P.",
            "Kollasch, A. W.",
            "Ritter, D.",
            "van Niekerk, L.",
            "Paul, S.",
            "Spinner, H.",
            "Rollins, N.",
            "Shaw, A.",
        ),
        truncated=True,
        year=2023,
        title="ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction and Design",
        venue="NeurIPS Datasets and Benchmarks Track",
        arxiv="",
        url="https://papers.nips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract-Datasets_and_Benchmarks.html",
    ),
    Reference(
        key="sasse2023",
        authors=(
            "Sasse, A.",
            "Ng, B.",
            "Spiro, A. E.",
            "Tasaki, S.",
            "Bennett, D. A.",
            "Gaiteri, C.",
            "De Jager, P. L.",
            "Chikina, M.",
        ),
        truncated=True,
        year=2023,
        title="Benchmarking of deep neural networks for predicting personal gene expression from DNA sequence highlights shortcomings",
        venue="Nature Genetics",
        arxiv="",
        url="https://doi.org/10.1038/s41588-023-01524-6",
    ),
    Reference(
        key="vaswani2017",
        authors=(
            "Vaswani, A.",
            "Shazeer, N.",
            "Parmar, N.",
            "Uszkoreit, J.",
            "Jones, L.",
            "Gomez, A. N.",
            "Kaiser, L.",
            "Polosukhin, I.",
        ),
        truncated=False,
        year=2017,
        title="Attention Is All You Need",
        venue="NeurIPS",
        arxiv="1706.03762",
        url="",
    ),
    Reference(
        key="wang2020",
        authors=(
            "Wang, G.",
            "Sarkar, A.",
            "Carbonetto, P.",
            "Stephens, M.",
        ),
        truncated=False,
        year=2020,
        title="A simple new approach to variable selection in regression, with application to genetic fine mapping",
        venue="Journal of the Royal Statistical Society: Series B (Statistical Methodology)",
        arxiv="",
        url="https://doi.org/10.1111/rssb.12388",
    ),
    Reference(
        key="watson2023",
        authors=(
            "Watson, J. L.",
            "Juergens, D.",
            "Bennett, N. R.",
            "Trippe, B. L.",
            "Yim, J.",
            "Eisenach, H. E.",
            "Ahern, W.",
            "Borst, A. J.",
        ),
        truncated=True,
        year=2023,
        title="De novo design of protein structure and function with RFdiffusion",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-023-06415-8",
    ),
)


def _build_index(entries: tuple[Reference, ...]) -> dict[str, Reference]:
    """Index entries by key, failing loudly on duplicates."""
    index: dict[str, Reference] = {}
    for entry in entries:
        assert entry.key not in index, f"Duplicate reference key: {entry.key}."
        index[entry.key] = entry
    return index


REFERENCES: dict[str, Reference] = _build_index(_ENTRIES)
