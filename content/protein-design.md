Prediction and design are mirror images. A structure predictor (Chapter 8) reads a sequence you hand it and tells you the shape it folds into. Design runs the arrow backwards: you *specify* what you want — a shape, a surface that grips a chosen target, an active site that performs a reaction — and the model invents a molecule that meets the spec. This is *de novo* design: building a protein or small molecule from scratch rather than editing one nature already made. The mental model for the whole field fits in one line. Generative models now propose novel molecules by the thousand, cheap silicon filters throw most of them away, and the survivors go to a bench that decides which handful actually work. The gap between "the computer likes it" and "it works in a tube" is the whole story of the chapter.

## The problem: designing new molecules

The forward problem has one right answer and you can check it: fold the sequence, compare to the crystal structure. The inverse problem has *many* right answers and no cheap way to check any of them. A thousand different sequences can fold to the same backbone; countless backbones could present the surface you want. You are searching an astronomically large space (twenty amino acids at every position, hundreds of positions) for the rare members that fold, stay soluble, and do a job. And "does it do the job" cannot be read off a file — it needs a physical measurement.

<figure>
<img src="assets/figures/design-inverts-prediction.svg" alt="Two horizontal arrows. Top: sequence maps forward to structure, labeled prediction. Bottom: a function-or-shape specification maps forward to a novel molecule, labeled design, drawn as the inverse direction.">
<figcaption>Design is prediction run backwards: you fix the desired shape or function and search for a molecule that satisfies it, out of a space with many valid answers and no cheap way to check them.</figcaption>
</figure>

The field is organized by *what* you specify. Fix a backbone shape and you want a **de novo protein** that folds to it. Fix a *target* (a disease protein) and you want a **binder**, a small designed protein that clamps onto a chosen patch of its surface with high affinity. Fix a chemical reaction and you want an **enzyme**, the hardest ask, because you are designing a precise geometric arrangement of catalytic residues, not just a complementary surface. A parallel track designs **small molecules** to sit in a protein's pocket, the generative face of structure-based drug design.

!!! intuition "Intuition"
    Prediction asks "what does this sequence do?" Design asks "what sequence does this?" — same physics, but the second question has a haystack of answers and you can only test a few straws.

!!! collaborator "Collaborator"
    *"Why not just mutate a natural protein that already sort of works?"* That is directed evolution or engineering, and it is often the right call. De novo design earns its keep when nature has no good starting point — a binder to a target with no known antibody, an enzyme for a reaction biology never invented, a fold built to spec. You trade a warm start for an unconstrained blank page.

## Models that attempt it

The workhorse for structure is **diffusion**, the same denoising idea as in image generators applied to atomic coordinates. **RFdiffusion** starts from a cloud of random 3D points and iteratively denoises them into a plausible protein backbone, and you can condition it: hold a target fixed and it grows a binder against a chosen patch; scaffold a set of catalytic residues and it builds a protein around them [@watson2023]. **Chroma** is a comparable programmable backbone generator that can be steered by symmetry, shape, and other constraints [@ingraham2023]. These models give you a *backbone* — a shape — but no sequence.

Turning a shape into a sequence is **inverse folding**, and the standard tool is **ProteinMPNN** [@dauparas2022]. Given fixed backbone coordinates, it predicts which amino acids fold to that backbone, decoding residues with a message-passing graph network over the atoms.

!!! warning "Common trap"
    ProteinMPNN is *not* a masked-language-model encoder like ESM (Chapter 8), and it does not read a sequence. It reads 3D coordinates and writes a sequence. ESM learns amino-acid statistics from millions of sequences; ProteinMPNN learns the structure-to-sequence map from the PDB. Different input, different job. Confusing the two is a common interview stumble.

For small molecules, the analogue is target-aware generation. **TargetDiff** diffuses atom coordinates and types *inside a protein pocket*, generating 3D molecules shaped to fit [@guan2023], while docking models like **DiffDock** frame pose-finding — where and how a molecule sits — as diffusion over the ligand's translations, rotations, and torsions [@corso2022]. These share the design pipeline's spirit but inherit small-molecule headaches: synthesizability and the crudeness of scoring binding from structure alone.

The pieces only become a *method* when you chain them into a loop.

<figure>
<img src="assets/figures/design-generate-filter-validate.svg" alt="A left-to-right pipeline of four boxes: backbone generation, sequence design, refold-and-score, wet lab. A curved arrow loops from the scoring stage back to generation, labeled rejected designs are resampled.">
<figcaption>The loop that makes design work: generate many candidates, keep only the ones a structure predictor agrees will fold, and let the bench be the final judge. Cheap silicon does the culling so expensive wet-lab slots are spent on the likeliest few.</figcaption>
</figure>

The middle step, the **self-consistency** filter, is what makes the whole thing tractable. You designed a sequence *for* a backbone; now feed that sequence to an independent structure predictor (AlphaFold2 or ESMFold, Chapter 8) and ask whether it folds back to the shape you intended. If the predicted structure matches — low RMSD between design and refold, high confidence (**pLDDT**) — you trust it; if not, you discard it. Because you generate thousands and predict cheaply, you can throw away 99% and still have plenty to order. A newer twist skips the separate backbone step entirely: **BindCraft** runs backpropagation *through* AlphaFold2 itself, optimizing a binder sequence directly toward a high-confidence complex ("hallucination"), and reports experimental success rates of 10-100% depending on target [@pacesa2025]. DeepMind's **AlphaProteo** is a closed-system generator reporting high hit rates and nanomolar affinities across several targets in a single screening round [@zambaldi2024].

## What they do well and what is still hard

Read the numbers with the pipeline in mind. When a paper says "90% of designs bind," it means 90% of the survivors *after* self-consistency and developability filtering, screened in an assay tuned to that method. The in-silico funnel is spectacular and the raw wet-lab hit rate is far lower — many designs never fold, never express, or bind too weakly to matter. Aggressive filtering is what closes the gap, which is exactly why the loop, not any single model, is the unit of progress.

<figure>
<img src="assets/figures/design-silico-to-wetlab-funnel.svg" alt="A downward funnel of four shrinking bars: ten thousand backbones generated, hundreds pass the self-consistency filter, a small fraction bind in the wet lab, and only a handful show genuine catalytic function.">
<figcaption>Every stage discards most of the previous one. Headline success rates are measured at a late, narrow slice of the funnel; the honest end-to-end yield from raw generation to a working molecule is much smaller — and narrows further when the goal is function, not just binding.</figcaption>
</figure>

The sharpest divide is **binding versus function**. Designing a surface that sticks to a target is now close to routine for many targets, because sticking is a matter of shape and chemical complementarity — the thing diffusion and self-consistency are built to get right. Designing genuine *catalysis* is far harder: an enzyme must hold several residues in near-perfect geometry, stabilize a fleeting transition state, and cycle substrate in and product out, all while the protein breathes. Progress is real and recent — designed **serine hydrolases** now show meaningful catalytic efficiency and crystal structures matching the design, using RFdiffusion plus ensemble scoring of active-site preorganization [@lauko2025], and RFdiffusion2 scaffolds active sites from bare functional-group geometry — but designed enzymes still land orders of magnitude below evolved ones in turnover, and each success tests only a handful of the many designs made.

!!! collaborator "Collaborator"
    *"Your model loves this binder. Will it survive my lab?"* Passing self-consistency is necessary, not sufficient. **Developability** is the rest: does it **express** (can cells actually manufacture it), stay soluble instead of aggregating, tolerate storage, avoid triggering an immune response? A predictor scores none of these directly. Treat a passing design as a hypothesis to be measured, and budget for the ones that fold on-screen but clump in the tube.

!!! note "Note"
    The static-structure limitation from Chapter 8 bites twice as hard here. A predictor that returns one rigid snapshot cannot fully judge a design whose function *is* motion — an enzyme's catalytic cycle, a binder that must accommodate a flexible target. Self-consistency checks the fold, not the dynamics, which is one reason function lags behind shape.

The takeaway to carry forward: generative design has made proposing plausible novel molecules cheap and fast, and the binding problem is well on its way to solved for accessible targets. What remains hard is everything the wet lab measures and the file cannot — expression, developability, and above all genuine function. The bench, not the benchmark, still writes the verdict, which is the theme of the lab-in-the-loop workflow in Chapter 16.
