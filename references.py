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
    Reference(
        key="nelson2015",
        authors=(
            "Nelson, M. R.",
            "Tipney, H.",
            "Painter, J. L.",
            "Shen, J.",
            "Nicoletti, P.",
            "Shen, Y.",
            "Floratos, A.",
            "Sham, P. C.",
        ),
        truncated=True,
        year=2015,
        title="The support of human genetic evidence for approved drug indications",
        venue="Nature Genetics",
        arxiv="",
        url="https://doi.org/10.1038/ng.3314",
    ),
    Reference(
        key="king2019",
        authors=(
            "King, E. A.",
            "Davis, J. W.",
            "Degner, J. F.",
        ),
        truncated=False,
        year=2019,
        title="Are drug targets with genetic support twice as likely to be approved? Revised estimates of the impact of genetic support for drug mechanisms on the probability of drug approval",
        venue="PLOS Genetics",
        arxiv="",
        url="https://doi.org/10.1371/journal.pgen.1008489",
    ),
    Reference(
        key="minikel2024",
        authors=(
            "Minikel, E. V.",
            "Painter, J. L.",
            "Dong, C. C.",
            "Nelson, M. R.",
        ),
        truncated=False,
        year=2024,
        title="Refining the impact of genetic evidence on clinical success",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-024-07316-0",
    ),
    Reference(
        key="buniello2025",
        authors=(
            "Buniello, A.",
            "Suveges, D.",
            "Cruz-Castillo, C.",
            "Bernal Llinares, M.",
            "Cornu, H.",
            "Lopez, I.",
            "Tsukanov, K.",
            "Roldan-Romero, J. M.",
        ),
        truncated=True,
        year=2025,
        title="Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery",
        venue="Nucleic Acids Research",
        arxiv="",
        url="https://doi.org/10.1093/nar/gkae1128",
    ),
    Reference(
        key="replogle2022",
        authors=(
            "Replogle, J. M.",
            "Saunders, R. A.",
            "Pogson, A. N.",
            "Hussmann, J. A.",
            "Lenail, A.",
            "Guna, A.",
            "Mascibroda, L.",
            "Wagner, E. J.",
        ),
        truncated=True,
        year=2022,
        title="Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq",
        venue="Cell",
        arxiv="",
        url="https://doi.org/10.1016/j.cell.2022.05.013",
    ),
    Reference(
        key="origene2025",
        authors=(
            "Zhang, Z.",
            "Qiu, Z.",
            "Wu, Y.",
            "Li, S.",
            "Wang, D.",
            "Liu, Y.",
            "Zhou, Z.",
            "Hu, Y.",
        ),
        truncated=True,
        year=2025,
        title="OriGene: A Self-Evolving Virtual Disease Biologist Automating Therapeutic Target Discovery",
        venue="bioRxiv",
        arxiv="",
        url="https://doi.org/10.1101/2025.06.03.657658",
    ),
    Reference(
        key="rives2021",
        authors=(
            "Rives, A.",
            "Meier, J.",
            "Sercu, T.",
            "Goyal, S.",
            "Lin, Z.",
            "Liu, J.",
            "Guo, D.",
            "Ott, M.",
            "Zitnick, C. L.",
            "Ma, J.",
            "Fergus, R.",
        ),
        truncated=False,
        year=2021,
        title="Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences",
        venue="Proceedings of the National Academy of Sciences",
        arxiv="",
        url="https://doi.org/10.1073/pnas.2016239118",
    ),
    Reference(
        key="tsuboyama2023",
        authors=(
            "Tsuboyama, K.",
            "Dauparas, J.",
            "Chen, J.",
            "Laine, E.",
            "Mohseni Behbahani, Y.",
            "Weinstein, J. J.",
            "Mangan, N. M.",
            "Ovchinnikov, S.",
        ),
        truncated=True,
        year=2023,
        title="Mega-scale experimental analysis of protein folding stability in biology and design",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-023-06328-6",
    ),
    Reference(
        key="dieckhaus2024",
        authors=(
            "Dieckhaus, H.",
            "Brocidiacono, M.",
            "Randolph, N. Z.",
            "Kuhlman, B.",
        ),
        truncated=False,
        year=2024,
        title="Transfer learning to leverage larger datasets for improved prediction of protein stability changes",
        venue="PNAS",
        arxiv="",
        url="https://doi.org/10.1073/pnas.2314853121",
    ),
    Reference(
        key="huang2021",
        authors=(
            "Huang, K.",
            "Fu, T.",
            "Gao, W.",
            "Zhao, Y.",
            "Roohani, Y.",
            "Leskovec, J.",
            "Coley, C. W.",
            "Xiao, C.",
            "Sun, J.",
            "Zitnik, M.",
        ),
        truncated=False,
        year=2021,
        title="Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development",
        venue="NeurIPS Datasets and Benchmarks",
        arxiv="2102.09548",
        url="",
    ),
    Reference(
        key="swanson2024",
        authors=(
            "Swanson, K.",
            "Walther, P.",
            "Leitz, J.",
            "Mukherjee, S.",
            "Wu, J. C.",
            "Shivnaraine, R. V.",
            "Zou, J.",
        ),
        truncated=False,
        year=2024,
        title="ADMET-AI: a machine learning ADMET platform for evaluation of large-scale chemical libraries",
        venue="Bioinformatics",
        arxiv="",
        url="https://doi.org/10.1093/bioinformatics/btae416",
    ),
    Reference(
        key="berman2000",
        authors=(
            "Berman, H. M.",
            "Westbrook, J.",
            "Feng, Z.",
            "Gilliland, G.",
            "Bhat, T. N.",
            "Weissig, H.",
            "Shindyalov, I. N.",
            "Bourne, P. E.",
        ),
        truncated=False,
        year=2000,
        title="The Protein Data Bank",
        venue="Nucleic Acids Research",
        arxiv="",
        url="https://doi.org/10.1093/nar/28.1.235",
    ),
    Reference(
        key="krishna2024",
        authors=(
            "Krishna, R.",
            "Wang, J.",
            "Ahern, W.",
            "Sturmfels, P.",
            "Venkatesh, P.",
            "Kalvet, I.",
            "Lee, G. R.",
            "Baker, D.",
        ),
        truncated=True,
        year=2024,
        title="Generalized biomolecular modeling and design with RoseTTAFold All-Atom",
        venue="Science",
        arxiv="",
        url="https://doi.org/10.1126/science.adl2528",
    ),
    Reference(
        key="wohlwend2024",
        authors=(
            "Wohlwend, J.",
            "Corso, G.",
            "Passaro, S.",
            "Getz, N.",
            "Reveiz, M.",
            "Leidal, K.",
            "Swiderski, W.",
            "Atkinson, L.",
        ),
        truncated=True,
        year=2024,
        title="Boltz-1: Democratizing Biomolecular Interaction Modeling",
        venue="bioRxiv",
        arxiv="",
        url="https://doi.org/10.1101/2024.11.19.624167",
    ),
    Reference(
        key="jing2024",
        authors=(
            "Jing, B.",
            "Berger, B.",
            "Jaakkola, T.",
        ),
        truncated=False,
        year=2024,
        title="AlphaFold Meets Flow Matching for Generating Protein Ensembles",
        venue="ICML",
        arxiv="2402.04845",
        url="",
    ),
    Reference(
        key="dauparas2022",
        authors=(
            "Dauparas, J.",
            "Anishchenko, I.",
            "Bennett, N.",
            "Bai, H.",
            "Ragotte, R. J.",
            "Milles, L. F.",
            "Wicky, B. I. M.",
            "Courbet, A.",
        ),
        truncated=True,
        year=2022,
        title="Robust deep learning-based protein sequence design using ProteinMPNN",
        venue="Science",
        arxiv="",
        url="https://doi.org/10.1126/science.add2187",
    ),
    Reference(
        key="ingraham2023",
        authors=(
            "Ingraham, J. B.",
            "Baranov, M.",
            "Costello, Z.",
            "Barber, K. W.",
            "Wang, W.",
            "Ismail, A.",
            "Grigoryan, G.",
        ),
        truncated=True,
        year=2023,
        title="Illuminating protein space with a programmable generative model",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-023-06728-8",
    ),
    Reference(
        key="guan2023",
        authors=(
            "Guan, J.",
            "Qian, W. W.",
            "Peng, X.",
            "Su, Y.",
            "Peng, J.",
            "Ma, J.",
        ),
        truncated=False,
        year=2023,
        title="3D Equivariant Diffusion for Target-Aware Molecule Generation and Affinity Prediction",
        venue="ICLR",
        arxiv="2303.03543",
        url="",
    ),
    Reference(
        key="corso2022",
        authors=(
            "Corso, G.",
            "Stärk, H.",
            "Jing, B.",
            "Barzilay, R.",
            "Jaakkola, T.",
        ),
        truncated=False,
        year=2022,
        title="DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking",
        venue="ICLR 2023",
        arxiv="2210.01776",
        url="",
    ),
    Reference(
        key="pacesa2025",
        authors=(
            "Pacesa, M.",
            "Nickel, L.",
            "Schellhaas, C.",
            "Schmidt, J.",
            "Pyatova, E.",
            "Kissling, L.",
            "Barendse, P.",
            "Choudhury, J.",
        ),
        truncated=True,
        year=2025,
        title="One-shot design of functional protein binders with BindCraft",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-025-09429-6",
    ),
    Reference(
        key="zambaldi2024",
        authors=(
            "Zambaldi, V.",
            "La, D.",
            "Chu, A. E.",
            "Patani, H.",
            "Danson, A. E.",
            "Kwan, T. O. C.",
            "Frerix, T.",
            "Schneider, R. G.",
        ),
        truncated=True,
        year=2024,
        title="De novo design of high-affinity protein binders with AlphaProteo",
        venue="arXiv preprint",
        arxiv="2409.08022",
        url="",
    ),
    Reference(
        key="lauko2025",
        authors=(
            "Lauko, A.",
            "Pellock, S. J.",
            "Sumida, K. H.",
            "Anishchenko, I.",
            "Juergens, D.",
            "Ahern, W.",
            "Jeung, J.",
            "Shida, A. F.",
        ),
        truncated=True,
        year=2025,
        title="Computational design of serine hydrolases",
        venue="Science",
        arxiv="",
        url="https://doi.org/10.1126/science.adu2454",
    ),
    Reference(
        key="roohani2023",
        authors=(
            "Roohani, Y.",
            "Huang, K.",
            "Leskovec, J.",
        ),
        truncated=False,
        year=2024,
        title="Predicting transcriptional outcomes of novel multigene perturbations with GEARS",
        venue="Nature Biotechnology",
        arxiv="",
        url="https://doi.org/10.1038/s41587-023-01905-6",
    ),
    Reference(
        key="adduri2025",
        authors=(
            "Adduri, A. K.",
            "Gautam, D.",
            "Bevilacqua, B.",
            "Imran, A.",
            "Shah, R.",
            "Naghipourfar, M.",
            "Teyssier, N.",
            "Ilango, R.",
        ),
        truncated=True,
        year=2025,
        title="Predicting cellular responses to perturbation across diverse contexts with State",
        venue="bioRxiv",
        arxiv="",
        url="https://www.biorxiv.org/content/10.1101/2025.06.26.661135v1",
    ),
    Reference(
        key="ahlmanneltze2025",
        authors=(
            "Ahlmann-Eltze, C.",
            "Huber, W.",
            "Anders, S.",
        ),
        truncated=False,
        year=2025,
        title="Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines",
        venue="Nature Methods",
        arxiv="",
        url="https://doi.org/10.1038/s41592-025-02772-6",
    ),
    Reference(
        key="cui2024",
        authors=(
            "Cui, Haotian",
            "Wang, Chloe",
            "Maan, Hassaan",
            "Pang, Kuan",
            "Luo, Fengning",
            "Duan, Nan",
            "Wang, Bo",
        ),
        truncated=False,
        year=2024,
        title="scGPT: toward building a foundation model for single-cell multi-omics using generative AI",
        venue="Nature Methods",
        arxiv="",
        url="https://doi.org/10.1038/s41592-024-02201-0",
    ),
    Reference(
        key="theodoris2023",
        authors=(
            "Theodoris, C. V.",
            "Xiao, L.",
            "Chopra, A.",
            "Chaffin, M. D.",
            "Al Sayed, Z. A.",
            "Hill, M. C.",
            "Mantineo, H.",
            "Brydon, E. M.",
        ),
        truncated=True,
        year=2023,
        title="Transfer learning enables predictions in network biology",
        venue="Nature",
        arxiv="",
        url="https://doi.org/10.1038/s41586-023-06139-9",
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
