Before you reach for a model, you need a map of the questions. Biology asks a lot of things, but the questions that foundation models answer fall into a small number of recurring shapes: *which molecule matters*, *what does this molecule do*, *what shape is it*, *build me one that does X*, and, on the genome side, *what does this stretch of DNA control* and *what does this mutation break*. A model is only ever an answer to one of these shapes. This chapter draws the map first — naming each problem and why it is genuinely hard — so that when the later chapters bring in the models, you have a fixed thing to measure them against instead of an accuracy number floating free of any decision.

## A map before the models

Every problem chapter in this book follows the same three-beat template: **the problem**, **the models**, **the gaps**. First we state what a working biologist actually wants and why it resists a clean solution. Then we bring in the current models and what they buy you. Then we are honest about where they still fail, because "what stays hard" is usually the thing that reframes the next problem. Keeping these three beats separate is the whole discipline of the book. A benchmark score reported without the first and third beats is close to meaningless: 0.9 correlation is triumphant on an easy split and a failure on a hard one, and a model can top a leaderboard while answering a proxy question that no one needed answered.

<figure>
<img src="assets/figures/problem-map.svg" alt="Three boxes in a row, problem then models then gaps, with a dashed arrow looping from gaps back to problem.">
<figcaption>Read every later chapter in three beats; the gaps are not an afterthought but the seed of the next problem.</figcaption>
</figure>

The problems split into two families that this book treats as two lobes of one story. The **molecular and therapeutic** lobe lives in the world of proteins and small molecules: it is where drug discovery happens, and where structure prediction and protein design have produced the field's loudest wins. The **genomic and regulatory** lobe lives in the world of DNA and gene expression: it asks what non-coding sequence does and what a person's genetic variants mean. The two lobes use different data, different models, and different yardsticks, and they finally meet in multimodal integration (Chapter 13). Hold them apart for now; conflating "predict a protein's fold" with "predict what a promoter mutation does" is the single most common way newcomers misjudge what a model can do.

!!! intuition "Intuition"
    A foundation model does not answer "biology"; it answers exactly one problem shape. Your first job on any task is to find which shape it is and how the field grades it.

!!! collaborator "Collaborator"
    *A statistician asks: if you have a benchmark, why do you need a "map"? Just report the number.* Because the number scores a proxy, and the map tells you whether the proxy matches the decision. A variant-effect model can hit high AUROC by separating well-studied pathogenic mutations from random ones, yet be useless for the actual clinical question of ranking novel variants of unknown significance. The map is what keeps you from optimizing a metric that has quietly stopped meaning what you need.

## The molecular and therapeutic problems

**Target discovery (Chapter 6)** asks which protein or gene to aim a drug at in the first place. This is upstream of everything else and the least model-shaped of the five: it is fundamentally a *causal* question — does perturbing this target change the disease, or is the target merely correlated with it — and correlation is cheap while causal evidence is expensive. Models here rank and prioritize rather than decide, and the hardest part is that the ground truth (a successful clinical trial) arrives years too late to train on.

**Property and function prediction (Chapter 7)** takes a given molecule and predicts a number about it: how tightly a protein binds, how stable it is, whether a drug candidate is absorbed and cleared safely (the cluster of properties called **ADMET** — absorption, distribution, metabolism, excretion, toxicity). Protein language models such as ESM-2 turn a sequence into an embedding that a small head can regress against these labels. The difficulty is label economics: assays are noisy and scarce, and a model trained on one chemical series routinely collapses on the next, so distribution shift, not raw accuracy, is the real adversary.

**Protein structure (Chapter 8)** maps a sequence to its 3D shape, and it is the problem where deep learning most convincingly "won." AlphaFold3 predicts the joint structure of proteins together with nucleic acids, ligands, and ions using a diffusion-based generator [@abramson2024], and ESMFold drops the multiple-sequence-alignment step for speed. But "solved" is narrower than the headlines: a confident single-chain structure is not a complex, not a conformational ensemble, and not a disordered region, and a static picture is still not a function.

**Protein and binder design (Chapter 9)** runs the arrow backwards. Instead of sequence-to-structure, it is the **inverse design** problem: specify the function or shape you want and get a novel sequence that realizes it. RFdiffusion generates protein backbones by diffusion and has produced binders confirmed by crystallography [@watson2023], typically paired with an inverse-folding step to choose the amino acids, while ESM3 casts sequence, structure, and function as jointly generatable tokens [@hayes2025]. The gap is brutal and physical: a design that looks perfect in silico still has to fold, express, and work in a tube, and wet-lab success rates set the true score.

**Cell engineering (Chapter 10)** moves up from single molecules to whole cells: predict how a cell's state (read out by single-cell RNA sequencing) shifts when you perturb it with a CRISPR knockout or a base edit, and ideally steer it toward a target state. The hardness is combinatorial — the space of genetic perturbations and their interactions is astronomically larger than any screen — and again causal, since observing that two genes move together does not tell you that editing one moves the other.

<figure>
<img src="assets/figures/molecular-pipeline.svg" alt="Five boxes left to right labeled target, property, structure, design, cell, each tagged with a chapter number and joined by arrows.">
<figcaption>The five molecular problems are not rivals but stations on one pipeline: pick a target, characterize it, see it, build against it, and put it to work in a cell.</figcaption>
</figure>

!!! collaborator "Collaborator"
    *A wet-lab partner asks: AlphaFold solved structure, so are we done?* No, and the confusion is worth naming. Structure prediction answers "what shape is this natural sequence," which is one station on the pipeline. It does not hand you a target worth drugging, a binding affinity, a molecule that does not exist yet, or how the protein moves. Each of those is a separate problem with its own model and its own, lower, success rate.

## The genomic and regulatory problems

The genomic lobe has two flagship problems. The first is **sequence-to-function** (Chapter 11): read a long window of DNA and predict the regulatory activity it produces — the family of **tracks** that assays measure along the genome, such as RNA expression, chromatin accessibility, protein-DNA binding, and 3D contacts (Chapter 4 covers what each assay actually measures). The line runs from Enformer, which pulled in long-range context up to about 100 kilobases [@avsec2021], through Borzoi, which predicts RNA-seq coverage at 32-bp resolution and so scores transcription, splicing, and polyadenylation at once [@linder2025], to AlphaGenome, which unifies many track types across a megabase at single-base resolution [@avsec2026]. What makes this hard is that regulation is long-range and cell-type-specific: the sequence that controls a gene can sit far away, and the same DNA does different things in a neuron and a liver cell.

<figure>
<img src="assets/figures/sequence-to-function.svg" alt="A DNA window box feeds a sequence model box, which fans out into four stacked wavy signal tracks labeled RNA-seq, ATAC, ChIP-seq, and Hi-C.">
<figcaption>A sequence-to-function model is a one-to-many predictor: one DNA window in, a stack of cell-type-specific regulatory tracks out.</figcaption>
</figure>

The second problem is **variant-to-mechanism** (Chapter 12): given a specific genetic change, say what it does. The catch is that "what it does" changes character as you move along the **allele frequency spectrum** — the range from mutations carried by one family to those carried by a third of the planet. Rare variants tend to have large effects, because natural selection removes anything both common and severely damaging, so a variant that is both frequent and present usually has a small effect. That single fact splits the field in two. At the rare, large-effect end sit Mendelian and coding variants, where per-variant tools like AlphaMissense score the damage of an amino-acid change [@cheng2023] and gene-level burden tests aggregate rare hits. At the common, small-effect end sit **GWAS** (genome-wide association studies), which flag DNA positions statistically associated with a trait across a population — but a hit is tangled by **linkage disequilibrium** (LD), the tendency of nearby variants to be inherited together, so the associated position usually only *tags* the true cause. Untangling it needs fine-mapping and colocalization (Chapter 5 is the primer), and the deeper reason it is hard is **polygenicity**: many traits are driven by thousands of tiny-effect variants with no single culprit to find.

<figure>
<img src="assets/figures/allele-frequency-spectrum.svg" alt="A scatter with allele frequency on the x-axis from rare to common and effect size on the y-axis from large to small, showing a rare large-effect cluster upper-left and a common small-effect cluster lower-right along a descending curve.">
<figcaption>The allele frequency spectrum is why one modality needs two toolkits: selection pins large effects to rare variants, so Mendelian methods and GWAS are solving different problems on the same DNA.</figcaption>
</figure>

There is one honest gap worth flagging now because it recurs. Sequence-to-function models predict variation *across* genes and cell types well, but they explain *personal*, inter-individual variation poorly: on paired personal genomes and transcriptomes, leading models often miss even the direction of a variant's effect on expression [@sasse2023]. DNA language models like Evo 2, trained across the whole tree of life, extend the toolkit further into variant scoring and design [@brixi2026], but do not close this particular hole. Keep it in view — it is exactly the kind of gap the three-beat map exists to surface.

!!! warning "Common trap"
    Treating a GWAS hit as "the gene for" a trait. The associated marker is usually not causal, often does not fall in the gene it is named after, and shares its signal with a whole LD block; naming the actual mechanism is a separate, harder step.

!!! collaborator "Collaborator"
    *A genomics collaborator asks: if these models nail expression prediction, why can't they tell me what my patient's variant does?* Because "predict expression across genes" and "predict how one person's variant shifts expression" are different problems that happen to share an output. The first rewards learning what strong promoters look like; the second demands sensitivity to the small sequence differences between two humans, and that is where current models are weakest.
