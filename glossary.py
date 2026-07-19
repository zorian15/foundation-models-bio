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
        "ADMET",
        "Absorption, distribution, metabolism, excretion, toxicity: the cluster of pharmacological properties that decide whether a drug candidate behaves safely in the body.",
    ),
    Term(
        "Allele",
        "One of the alternative versions of the DNA sequence at a given genomic position; a SNP has two, such as an A allele and a G allele.",
    ),
    Term(
        "Allele frequency",
        "The fraction of chromosomes in a population carrying a particular allele. The minor allele frequency (MAF) is that of the rarer allele.",
    ),
    Term(
        "Allele frequency spectrum",
        "The full range of how common a genetic variant is, from private to a single family up to carried by most of the population; effect size tends to shrink as frequency rises.",
    ),
    Term(
        "ATAC-seq / DNase-seq",
        "Assays measuring chromatin accessibility, i.e. which stretches of DNA are physically open and reachable by regulatory proteins.",
    ),
    Term(
        "Attention",
        "The transformer operation that lets each position read a weighted blend of every other position, making a token's representation depend on its context.",
    ),
    Term(
        "Autoregressive decoder",
        "A model that factors a sequence left to right, predicting each token from the previous ones; a natural generator that also yields a whole-sequence likelihood (e.g. Evo 2, ProGen2).",
    ),
    Term(
        "CAGE",
        "An assay measuring transcription start site activity, capturing the exact base where transcription begins and how much starts there.",
    ),
    Term(
        "Central dogma",
        "The flow of biological information from DNA to RNA to protein, which is what links the genomic and molecular halves of the field.",
    ),
    Term(
        "ChIP-seq",
        "An assay that maps where a specific protein binds DNA (a transcription factor site or a histone modification) by pulling down the protein with its bound DNA and sequencing it.",
    ),
    Term(
        "Chromatin accessibility",
        "How open versus tightly packaged a region of DNA is; open regions are where regulatory proteins can dock, marking candidate regulatory elements.",
    ),
    Term(
        "Cis-regulatory variant",
        "A DNA change near a gene that alters how much of that gene is expressed, rather than changing the protein's amino-acid sequence.",
    ),
    Term(
        "Colocalization",
        "A statistical test of whether a GWAS signal and a molecular QTL at the same locus are driven by the same causal variant (e.g., coloc).",
    ),
    Term(
        "Coverage track",
        "A signal value at (almost) every genomic position, one track per assay per cell type, the common output form of regulatory-genome assays and the prediction target for sequence-to-function models.",
    ),
    Term(
        "Credible set",
        "A small group of variants that together are highly likely to contain the causal one, output by fine-mapping methods.",
    ),
    Term(
        "Cryo-electron microscopy (cryo-EM)",
        "A method for solving structures by imaging flash-frozen molecules with an electron beam, well suited to large complexes that resist crystallization.",
    ),
    Term(
        "de novo protein design",
        "Creating protein sequences and structures from scratch to meet a specification (for example a binder to a chosen target), rather than modifying a natural protein.",
    ),
    Term(
        "Deep mutational scanning (DMS)",
        "An assay that measures the functional effect of many mutations at once by selecting a mutant library under a pressure and sequencing survivors, yielding a per-variant fitness map.",
    ),
    Term(
        "Diffusion model",
        "A generator trained to reverse a gradual noising process, denoising from noise into a valid object; in biology usually 3D coordinates of a structure or molecule (e.g. RFdiffusion, AlphaFold3's structure head).",
    ),
    Term(
        "Effect size",
        "How much carrying an allele shifts a trait; for common variants it is typically small, for rare variants it can be large.",
    ),
    Term(
        "Embedding",
        "The learned vector a token is mapped to; the geometry of embedding space places biochemically or evolutionarily similar tokens near each other.",
    ),
    Term(
        "ENCODE / FANTOM5 / GTEx / 4D Nucleome",
        "Large public consortia that generated regulatory tracks (ENCODE, FANTOM5), tissue-level RNA-seq (GTEx), and 3D-contact maps (4D Nucleome) at scale.",
    ),
    Term(
        "Encoder (masked language model)",
        "A model that sees the whole sequence and predicts hidden tokens from both sides, producing context-aware representations rather than generating new sequence (e.g. ESM-2).",
    ),
    Term(
        "Fine-mapping",
        "Statistical methods that narrow an associated LD region down toward the specific variant most likely to be causal.",
    ),
    Term(
        "Fine-tuning",
        "Continuing to train a pretrained model, usually with a small added task head, on a labeled downstream dataset.",
    ),
    Term(
        "Fitness map",
        "An effect score for each variant of a protein (ideally every single-amino-acid substitution), the ground truth against which variant-effect predictors are scored.",
    ),
    Term(
        "Foundation model",
        "A model pretrained once on a broad corpus with a self-supervised objective, then adapted to many downstream tasks rather than trained from scratch for each one.",
    ),
    Term(
        "Genome-wide significance",
        "The stringent p-value threshold (about 5e-8) that corrects for the roughly one million independent common-variant tests in a GWAS.",
    ),
    Term(
        "GWAS (genome-wide association study)",
        "A study that scans the genome for positions where a variant is statistically associated with a trait across many individuals.",
    ),
    Term(
        "Haplotype block",
        "A run of variants inherited together and highly correlated, so that one causal variant makes all of them appear associated.",
    ),
    Term(
        "Heritability",
        "The fraction of a trait's variation across individuals attributable to genetic differences, estimated classically from twins and families.",
    ),
    Term(
        "Hi-C",
        "An assay measuring 3D genome contacts, i.e. which distant stretches of DNA physically touch when the chromosome folds inside the nucleus.",
    ),
    Term(
        "Horizontal pleiotropy",
        "When a genetic instrument affects the outcome through pathways other than the intended exposure, biasing a Mendelian randomization estimate.",
    ),
    Term(
        "Inverse design",
        "The design direction of a problem: instead of predicting a property from a molecule, you specify the desired function or shape and generate a novel molecule that realizes it.",
    ),
    Term(
        "Lead SNP / tag",
        "The variant with the smallest p-value in a GWAS peak; usually just the best-correlated marker (tag) for the causal signal, not the cause itself.",
    ),
    Term(
        "Linkage disequilibrium (LD)",
        "The tendency of nearby variants to be inherited together, so an associated position usually only tags the true causal variant rather than being it.",
    ),
    Term(
        "Log-likelihood ratio (variant scoring)",
        "The quantity log P(mutant) minus log P(wild-type) at a site; a large negative value flags a mutation the model finds evolutionarily surprising, correlating with functional damage.",
    ),
    Term(
        "Mendelian randomization (MR)",
        "Using a genetic variant as an instrumental variable, exploiting random inheritance, to test whether an exposure causes an outcome rather than merely correlating with it.",
    ),
    Term(
        "Missing heritability",
        "The historical gap between family-based heritability and the small fraction explained by genome-wide-significant hits, largely resolved as signal hiding in many sub-threshold variants.",
    ),
    Term(
        "Modality",
        "A distinct type of biological data or measurement, such as protein sequence, DNA sequence, 3D structure, or single-cell expression.",
    ),
    Term(
        "MPRA (massively parallel reporter assay)",
        "An assay that measures the enhancer activity of thousands of short synthetic DNA sequences at once by wiring each to a readout gene, giving a designed causal test.",
    ),
    Term(
        "Multimodal integration",
        "Building models that reason jointly across modalities (DNA, RNA, protein, cell state) rather than one modality in isolation.",
    ),
    Term(
        "Polygenicity",
        "The property of a trait being influenced by very many variants each of tiny effect, so there is no single causal gene to find.",
    ),
    Term(
        "Population stratification",
        "Confounding by ancestry, where allele frequencies and trait prevalence both differ across groups, faking associations; the genetic analogue of a batch effect.",
    ),
    Term(
        "Posterior inclusion probability (PIP)",
        "In fine-mapping, the estimated probability that a specific variant is causal for the signal.",
    ),
    Term(
        "Pretraining",
        "The initial, task-agnostic training phase on a large corpus that produces general representations; later adapted or fine-tuned to specific tasks.",
    ),
    Term(
        "Property / function prediction",
        "Predicting a measurable quantity about a given molecule, such as binding affinity, stability, or safety, typically from a learned sequence embedding.",
    ),
    Term(
        "Protein Data Bank (PDB)",
        "The public archive of experimentally determined 3D biomolecular structures, roughly 220,000 entries, and the training/evaluation set for structure prediction.",
    ),
    Term(
        "Protein language model",
        "A foundation model whose corpus is protein sequences, trained to predict masked or next residues, from which structure and function information emerges.",
    ),
    Term(
        "ProteinGym",
        "A standardized benchmark aggregating over 2.5 million DMS variant measurements across hundreds of assays for evaluating protein fitness and variant-effect models.",
    ),
    Term(
        "Purifying selection",
        "Natural selection removing deleterious alleles from a population, which keeps strongly harmful (large-effect) variants rare rather than common.",
    ),
    Term(
        "QTL / eQTL",
        "A quantitative trait locus is a variant that changes a molecular readout; an expression QTL (eQTL) changes a gene's expression level.",
    ),
    Term(
        "Reference genome",
        "A single agreed-upon consensus DNA sequence for a species (e.g. the human build GRCh38) against which any individual's genome is described as a set of differences.",
    ),
    Term(
        "Regulatory track",
        "A signal measured along the genome by an assay, such as RNA expression, chromatin accessibility, or protein-DNA binding, that a sequence-to-function model learns to predict.",
    ),
    Term(
        "Representation (embedding)",
        "The internal vector a model produces for an input; because it is shaped by the whole corpus, it can transfer to tasks the model never trained on.",
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
        "Self-supervised learning",
        "Training where the label comes from the data itself (for example, mask an amino acid and predict it), so no human annotation is needed.",
    ),
    Term(
        "Self-supervised pretraining",
        "Training on a task whose labels come free from the data itself, such as predicting a masked or next token, requiring no experimental annotation.",
    ),
    Term(
        "Sequence-to-function",
        "The problem of predicting the regulatory activity produced by a stretch of DNA, reading a long sequence window and outputting genomic tracks.",
    ),
    Term(
        "Sequence-to-function model",
        "A model that reads a long DNA window and predicts functional genomic readouts such as gene expression, chromatin accessibility, or splicing.",
    ),
    Term(
        "Single-nucleotide polymorphism (SNP)",
        "A single-letter position in the genome where individuals differ; the most common type of variant used in association studies.",
    ),
    Term(
        "SNP-heritability",
        "The portion of heritability captured by common SNPs jointly, estimated from genome-wide data rather than from significant hits alone.",
    ),
    Term(
        "Target (drug target)",
        "The protein or gene a therapy is designed to act on. Choosing one is a causal question: does perturbing it change the disease, or is it merely correlated with the disease.",
    ),
    Term(
        "Token",
        "One discrete unit of model input: an amino acid or nucleotide, or a learned multi-character chunk such as a k-mer or byte-pair merge.",
    ),
    Term(
        "Transcription start site (TSS)",
        "The genomic base at which transcription of a gene begins; its location and activity are read out by CAGE.",
    ),
    Term(
        "Transfer learning",
        "Reusing knowledge captured during pretraining to solve a new task, instead of learning that task from zero.",
    ),
    Term(
        "Transformer",
        "A neural architecture built from stacked attention layers; the backbone of nearly every biological foundation model.",
    ),
    Term(
        "UniProt / UniRef",
        "The reference database of known protein sequences (hundreds of millions of entries); UniRef is its clustered, redundancy-reduced version, the usual pretraining corpus for protein language models.",
    ),
    Term(
        "X-ray crystallography",
        "A method for solving a molecule's 3D structure by crystallizing it and inferring atom positions from how it diffracts X-rays.",
    ),
    Term(
        "Zero-shot prediction",
        "Using a pretrained model on a task directly, with no task-specific training, for example by reading effects off its likelihoods.",
    ),
    Term(
        "Target discovery",
        "The process of choosing which gene or protein a drug should act on for a given disease, requiring the target to be both causal for the disease and druggable.",
    ),
    Term(
        "Druggability",
        "The capacity of a biological target, usually a protein, to be bound and modulated by a drug-like molecule with sufficient affinity and selectivity to have a therapeutic effect.",
    ),
    Term(
        "Druggable genome",
        "The subset of human protein-coding genes (roughly 3,000 to 4,500) whose products can plausibly be modulated by a drug; fewer than 700 are hit by an approved drug today.",
    ),
    Term(
        "Causal target",
        "A gene or protein whose perturbation actually changes the disease, as opposed to one merely correlated with or downstream of the disease.",
    ),
    Term(
        "Open Targets",
        "An open platform that aggregates genetic, genomic, and other evidence into a single target-disease association score, and includes the locus-to-gene (L2G) model for mapping GWAS loci to likely causal genes.",
    ),
    Term(
        "Locus-to-gene (L2G)",
        "A trained classifier that scores which gene a GWAS association acts through, since the associated variant is usually not located in the gene it regulates.",
    ),
    Term(
        "Perturb-seq",
        "A pooled CRISPR screen read out by single-cell RNA sequencing, so each cell's full transcriptome reveals the downstream program controlled by the perturbed gene.",
    ),
    Term(
        "Pleiotropy",
        "When one genetic variant affects multiple traits or pathways, which can violate the assumption in Mendelian randomization that an instrument affects the disease only through the intended target.",
    ),
    Term(
        "Undruggable target",
        "A protein for which no drug-like molecule is known to bind productively, often transcription factors or scaffolds; the label reflects both intrinsic difficulty and where industry has invested.",
    ),
    Term(
        "Property prediction",
        "Predicting a measurable quantity (stability, binding, activity, toxicity) for a molecule whose sequence or structure is already given, as a cheap stand-in for running the assay.",
    ),
    Term(
        "Variant effect (fitness)",
        "How much a mutation changes a protein's function relative to the wild type; the quantity deep mutational scanning measures and that zero-shot PLM scores approximate.",
    ),
    Term(
        "Zero-shot",
        "Using a model to score a task it was never trained on with labels; here, scoring variant fitness directly from a language model's sequence probabilities.",
    ),
    Term(
        "Folding stability (ΔΔG)",
        "The change in a protein's folding free energy caused by a mutation; positive values are destabilizing. Measured at scale by proteolysis assays and predicted by supervised models like ThermoMPNN.",
    ),
    Term(
        "Binding affinity (Kd)",
        "The dissociation constant quantifying how tightly two molecules bind; a smaller Kd means a tighter interaction.",
    ),
    Term(
        "Epistasis",
        "Non-additive interaction between mutations, where the combined effect differs from the sum of individual effects; sign epistasis is the case where two individually beneficial mutations combine to harm the protein.",
    ),
    Term(
        "Calibration",
        "Whether a model's numeric scores can be read as reliable probabilities or physical values across proteins, as opposed to only ranking candidates correctly within one protein.",
    ),
    Term(
        "Multiple sequence alignment (MSA)",
        "The stack of evolutionarily related sequences for a protein; alignment-based methods exploit its per-column conservation and remain competitive with single-sequence language models on variant effect.",
    ),
    Term(
        "Out-of-distribution generalization",
        "A model's accuracy on inputs unlike its training data; protein language models anchored to natural sequences degrade on de novo or heavily engineered proteins.",
    ),
    Term(
        "Protein folding problem",
        "The task of predicting a protein's 3D structure (the coordinates of its atoms) from its 1D amino-acid sequence.",
    ),
    Term(
        "Cryo-EM (cryo-electron microscopy)",
        "An experimental method that images flash-frozen molecules with an electron beam; handles large assemblies and membrane proteins without needing crystals.",
    ),
    Term(
        "Co-evolution",
        "The tendency of two residues that touch in the folded structure to mutate in a correlated way across evolution, so their alignment columns vary together; the signal that makes structure prediction possible.",
    ),
    Term(
        "Homolog",
        "A sequence related to a query protein by shared ancestry, from another species or a duplicated gene.",
    ),
    Term(
        "CASP",
        "Critical Assessment of Structure Prediction, the biennial blind competition where methods predict structures of sequences whose experimental answers are withheld.",
    ),
    Term(
        "pLDDT",
        "AlphaFold's per-residue confidence score; low values flag regions that are unreliable or intrinsically disordered.",
    ),
    Term(
        "Monomer",
        "A single protein chain, as opposed to a complex of several chains or of a protein bound to other molecules.",
    ),
    Term(
        "Complex / assembly",
        "A structure of multiple molecules bound together, such as protein with protein, DNA, RNA, a ligand, or ions.",
    ),
    Term(
        "Ligand",
        "A small molecule that binds a protein, such as a drug, cofactor, or metabolite.",
    ),
    Term(
        "Co-folding model",
        "A predictor that folds a protein together with its binding partners (ligand, nucleic acid, ion) into one joint structure rather than folding the protein alone.",
    ),
    Term(
        "Conformational ensemble",
        "The population of distinct shapes a molecule actually visits; function often depends on the distribution of states, not any single one.",
    ),
    Term(
        "Intrinsically disordered region (IDR)",
        "A stretch of a protein that has no fixed fold and stays flexible in the cell, yet is often functional.",
    ),
    Term(
        "de novo design",
        "Building a protein or small molecule from scratch to meet a specification, rather than editing a molecule nature already made.",
    ),
    Term(
        "inverse folding",
        "The task of choosing an amino-acid sequence that folds into a given backbone shape; the inverse of structure prediction.",
    ),
    Term(
        "backbone",
        "The chain of a protein's main-chain atoms defining its 3D shape, without the amino-acid side chains that specify identity.",
    ),
    Term(
        "binder",
        "A designed protein engineered to bind tightly to a chosen patch on a target molecule's surface.",
    ),
    Term(
        "RFdiffusion",
        "A diffusion model that generates protein backbones and can be conditioned to build binders or scaffold catalytic sites.",
    ),
    Term(
        "ProteinMPNN",
        "An inverse-folding model that reads 3D backbone coordinates and predicts a sequence that folds to them; a message-passing network, not a sequence language model.",
    ),
    Term(
        "self-consistency",
        "A filter that feeds a designed sequence to an independent structure predictor and keeps it only if the predicted fold matches the intended backbone (low RMSD, high confidence).",
    ),
    Term(
        "hallucination (design)",
        "Optimizing a sequence by backpropagating through a structure predictor toward a high-confidence target structure, as in BindCraft.",
    ),
    Term(
        "developability",
        "The practical qualities a designed protein needs to be usable: expressing in cells, staying soluble, tolerating storage, and not provoking an immune response.",
    ),
    Term(
        "expression",
        "Whether living cells can actually manufacture a designed protein at usable yield.",
    ),
    Term(
        "structure-based drug design",
        "Designing or scoring small molecules using the 3D structure of a target protein's binding pocket.",
    ),
    Term(
        "Cell state",
        "A cell's condition summarized as its transcriptome, the vector of which genes are expressed and how strongly, read out by single-cell RNA sequencing.",
    ),
    Term(
        "Perturbation",
        "A deliberate intervention on a cell, such as knocking out a gene, activating or repressing it with CRISPRa/CRISPRi, or applying a drug, cytokine, or gene circuit.",
    ),
    Term(
        "CRISPRa / CRISPRi",
        "CRISPR activation and CRISPR interference: using a guided, catalytically dead Cas protein to increase or decrease a gene's expression without cutting the DNA.",
    ),
    Term(
        "Perturbation-response model",
        "A model that maps a perturbation to the expression shift it causes, so it can score or rank perturbations that have not been experimentally run.",
    ),
    Term(
        "Virtual cell",
        "A model that aims to simulate a cell's response to arbitrary perturbations across contexts; Arc Institute's State is an early example.",
    ),
    Term(
        "Pseudobulk",
        "The mean expression profile across the cells sharing a condition, used as a per-perturbation summary that discards cell-to-cell variation.",
    ),
    Term(
        "Distribution shift",
        "The change in data distribution between training and deployment, e.g. from immortalized cell lines to primary or patient cells, which degrades a model's transfer.",
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
