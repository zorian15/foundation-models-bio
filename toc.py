"""Single source of truth for the book's structure.

`build.py` imports `BOOK` from this module and generates one HTML file per
entry, plus the landing page. To reorder, rename, or add a chapter, edit this
file and rerun the build. If a chapter has a matching `content/<slug>.md`, that
prose is rendered; otherwise a stub page is synthesized from the `outline`
declared here, so the whole book is always navigable even before it is written.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    """One page of the book.

    `slug` is the file stem (used for `content/<slug>.md` and `<slug>.html`).
    `label` is the display number shown in navigation and section numbering:
    a digit for chapters, a letter for appendices, or an empty string for
    unnumbered front matter. `outline` is a list of (section_title, note)
    pairs describing what the chapter should eventually cover; it is only used
    to synthesize the stub when no drafted markdown exists yet.
    """

    slug: str
    label: str
    title: str
    outline: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Part:
    """A titled group of chapters, rendered as a heading in the sidebar."""

    title: str
    chapters: tuple[Chapter, ...]


# Front matter sits outside any part and is unnumbered.
PREFACE = Chapter(
    slug="preface",
    label="",
    title="Preface",
    outline=(
        (
            "Who this book is for",
            "An ML practitioner who wants the load-bearing picture of how "
            "foundation models are used in biology, without a PhD in the wet lab.",
        ),
        (
            "How to read it",
            "Problem-first spine; two lobes bridged by integration; "
            "awareness-and-synthesis depth over exhaustive detail.",
        ),
    ),
)


BOOK: tuple[Part, ...] = (
    Part(
        title="I · Foundations",
        chapters=(
            Chapter(
                slug="introduction",
                label="1",
                title="The Synthesis Premise",
                outline=(
                    (
                        "Foundation models meet biology",
                        "Why the same recipe that built LLMs now trains on "
                        "proteins, genomes, and cells.",
                    ),
                    (
                        "Two lobes, one journey",
                        "The molecular/therapeutic lobe and the "
                        "genomic/regulatory lobe, joined by multi-modal integration.",
                    ),
                    (
                        "What this book is and is not",
                        "The problem -> models -> what is still hard spine; the "
                        "depth invariant; what we defer to the appendices.",
                    ),
                ),
            ),
            Chapter(
                slug="landscape",
                label="2",
                title="The Landscape of Biological Problems",
                outline=(
                    (
                        "A map before the models",
                        "The problems first, so the models have something to be "
                        "measured against.",
                    ),
                    (
                        "The molecular and therapeutic problems",
                        "Target discovery, property prediction, structure, design, "
                        "cell engineering.",
                    ),
                    (
                        "The genomic and regulatory problems",
                        "Sequence-to-function of gene regulation, and variant-to-"
                        "mechanism across the allele frequency spectrum.",
                    ),
                ),
            ),
            Chapter(
                slug="ml-onramp",
                label="3",
                title="Modern ML and Foundation Models, Quickly",
                outline=(
                    (
                        "Representations and transformers",
                        "The refresher: embeddings, attention, why pretraining "
                        "transfers. Deeper treatment lives in the LLM book.",
                    ),
                    (
                        "The model families you will meet",
                        "Encoders, autoregressive decoders, and diffusion models, "
                        "and what each is good for.",
                    ),
                    (
                        "Pretraining, fine-tuning, zero-shot",
                        "Self-supervision on unlabeled biological data, then "
                        "transfer to a labelled task.",
                    ),
                ),
            ),
            Chapter(
                slug="data-modalities",
                label="4",
                title="The Data: What Each Assay Measures",
                outline=(
                    (
                        "Sequence, structure, and fitness",
                        "Amino-acid and DNA sequence; structures in the PDB from "
                        "cryo-EM and X-ray; deep mutational scanning.",
                    ),
                    (
                        "Reading the regulatory genome",
                        "RNA-seq, ATAC/DNase, ChIP-seq, CAGE, and Hi-C, and what "
                        "each one actually measures.",
                    ),
                    (
                        "From assay to training signal",
                        "Which readouts become model inputs and which become "
                        "prediction targets; the modality-to-model thread.",
                    ),
                ),
            ),
            Chapter(
                slug="genetics-primer",
                label="5",
                title="Genetics for the ML Practitioner",
                outline=(
                    (
                        "The allele frequency spectrum",
                        "Common vs rare variants, and why effect size tends to "
                        "rise as frequency falls.",
                    ),
                    (
                        "GWAS, linkage, and heritability",
                        "Association testing, why a hit is usually a tag, and where "
                        "the missing heritability went.",
                    ),
                    (
                        "Association versus causation",
                        "Fine-mapping, colocalization, Mendelian randomization; "
                        "confounding and population stratification.",
                    ),
                ),
            ),
        ),
    ),
    Part(
        title="II · Molecular and therapeutic problems",
        chapters=(
            Chapter(
                slug="target-discovery",
                label="6",
                title="Target Discovery",
                outline=(
                    (
                        "The problem: which gene or protein to drug",
                        "From a disease to a tractable, causal target.",
                    ),
                    (
                        "Models that attempt it",
                        "Sequence and network embeddings, perturbation readouts, "
                        "and genetics-informed prioritization.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Causality, novelty beyond known biology, and validation "
                        "cost.",
                    ),
                ),
            ),
            Chapter(
                slug="property-prediction",
                label="7",
                title="Function and Property Prediction",
                outline=(
                    (
                        "The problem: from sequence to phenotype",
                        "Variant effects, stability, binding, expression, and "
                        "activity.",
                    ),
                    (
                        "Models that attempt it",
                        "Protein language models used zero-shot and fine-tuned; "
                        "supervised property heads; benchmarks like ProteinGym.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Generalization off the training distribution; epistasis "
                        "and higher-order effects.",
                    ),
                ),
            ),
            Chapter(
                slug="protein-structure",
                label="8",
                title="Protein Structure Determination",
                outline=(
                    (
                        "The problem: from sequence to 3D",
                        "Why structure matters and what experiments cost.",
                    ),
                    (
                        "Models that attempt it",
                        "AlphaFold2/3, ESMFold, RoseTTAFold, and the open "
                        "all-atom co-folding models.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Single structures vs ensembles and dynamics; disordered "
                        "regions; complexes and conformational change.",
                    ),
                ),
            ),
            Chapter(
                slug="protein-design",
                label="9",
                title="Protein and Binder Design",
                outline=(
                    (
                        "The problem: designing new molecules",
                        "De novo backbones, binders, and enzymes to specification.",
                    ),
                    (
                        "Models that attempt it",
                        "Diffusion over structure (RFdiffusion, Chroma), inverse "
                        "folding (ProteinMPNN), and small-molecule generation.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "In-silico success rates vs wet-lab hit rates; function "
                        "beyond binding.",
                    ),
                ),
            ),
            Chapter(
                slug="cell-engineering",
                label="10",
                title="Cell Engineering",
                outline=(
                    (
                        "The problem: programming cells",
                        "Perturbations, circuits, and cell states for therapy.",
                    ),
                    (
                        "Models that attempt it",
                        "Perturbation-response models and single-cell readouts "
                        "linking intervention to phenotype.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Predicting unseen perturbations; combinatorial effects; "
                        "the gap from a dish to a patient.",
                    ),
                ),
            ),
        ),
    ),
    Part(
        title="III · Genomic and regulatory problems",
        chapters=(
            Chapter(
                slug="sequence-to-function",
                label="11",
                title="From Sequence to Regulatory Function",
                outline=(
                    (
                        "The problem: predicting function from DNA",
                        "What regulatory activity a stretch of genome will have.",
                    ),
                    (
                        "Models that attempt it",
                        "The Enformer and Borzoi line predicting expression, "
                        "accessibility, and 3D contacts; DNA language models.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Cross-gene accuracy vs poor personal, inter-individual "
                        "variation; long-range regulation.",
                    ),
                ),
            ),
            Chapter(
                slug="variant-to-mechanism",
                label="12",
                title="From Variant to Mechanism",
                outline=(
                    (
                        "The problem: from association to cause",
                        "Turning a genetic signal into a mechanism, across the "
                        "allele frequency spectrum.",
                    ),
                    (
                        "Models that attempt it",
                        "In-silico variant scoring feeding fine-mapping and "
                        "colocalization; missense and noncoding effect predictors.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Noncoding effects; cohort confounding; the running "
                        "example of aging-related disease.",
                    ),
                ),
            ),
        ),
    ),
    Part(
        title="IV · Integration",
        chapters=(
            Chapter(
                slug="multimodal-integration",
                label="13",
                title="Multi-Modal Integration",
                outline=(
                    (
                        "Why one modality is never enough",
                        "The frontier thesis: models that span sequence, "
                        "structure, expression, and chemistry.",
                    ),
                    (
                        "How models fuse modalities",
                        "Joint architectures (AlphaFold3), unified sequence "
                        "streams (Evo 2), and perturbation models.",
                    ),
                    (
                        "What they do well and what is still hard",
                        "Aligning modalities with different noise and scale; "
                        "missing-modality inference.",
                    ),
                ),
            ),
        ),
    ),
    Part(
        title="V · Doing it for real",
        chapters=(
            Chapter(
                slug="data-realities",
                label="14",
                title="The Hard Realities of Biological Data",
                outline=(
                    (
                        "Sparsity, imbalance, and noise",
                        "Few labels, rare positives, and measurement error as the "
                        "default condition.",
                    ),
                    (
                        "Batch effects and experimental bias",
                        "Why the confounder is often the assay, the lab, or the "
                        "cohort ancestry.",
                    ),
                    (
                        "Heterogeneity of effects",
                        "When one average hides many mechanisms.",
                    ),
                ),
            ),
            Chapter(
                slug="evaluation",
                label="15",
                title="Evaluating Models in Biology",
                outline=(
                    (
                        "What a good benchmark measures",
                        "Choosing the metric and the split that match the "
                        "biological question.",
                    ),
                    (
                        "Leakage, calibration, and statistics",
                        "Homology leakage, calibrated uncertainty, and the "
                        "statistical tests a collaborator will expect.",
                    ),
                    (
                        "From leaderboard to your assay",
                        "Why public performance rarely transfers to your problem.",
                    ),
                ),
            ),
            Chapter(
                slug="lab-loop",
                label="16",
                title="Closing the Loop with the Lab",
                outline=(
                    (
                        "The design-build-test-learn cycle",
                        "The model proposes, the lab tests, the results feed back.",
                    ),
                    (
                        "Active learning and iteration",
                        "Choosing the next experiment when experiments are the "
                        "expensive resource.",
                    ),
                    (
                        "Delivering into a pipeline",
                        "Working with wet-lab partners; predictions that a lab "
                        "can actually act on.",
                    ),
                ),
            ),
        ),
    ),
    Part(
        title="VI · Outlook",
        chapters=(
            Chapter(
                slug="outlook",
                label="17",
                title="Outlook: Open Frontiers",
                outline=(
                    (
                        "Where the field is heading",
                        "Unified biological foundation models, virtual cells, and "
                        "in-silico experiments. Flagged as speculative.",
                    ),
                    (
                        "What is science fiction and what is imminent",
                        "Separating the plausible near term from the aspirational.",
                    ),
                ),
            ),
        ),
    ),
)


APPENDICES: tuple[Chapter, ...] = (
    Chapter(
        slug="single-cell",
        label="A",
        title="Single-Cell Foundation Models",
        outline=(
            (
                "What single-cell data measures",
                "scRNA-seq expression matrices and the cell-by-gene view.",
            ),
            (
                "The models",
                "Geneformer, scGPT, scFoundation, and where they help.",
            ),
        ),
    ),
    Chapter(
        slug="spatial-omics",
        label="B",
        title="Spatial Omics",
        outline=(
            (
                "What spatial data adds",
                "Keeping location when measuring expression across a tissue.",
            ),
            (
                "The models",
                "Integrating spatial context with sequence and expression.",
            ),
        ),
    ),
    Chapter(
        slug="cell-imaging",
        label="C",
        title="Cell Imaging and Morphology",
        outline=(
            (
                "What imaging measures",
                "Cell Painting and high-content morphology profiles.",
            ),
            (
                "The models",
                "Self-supervised image encoders on perturbation screens.",
            ),
        ),
    ),
    Chapter(
        slug="glossary",
        label="D",
        title="Glossary",
        outline=(),
    ),
)


def all_pages() -> tuple[Chapter, ...]:
    """Return every page in reading order: preface, chapters, then appendices."""
    pages: list[Chapter] = [PREFACE]
    for part in BOOK:
        pages.extend(part.chapters)
    pages.extend(APPENDICES)
    slugs = [page.slug for page in pages]
    assert len(slugs) == len(
        set(slugs)
    ), "Duplicate slug detected in the table of contents."
    return tuple(pages)
