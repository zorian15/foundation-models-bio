The premise of this book fits in one sentence: the recipe that produced large language models now trains on the molecules and code of life. That recipe is self-supervised pretraining on a vast corpus, which yields general-purpose representations you can reuse for many tasks. Swap the corpus of web text for a corpus of protein sequences, genomes, or single cells, keep almost everything else, and you get a *foundation model for biology* — a model that learned the statistics of evolution well enough to predict a protein's shape, score a mutation, or design a new enzyme. This chapter sets that mental model. The rest of the book is the payoff: problem by problem, what these models can do, and where they still break.

## Foundation models meet biology

A **foundation model** is a model pretrained once on a broad corpus with a self-supervised objective, then adapted to many downstream tasks instead of trained fresh for each one. Two words carry the weight. *Self-supervised* means the training signal comes from the data itself — mask an amino acid and predict it, or predict the next nucleotide — so you need no human labels. *Representations* are the internal vectors (embeddings) the model produces for an input; because they were shaped by the whole corpus, they transfer to problems the model never saw during training. This is the same shift that reorganized natural-language processing: one big pretrained model beat a zoo of narrow, task-specific ones.

Biology turns out to have exactly the ingredients this recipe wants. It has enormous unlabeled corpora — hundreds of millions of protein sequences in databases like UniProt and MGnify, trillions of DNA bases spanning the tree of life, millions of profiled single cells — and it has a chronic *shortage* of labels, because every experimentally solved structure or measured binding affinity costs real lab time. Self-supervision sidesteps that shortage. The striking empirical result is that a protein language model (a foundation model whose corpus is protein sequences) trained only to fill in masked residues ends up encoding structure and function it was never explicitly taught: you can read three-dimensional contacts and biophysical properties straight out of its embeddings [@lin2023]. Newer models push this further — ESM3 generates novel proteins by reasoning over sequence, structure, and function together [@hayes2025], and Evo 2, a DNA foundation model trained on over nine trillion nucleotides across all domains of life, both predicts and designs genomic sequence [@brixi2026].

!!! intuition "Intuition"
    Evolution already ran billions of experiments and wrote the results down as sequences; self-supervised pretraining is just reading that lab notebook at scale.

!!! collaborator "Collaborator"
    *You have no labels — how can the model learn anything real?* The sequence is its own answer key. A position that stays fixed across millions of related proteins is under evolutionary constraint, and a position that co-varies with another is physically coupled to it. Predicting masked residues forces the model to internalize those constraints, which is why structure and function fall out of a pure sequence objective.

<figure>
<img src="assets/figures/pretrain-recipe.svg" alt="A large unlabeled corpus of proteins, DNA, and cells feeds a self-supervised pretraining stage, producing one foundation model whose reusable representations fan out to structure, variant-effect, and design tasks.">
<figcaption>One corpus and one objective produce reusable representations; the downstream tasks come almost for free, which is why a single model replaces a zoo of task-specific ones.</figcaption>
</figure>

## Two lobes, one journey

The biological problems in this book split cleanly into two families, and it helps to hold both in your head from the start.

The **molecular / therapeutic lobe** works at the scale of a single molecule. Its questions are "what shape does this protein fold into, what does it bind, and can we design a new molecule that does job X?" This is the home of structure prediction — AlphaFold3 now predicts the joint structure of proteins with nucleic acids, ligands, and ions using a diffusion-based architecture [@abramson2024], and ESMFold does it from a single sequence with no alignment [@lin2023] — and of protein design (Chapter 9) and property prediction (Chapter 7).

The **genomic / regulatory lobe** works at the scale of a stretch of genome. Its questions are "what does this region of DNA *do*, and what happens if a base changes?" These are the **sequence-to-function** models, which read a long DNA window and predict functional readouts like gene expression, chromatin accessibility, and splicing. AlphaGenome, DeepMind's successor to Enformer, takes a one-megabase window and predicts thousands of such tracks at single-base resolution, matching or beating the best prior models on nearly all variant-effect benchmarks [@avsec2026]. This lobe is Part III (Chapters 11 and 12).

The two lobes are joined by the central dogma of biology: DNA is transcribed and translated into protein. A single mutation can change a protein's shape (molecular lobe) *or* change how much of that protein a cell makes (regulatory lobe), and often you cannot tell which without both views. **Multimodal integration** — building models that reason across DNA, RNA, protein, and cell state at once — is the bridge, and it gets its own chapter (Chapter 13).

!!! analogy "Analogy"
    Think of two lobes of one brain: the molecular side and the genomic side, wired together by the central dogma. Where it leaks: today's models mostly do *not* share weights across the two lobes — a protein language model and a genome model are separate systems. The "one brain" is the aspiration the field is building toward, not the shipping product.

!!! collaborator "Collaborator"
    *I only work on proteins — why should I care about the genome half?* Because a drug target lives in both lobes at once. You nominate a gene using genomic and regulatory evidence that it drives disease, then you drug the protein it encodes using structure and design tools. Skip either lobe and you either pick the wrong target or cannot make a molecule against it. Target discovery (Chapter 6) is exactly this handoff.

<figure>
<img src="assets/figures/two-lobes.svg" alt="Two boxes, a molecular-therapeutic lobe covering proteins, structure, and design, and a genomic-regulatory lobe covering DNA, expression, and variants, both connected downward to a shared multimodal-integration box.">
<figcaption>Why proteins and genomes are two faces of one modeling story: the central dogma links a molecule's structure to how much of it a genome makes.</figcaption>
</figure>

## What this book is and is not

Every problem chapter follows the same spine: **the problem**, then **the models** that attack it, then **what is still hard**. That last part is not a formality. Foundation models in biology are genuinely useful and genuinely oversold, sometimes in the same paper, and knowing the failure modes is what separates a practitioner from a press release.

The depth is calibrated deliberately. This book teaches you enough biology to be *dangerous and correct* — to know what an assay measures, what a variant is, and why a benchmark number does or does not answer your question — but not enough to defend a biology thesis. It assumes you already read machine learning fluently: you can follow a training loop, you know what an embedding is, and Chapter 3 refreshes the foundation-model machinery quickly rather than from scratch. Biology is what gets taught. Chapters 2 through 5 build the shared vocabulary — the landscape of problems, the data modalities, and a genetics primer (Chapter 5) — before the problem chapters begin. Part V, "Doing it for real" (Chapters 14 through 16), covers the unglamorous parts that decide whether any of this survives contact with a real lab: messy data, honest evaluation, and closing the loop with experiments.

The honest open problems get named, not hidden. The sharpest current example lives in the regulatory lobe: sequence-to-function models predict variation *across* genes and tissues impressively well, yet they explain variation *across individuals* poorly, often getting even the direction of a personal variant's effect wrong [@huang2023]. A model can top a leaderboard and still miss the question a clinician actually asks. Holding both facts at once — the capability and the gap — is the frame of mind this book is trying to install.

!!! warning "Common trap"
    Reading a benchmark win as biological truth. A model that leads a variant-effect leaderboard can still fail on personal, inter-individual variation, because the benchmark and the clinical question are not the same distribution. Chapter 15 is about designing evaluations that measure what you actually care about rather than what is easy to score.

<figure>
<img src="assets/figures/chapter-spine.svg" alt="Three boxes left to right connected by arrows: the problem, then the models, then what is still hard.">
<figcaption>The spine of every problem chapter: capability is only half the story, and the honest limits are the other half.</figcaption>
</figure>
