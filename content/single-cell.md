A single-cell foundation model wants to be for cells what a protein language model is for proteins: pretrain once on a giant unlabeled corpus, learn a general representation of "cell state," and transfer that representation to many downstream tasks. The corpus exists, and it is enormous. Public atlases now hold well over a hundred million cells, each one a full transcriptome, and models like Geneformer, scGPT, and scFoundation are transformers trained to fill in masked genes across that sea of cells. This appendix does two things. First it pins down what the data actually is, because the shape and the noise of single-cell measurements drive everything downstream. Then it looks honestly at the models, including the load-bearing finding that on several headline tasks they do not yet beat embarrassingly simple baselines. Keep the data primer (Chapter 4) and cell engineering (Chapter 11) nearby; this appendix is the deeper look those chapters point to.

## What single-cell data measures

Single-cell RNA sequencing (scRNA-seq) measures transcript abundance one cell at a time, and its output is a **cell-by-gene matrix**: one row per cell, one column per gene, and in each entry a count of how many RNA molecules of that gene were captured in that cell (Chapter 4).
A modern experiment gives you tens of thousands of cells by roughly twenty thousand genes, so the matrix is large before you have modeled anything.
The counts themselves are small integers, often obtained by tagging each captured molecule with a unique molecular identifier (a random barcode, or UMI, that lets you count original molecules rather than amplification copies).

The defining feature of that matrix is that it is mostly empty.
A typical entry is zero, and the fraction of zeros routinely runs past 90%.
Some of those zeros are real biology, a gene that is genuinely off in that cell, but many are **dropout**: the gene was transcribed and the assay simply failed to capture it, because catching a few thousand molecules out of the hundreds of thousands in a cell is a lossy, shallow sampling.
That is the single hardest fact about the modality. A zero is ambiguous, and the sparsity is a mixture of signal and missingness that no amount of downstream cleverness fully resolves.

<figure>
<img src="assets/figures/cell-by-gene-matrix.svg" alt="A grid with cells as rows and genes as columns, most cells blank to show zeros, a scattering of shaded entries showing counts, with a callout distinguishing a true-off zero from a dropout zero.">
<figcaption>Single-cell data is a huge, mostly-empty count matrix, and its zeros are the problem: some mean the gene is off, some mean the assay missed it, and the model cannot always tell which.</figcaption>
</figure>

!!! intuition "Intuition"
    Think of each cell as a photograph taken in near-darkness with a very short exposure: the bright genes register, but most of the scene is under-sampled into black, so a blank pixel might be truly empty or just too dim to have caught any light.

The reason to care is scale. A single lab's experiment is a matrix; a **cell atlas** is the union of thousands of them, a reference compendium spanning tissues, donors, and conditions and reaching tens to hundreds of millions of cells (the Human Cell Atlas, CELLxGENE, and similar efforts).
That scale is exactly what makes self-supervised pretraining (Chapter 3) plausible here: mask a gene, predict it from the rest of the cell, and you have a free training signal across a hundred million cells.
It is also where the trouble starts, because those cells were measured in different labs on different platforms, so a large fraction of the variation between two cells is technical **batch effect** rather than biology (Chapter 15).

!!! collaborator "Collaborator"
    *If most entries are zero, are you not just modeling missingness?* Partly, and that is the risk. Highly expressed housekeeping genes dominate the nonzero entries, so a model can score well by learning the boring, shared backbone of every cell while missing the rare, low-count genes that actually distinguish one cell type from another. Which is why representation quality has to be judged on cell-type-resolving tasks, not on reconstruction loss.

## The models and the baseline debate

The models take the atlas and pretrain a transformer on it, differing mainly in how they turn a cell's counts into tokens.
**Geneformer** uses **rank-value encoding**: instead of feeding raw counts, it ranks the genes in a cell from most to least expressed (each gene normalized by its typical expression across the corpus) and feeds that ordered list of gene tokens [@theodoris2023].
Ranks are nonparametric and robust to the wildly different sequencing depths between cells, which sidesteps some of the count-noise problem.
It was pretrained on roughly 30 million human cells with a masked-gene objective (later versions expand the corpus past 100 million) and is adapted by fine-tuning to tasks like predicting whether a gene is essential or classifying a disease state.
**scGPT** keeps expression values and learns a joint embedding of genes and their binned expression with a generative masked objective, pretrained on tens of millions of cells [@cui2024].
**scFoundation** pushes the scale, a 100-million-parameter model over about 20,000 genes trained on more than 50 million cells, with an architecture built to read a cell's full expression vector at once [@hao2024].
When these are turned toward perturbation prediction they become the perturbation-response models of Chapter 11; here the interest is the general-purpose representation itself.

<figure>
<img src="assets/figures/foundation-vs-baseline.svg" alt="Grouped bars for three tasks, cell-type annotation, batch integration, and perturbation prediction, each comparing a foundation model bar against a simple baseline bar, with the bars nearly tied or the baseline slightly ahead.">
<figcaption>On the tasks the models were sold on, a foundation model and a simple baseline (PCA on highly variable genes, or a linear method) land close together, and the baseline sometimes wins outright.</figcaption>
</figure>

Now the honest part, because this is the field's live argument.
Independent benchmarks have repeatedly found that these models struggle to beat simple baselines on their headline tasks.
A careful zero-shot evaluation showed that the pretrained embeddings from Geneformer and scGPT underperform conventional methods, and sometimes plain principal-component analysis on highly variable genes, at cell-type clustering and batch integration, the exact jobs a general cell representation is supposed to nail [@kedzierska2025].
On the perturbation side, deep models trail predicting the training mean for unseen genes and an additive model for gene pairs [@ahlmanneltze2025].
The common thread is that single-cell data has a strong, cheap-to-capture structure (a few axes of variation, dominated by a handful of high-count genes), so a linear baseline already gets most of the way, and the extra capacity of a pretrained transformer has not reliably added signal on top.

!!! warning "Common trap"
    Do not read "pretrained on 100 million cells" as "state of the art on your task." The scale is real and the pretraining loss goes down, but a low masked-gene loss does not certify a useful embedding. Always benchmark against a boring baseline, PCA or highly variable gene selection with a standard integration method, before you believe a foundation model earned its keep (Chapter 16).

This is not a claim that the models are worthless.
The debate is genuinely open, results are task-dependent, and fine-tuning (rather than zero-shot use) narrows or closes the gap on some classification tasks, while the models can be handy where labeled data is scarce and transfer helps.
But the burden of proof sits with the model, not the baseline, and much of the early enthusiasm outran the evidence.
Two forces explain the mismatch.
The transfer premise that works so well for protein language models leans on deep evolutionary constraint per sequence; a cell's transcriptome carries far less of that kind of structure, and far more technical noise.
And the evaluations that first looked impressive often rewarded recovering coarse cell types that a linear method recovers too.

!!! collaborator "Collaborator"
    *So should I reach for a single-cell foundation model on my atlas?* Only after a baseline bake-off. Run PCA on highly variable genes with a standard integration method, measure the task you actually care about, and adopt the foundation model only where it clearly wins on your data and your metric. Treat it as one option on the shelf, not the default, and hold it to the honest-evaluation bar the rest of this book insists on (Chapters 15 and 16).
