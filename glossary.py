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
        "Foundation model",
        "A model pretrained once on a broad corpus with a self-supervised objective, then adapted to many downstream tasks rather than trained from scratch for each one.",
    ),
    Term(
        "Self-supervised learning",
        "Training where the label comes from the data itself (for example, mask an amino acid and predict it), so no human annotation is needed.",
    ),
    Term(
        "Pretraining",
        "The initial, task-agnostic training phase on a large corpus that produces general representations; later adapted or fine-tuned to specific tasks.",
    ),
    Term(
        "Representation (embedding)",
        "The internal vector a model produces for an input; because it is shaped by the whole corpus, it can transfer to tasks the model never trained on.",
    ),
    Term(
        "Transfer learning",
        "Reusing knowledge captured during pretraining to solve a new task, instead of learning that task from zero.",
    ),
    Term(
        "Modality",
        "A distinct type of biological data or measurement, such as protein sequence, DNA sequence, 3D structure, or single-cell expression.",
    ),
    Term(
        "Protein language model",
        "A foundation model whose corpus is protein sequences, trained to predict masked or next residues, from which structure and function information emerges.",
    ),
    Term(
        "Sequence-to-function model",
        "A model that reads a long DNA window and predicts functional genomic readouts such as gene expression, chromatin accessibility, or splicing.",
    ),
    Term(
        "Central dogma",
        "The flow of biological information from DNA to RNA to protein, which is what links the genomic and molecular halves of the field.",
    ),
    Term(
        "Multimodal integration",
        "Building models that reason jointly across modalities (DNA, RNA, protein, cell state) rather than one modality in isolation.",
    ),
    Term(
        "Cis-regulatory variant",
        "A DNA change near a gene that alters how much of that gene is expressed, rather than changing the protein's amino-acid sequence.",
    ),
    Term(
        "Target (drug target)",
        "The protein or gene a therapy is designed to act on. Choosing one is a causal question: does perturbing it change the disease, or is it merely correlated with the disease.",
    ),
    Term(
        "Property / function prediction",
        "Predicting a measurable quantity about a given molecule, such as binding affinity, stability, or safety, typically from a learned sequence embedding.",
    ),
    Term(
        "ADMET",
        "Absorption, distribution, metabolism, excretion, toxicity: the cluster of pharmacological properties that decide whether a drug candidate behaves safely in the body.",
    ),
    Term(
        "Inverse design",
        "The design direction of a problem: instead of predicting a property from a molecule, you specify the desired function or shape and generate a novel molecule that realizes it.",
    ),
    Term(
        "de novo protein design",
        "Creating protein sequences and structures from scratch to meet a specification (for example a binder to a chosen target), rather than modifying a natural protein.",
    ),
    Term(
        "Regulatory track",
        "A signal measured along the genome by an assay, such as RNA expression, chromatin accessibility, or protein-DNA binding, that a sequence-to-function model learns to predict.",
    ),
    Term(
        "Sequence-to-function",
        "The problem of predicting the regulatory activity produced by a stretch of DNA, reading a long sequence window and outputting genomic tracks.",
    ),
    Term(
        "Allele frequency spectrum",
        "The full range of how common a genetic variant is, from private to a single family up to carried by most of the population; effect size tends to shrink as frequency rises.",
    ),
    Term(
        "GWAS (genome-wide association study)",
        "A study that scans the genome for positions where a variant is statistically associated with a trait across many individuals.",
    ),
    Term(
        "Linkage disequilibrium (LD)",
        "The tendency of nearby variants to be inherited together, so an associated position usually only tags the true causal variant rather than being it.",
    ),
    Term(
        "Fine-mapping",
        "Statistical methods that narrow an associated LD region down toward the specific variant most likely to be causal.",
    ),
    Term(
        "Polygenicity",
        "The property of a trait being influenced by very many variants each of tiny effect, so there is no single causal gene to find.",
    ),
    Term(
        "Token",
        "One discrete unit of model input: an amino acid or nucleotide, or a learned multi-character chunk such as a k-mer or byte-pair merge.",
    ),
    Term(
        "Embedding",
        "The learned vector a token is mapped to; the geometry of embedding space places biochemically or evolutionarily similar tokens near each other.",
    ),
    Term(
        "Attention",
        "The transformer operation that lets each position read a weighted blend of every other position, making a token's representation depend on its context.",
    ),
    Term(
        "Transformer",
        "A neural architecture built from stacked attention layers; the backbone of nearly every biological foundation model.",
    ),
    Term(
        "Encoder (masked language model)",
        "A model that sees the whole sequence and predicts hidden tokens from both sides, producing context-aware representations rather than generating new sequence (e.g. ESM-2).",
    ),
    Term(
        "Autoregressive decoder",
        "A model that factors a sequence left to right, predicting each token from the previous ones; a natural generator that also yields a whole-sequence likelihood (e.g. Evo 2, ProGen2).",
    ),
    Term(
        "Diffusion model",
        "A generator trained to reverse a gradual noising process, denoising from noise into a valid object; in biology usually 3D coordinates of a structure or molecule (e.g. RFdiffusion, AlphaFold3's structure head).",
    ),
    Term(
        "Self-supervised pretraining",
        "Training on a task whose labels come free from the data itself, such as predicting a masked or next token, requiring no experimental annotation.",
    ),
    Term(
        "Fine-tuning",
        "Continuing to train a pretrained model, usually with a small added task head, on a labeled downstream dataset.",
    ),
    Term(
        "Zero-shot prediction",
        "Using a pretrained model on a task directly, with no task-specific training, for example by reading effects off its likelihoods.",
    ),
    Term(
        "Log-likelihood ratio (variant scoring)",
        "The quantity log P(mutant) minus log P(wild-type) at a site; a large negative value flags a mutation the model finds evolutionarily surprising, correlating with functional damage.",
    ),
    Term(
        "UniProt / UniRef",
        "The reference database of known protein sequences (hundreds of millions of entries); UniRef is its clustered, redundancy-reduced version, the usual pretraining corpus for protein language models.",
    ),
    Term(
        "Reference genome",
        "A single agreed-upon consensus DNA sequence for a species (e.g. the human build GRCh38) against which any individual's genome is described as a set of differences.",
    ),
    Term(
        "Protein Data Bank (PDB)",
        "The public archive of experimentally determined 3D biomolecular structures, roughly 220,000 entries, and the training/evaluation set for structure prediction.",
    ),
    Term(
        "X-ray crystallography",
        "A method for solving a molecule's 3D structure by crystallizing it and inferring atom positions from how it diffracts X-rays.",
    ),
    Term(
        "Cryo-electron microscopy (cryo-EM)",
        "A method for solving structures by imaging flash-frozen molecules with an electron beam, well suited to large complexes that resist crystallization.",
    ),
    Term(
        "Deep mutational scanning (DMS)",
        "An assay that measures the functional effect of many mutations at once by selecting a mutant library under a pressure and sequencing survivors, yielding a per-variant fitness map.",
    ),
    Term(
        "Fitness map",
        "An effect score for each variant of a protein (ideally every single-amino-acid substitution), the ground truth against which variant-effect predictors are scored.",
    ),
    Term(
        "ProteinGym",
        "A standardized benchmark aggregating over 2.5 million DMS variant measurements across hundreds of assays for evaluating protein fitness and variant-effect models.",
    ),
    Term(
        "RNA-seq",
        "An assay measuring transcript abundance, the number of RNA copies of each gene in a sample, used as the standard proxy for gene expression level.",
    ),
    Term(
        "scRNA-seq",
        "Single-cell RNA-seq: transcript abundance measured per individual cell rather than averaged over a bulk tissue.",
    ),
    Term(
        "ATAC-seq / DNase-seq",
        "Assays measuring chromatin accessibility, i.e. which stretches of DNA are physically open and reachable by regulatory proteins.",
    ),
    Term(
        "Chromatin accessibility",
        "How open versus tightly packaged a region of DNA is; open regions are where regulatory proteins can dock, marking candidate regulatory elements.",
    ),
    Term(
        "ChIP-seq",
        "An assay that maps where a specific protein binds DNA (a transcription factor site or a histone modification) by pulling down the protein with its bound DNA and sequencing it.",
    ),
    Term(
        "CAGE",
        "An assay measuring transcription start site activity, capturing the exact base where transcription begins and how much starts there.",
    ),
    Term(
        "Transcription start site (TSS)",
        "The genomic base at which transcription of a gene begins; its location and activity are read out by CAGE.",
    ),
    Term(
        "Hi-C",
        "An assay measuring 3D genome contacts, i.e. which distant stretches of DNA physically touch when the chromosome folds inside the nucleus.",
    ),
    Term(
        "Coverage track",
        "A signal value at (almost) every genomic position, one track per assay per cell type, the common output form of regulatory-genome assays and the prediction target for sequence-to-function models.",
    ),
    Term(
        "MPRA (massively parallel reporter assay)",
        "An assay that measures the enhancer activity of thousands of short synthetic DNA sequences at once by wiring each to a readout gene, giving a designed causal test.",
    ),
    Term(
        "ENCODE / FANTOM5 / GTEx / 4D Nucleome",
        "Large public consortia that generated regulatory tracks (ENCODE, FANTOM5), tissue-level RNA-seq (GTEx), and 3D-contact maps (4D Nucleome) at scale.",
    ),
    Term(
        "Allele",
        "One of the alternative versions of the DNA sequence at a given genomic position; a SNP has two, such as an A allele and a G allele.",
    ),
    Term(
        "Single-nucleotide polymorphism (SNP)",
        "A single-letter position in the genome where individuals differ; the most common type of variant used in association studies.",
    ),
    Term(
        "Allele frequency",
        "The fraction of chromosomes in a population carrying a particular allele. The minor allele frequency (MAF) is that of the rarer allele.",
    ),
    Term(
        "Purifying selection",
        "Natural selection removing deleterious alleles from a population, which keeps strongly harmful (large-effect) variants rare rather than common.",
    ),
    Term(
        "Effect size",
        "How much carrying an allele shifts a trait; for common variants it is typically small, for rare variants it can be large.",
    ),
    Term(
        "Genome-wide significance",
        "The stringent p-value threshold (about 5e-8) that corrects for the roughly one million independent common-variant tests in a GWAS.",
    ),
    Term(
        "Haplotype block",
        "A run of variants inherited together and highly correlated, so that one causal variant makes all of them appear associated.",
    ),
    Term(
        "Lead SNP / tag",
        "The variant with the smallest p-value in a GWAS peak; usually just the best-correlated marker (tag) for the causal signal, not the cause itself.",
    ),
    Term(
        "Heritability",
        "The fraction of a trait's variation across individuals attributable to genetic differences, estimated classically from twins and families.",
    ),
    Term(
        "SNP-heritability",
        "The portion of heritability captured by common SNPs jointly, estimated from genome-wide data rather than from significant hits alone.",
    ),
    Term(
        "Missing heritability",
        "The historical gap between family-based heritability and the small fraction explained by genome-wide-significant hits, largely resolved as signal hiding in many sub-threshold variants.",
    ),
    Term(
        "Posterior inclusion probability (PIP)",
        "In fine-mapping, the estimated probability that a specific variant is causal for the signal.",
    ),
    Term(
        "Credible set",
        "A small group of variants that together are highly likely to contain the causal one, output by fine-mapping methods.",
    ),
    Term(
        "QTL / eQTL",
        "A quantitative trait locus is a variant that changes a molecular readout; an expression QTL (eQTL) changes a gene's expression level.",
    ),
    Term(
        "Colocalization",
        "A statistical test of whether a GWAS signal and a molecular QTL at the same locus are driven by the same causal variant (e.g., coloc).",
    ),
    Term(
        "Mendelian randomization (MR)",
        "Using a genetic variant as an instrumental variable, exploiting random inheritance, to test whether an exposure causes an outcome rather than merely correlating with it.",
    ),
    Term(
        "Horizontal pleiotropy",
        "When a genetic instrument affects the outcome through pathways other than the intended exposure, biasing a Mendelian randomization estimate.",
    ),
    Term(
        "Population stratification",
        "Confounding by ancestry, where allele frequencies and trait prevalence both differ across groups, faking associations; the genetic analogue of a batch effect.",
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
