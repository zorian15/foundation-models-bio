Up to now you have designed one molecule at a time: a protein that folds (Chapter 8), a binder that sticks (Chapter 9), a small molecule that drugs a target (Chapter 7). Cell engineering asks a bigger question. Given a living cell, which set of deliberate interventions pushes it into a state you want: a T cell that resists exhaustion, a stem cell nudged toward a chosen lineage, a tumor cell coaxed back toward something normal. The molecule is the lever; the cell is the machine you are trying to reprogram. This chapter follows the same spine as the rest of Part II. First the problem of choosing perturbations, then the models trained on Perturb-seq to predict their effects, and finally the sobering distance between predicting a cell in a dish and helping a patient.

## The problem: programming cells

Start with two definitions. A cell's **state** is, for our purposes, its transcriptome: the vector of which genes are transcribed and how much, exactly the readout that single-cell RNA sequencing (scRNA-seq) gives you (Chapter 4). A **perturbation** is a deliberate change you make to the cell: knock a gene out (CRISPR cuts it so it stops working), turn one on or down (CRISPR activation or interference, CRISPRa/CRISPRi, which steer a gene's expression without cutting), or wire several of these into a small synthetic circuit. Programming a cell means finding the perturbation, or combination of perturbations, that moves the cell from its starting state A to a desired state B.

<figure>
<img src="assets/figures/cell-state-programming.svg" alt="A menu of perturbations feeds an arrow that moves a cell from state A to a target state B.">
<figcaption>Cell engineering is a search problem: pick perturbations that push a cell from where it is toward the state you want, not design a single molecule.</figcaption>
</figure>

Two things make this hard, and neither is solved by a bigger dataset alone. The first is combinatorics. With roughly 20,000 human genes there are about 200 million single-and-double combinations and astronomically more triples, so you cannot test them all, especially not in a patient-relevant cell. The second is that genes interact. Knock out two genes and the effect is often not the sum of the two single knockouts, a phenomenon geneticists call **epistasis**. That non-additivity is exactly the interesting biology, and exactly what makes the search space refuse to factorize into independent choices.

!!! intuition "Intuition"
    A perturbation is a nudge in a very high-dimensional state space; the goal is to find the small set of nudges whose combined push lands the cell on a target state, when the nudges do not simply add up.

This reframes target discovery (Chapter 6). There the question was which gene is causally tied to disease. Here you assume you have candidate levers and ask which interventions, applied together, produce the cell state you want. The genetics primer (Chapter 5) supplies the vocabulary of gene function and interaction that the state space is built on.

!!! collaborator "Collaborator"
    *Why not just screen every combination in the lab and skip the model?* Genome-scale Perturb-seq can perturb every gene one at a time (the largest screens use CRISPRi to knock genes down), but the pairs and triples explode past any budget, and the cells you can screen (immortalized lines) are not the cells you want to treat. You screen a slice and ask a model to rank the rest.

## Models that attempt it

The training data is **Perturb-seq**: a pooled CRISPR screen with a single-cell RNA-seq readout, so that every cell carries a label for which gene was perturbed and a full transcriptome of the result [@replogle2022]. One cell is one (perturbation, response) pair, and a single experiment yields millions of them (Chapter 4). A **perturbation-response model** learns from these pairs to predict the expression shift a held-out perturbation would cause.

<figure>
<img src="assets/figures/perturbation-response-model.svg" alt="Perturb-seq pairs feed a model that predicts the expression shift of a held-out perturbation.">
<figcaption>Every model in this space learns the same map: from a perturbation to the transcriptome shift it causes, so it can score perturbations no one has run yet.</figcaption>
</figure>

**GEARS** attacks the unseen-perturbation problem with a graph [@roohani2023]. It places every gene in a gene-gene network built from known pathways and co-expression, represents a perturbation by its neighborhood in that graph, and so predicts the effect of a gene it never saw perturbed by borrowing from its neighbors that it did. It handles single and two-gene perturbations, and its authors report gains on combinations where one or both genes were never perturbed alone.

**scGPT-perturb** takes a different route: fine-tune a single-cell foundation model. Models like scGPT [@cui2024] and Geneformer [@theodoris2023] are transformers pretrained on tens of millions of cells to learn a general representation of cell state, then adapted to the perturbation task. These general-purpose single-cell models are appendix-tier for us; see the single-cell foundation model appendix for how they are pretrained and where they help.

The most ambitious recent effort is Arc Institute's **State**, a "virtual cell" model [@adduri2025]. It has two modules. State Embedding (SE) maps a raw transcriptome into a smooth latent space that dampens technical noise and aligns cell types. State Transition (ST) is a transformer that predicts how a cell's embedding shifts under a given perturbation, and a decoder maps the shifted embedding back to gene expression. It was trained on one of the largest compendia assembled, roughly 170 million observational and over 100 million perturbational cells across dozens of cell lines (the Tahoe-100M dataset among them), and it targets genetic, chemical, and cytokine perturbations with an explicit goal of transferring across cell types. Arc also launched a Virtual Cell Challenge in 2025 that held out an unseen cell type (H1 human embryonic stem cells) with 300 CRISPRi perturbations, a purpose-built benchmark that drew over a thousand teams and made cross-context generalization the headline metric.

!!! collaborator "Collaborator"
    *What exactly is the label you predict?* Usually a pseudobulk shift: the mean expression change across cells for a perturbation, compared against control. That discards the cell-to-cell distribution, which is why some newer work argues the real target should be the full response distribution, not its average.

## What they do well and what is still hard

Give the field its due. These models recover, for genuinely hard perturbations, which genes respond and in which direction, and they do it across thousands of candidate perturbations fast enough to prioritize wet-lab follow-up. On its own benchmarks State improves the discrimination of perturbation effects and the detection of truly differentially expressed genes over prior models. As a hypothesis generator that ranks what to try next, this is real value.

<figure>
<img src="assets/figures/generalization-ladder.svg" alt="Three ascending rungs: seen perturbation, unseen single gene, and combinatorial or new cell type.">
<figcaption>Difficulty climbs faster than the models do: baselines already handle seen perturbations, and the top rung, combinations in a new cell type, is still open.</figcaption>
</figure>

Now the hard part, and it is genuinely hard. A careful 2025 benchmark tested scGPT, scFoundation, and GEARS against deliberately simple baselines: predicting the mean of the training perturbations, or an additive model for pairs [@ahlmanneltze2025]. For perturbations of genes not seen in training, the deep models did not beat predicting the training mean. For two-gene combinations, they did not beat the additive baseline. This is the load-bearing caveat of the whole area: much of the impressive-looking correlation comes from the fact that most perturbations barely move most genes, so a constant baseline already scores high. A more nuanced follow-up finds that deep models do win on the subset of "resistant" perturbations, recovering which genes flip and in which direction, but not the magnitude of the response.

!!! warning "Common trap"
    A high overall correlation with the true expression profile is not evidence a model learned biology. Always report the gap over the mean and additive baselines; on many splits that gap is near zero even when the raw score looks strong.

Two more gaps sit between a good benchmark number and a therapy. The first is **distribution shift**. Perturb-seq is run mostly in a handful of immortalized cell lines, and models trained on them transfer poorly to primary cells, other labs' batches, or a patient's tissue, because batch and cell-type effects can swamp the perturbation signal. That is precisely why the Virtual Cell Challenge scores held-out cell types. The second is the **dish-to-patient gap**, the same translation gap that haunts every chapter in this part. A predicted transcriptome shift is not a cellular phenotype, a phenotype is not a clinical benefit, and none of these models say anything about delivery, getting the edit into the right cells inside a body. Cell engineering also echoes protein design (Chapter 9): in-silico success rates run far ahead of validated wet-lab wins, so treat rankings as leads, not conclusions.

!!! collaborator "Collaborator"
    *If I run your top ten predicted combinations at the bench, what hit rate should I expect?* Better than random at calling the direction of response, especially for perturbations that actually do something, but unreliable on magnitude and on any genuinely novel biology. Budget it as hypothesis prioritization, and confirm in your own cells (Chapters 15 and 16).
