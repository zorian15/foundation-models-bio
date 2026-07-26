A small molecule is not a protein, and that difference organizes this whole chapter.
Where a protein is a chain of hundreds of amino acids whose statistics evolution has already written down, a drug like aspirin is a compact assembly of twenty-one atoms, with no sequence to read off and no homologs to align.
Vast libraries of molecular *structures* exist — hundreds of millions of catalogued compounds — but molecules never reproduced under selection, so, unlike a protein family, a drug carries no evolutionary record of what works.
Yet the job is just as hard: a small-molecule drug must grip one chosen protein tightly, ignore the roughly twenty thousand other human proteins, and survive the body's chemistry long enough to act.
This is the small-molecule peer to protein and binder design (Chapter 9), and the book's molecular lobe is otherwise almost entirely protein-centric.
The models split into two faces — one *scores* a molecule you hand it, the other *generates* a molecule to fit a pocket — and the intellectual spine running under both is a real, unsettled tension: whether to trust general models that learn from data and compute, or to bake in the physics that chemistry has understood for a century.

## The problem: potency, selectivity, and surviving the body

Fix a target protein with a druggable pocket (druggability and pocket-finding are Chapter 6) and ask for a small molecule that acts on it.
Three demands pull at once.
The first is **potency**: how little of the drug you need to get the effect, usually reported as an **IC50** or **EC50** — the concentration that produces half of the maximum inhibition or effect, so a lower number means a more potent molecule — and underneath it a binding affinity, the dissociation constant Kd from property prediction (Chapter 7), where smaller is tighter.
The second is **selectivity**: binding *only* the intended target and not the thousands of related proteins whose accidental engagement becomes a side effect or a toxicity.
The third is everything the body does to the molecule — the **ADMET** properties (absorption, distribution, metabolism, excretion, toxicity) that Chapter 7 treats as affinity-adjacent properties in their own right.
A molecule can be exquisitely potent in a tube and still be useless because it is promiscuous, or because the liver destroys it in minutes.

To model any of this you first have to represent the molecule, and there are three standard views, each adding what the previous one throws away.
The flattest is **SMILES** (Simplified Molecular-Input Line-Entry System), a text string encoding atoms and bonds — `CC(=O)O` is acetic acid — which lets you treat a molecule like a sentence and reuse language-model machinery.
One step richer is the **molecular graph**, atoms as nodes and bonds as edges, the natural input for a graph neural network and the view that makes chemistry's connectivity explicit.
Richest, and the one where potency is actually decided, is the 3D **binding pose**: a specific placement of the molecule's atoms inside the target's pocket, presenting the right **pharmacophore** — the arrangement of hydrogen-bond donors and acceptors, hydrophobic groups, and charges that the pocket is shaped to grip.
Structure-based drug design lives in this last view; the flat views are cheaper but blind to the geometry that binding depends on.

<figure>
<img src="assets/figures/small-molecule-representations.svg" alt="Three panels left to right: a SMILES text string, a 2D molecular graph of nodes and bonds, and a 3D molecule seated in a concave protein pocket, connected by arrows.">
<figcaption>One molecule, three views: the SMILES string and 2D graph are cheap to compute on but blind to geometry, and potency is decided only in the last view, where atoms meet the pocket.</figcaption>
</figure>

!!! intuition "Intuition"
    A small molecule is a key with no sequence to study; you cannot read evolution off twenty atoms, so you are forced to reason about the *shape* of the key and the *shape* of the lock rather than the statistics of an evolutionary corpus.

!!! collaborator "Collaborator"
    *"Isn't the goal just to bind as tightly as possible?"* No, and chasing raw affinity is how programs get into trouble. A molecule optimized only for potency tends to grow greasy and promiscuous, sticking to many proteins and to fat rather than staying selective and drug-like. The real objective is a balance: enough potency, real selectivity, and ADMET behavior that survives a body. Potency is the easiest of the three to predict and the least sufficient on its own.

## Models that attempt it

The models wear two faces, and it helps to keep them separate.
The first face is **scoring**: given a molecule and a pocket, estimate how well it binds.
Scoring a molecule against a target is an old problem — for decades the tool was **QSAR** (quantitative structure–activity relationship), regressing hand-crafted molecular descriptors against measured activity, the ancestor of every learned scorer here.
The structure-based version is **docking**: search over candidate poses of the molecule in the pocket and rank them with a **scoring function**, a fast estimate of binding quality standing in for a real free energy.
**AutoDock Vina** is the classical workhorse, pairing an efficient pose search with an empirical, physics-inspired scoring function [@trott2010].
**Gnina** keeps Vina's search but replaces the scorer with an ensemble of convolutional neural networks that read the 3D complex directly — a learned scoring function grafted onto a classical docker [@mcnutt2021].
The newest option folds scoring into structure prediction: the co-folding models from Chapter 8 (AlphaFold3, and the open Boltz and Chai lines [@abramson2024; @wohlwend2024; @chai2024]) predict the joint protein–ligand structure, and **Boltz-2** adds a binding-affinity head on top, reporting correlation approaching that of open-source free-energy perturbation at over a thousandfold less compute, and outperforming every method submitted to the CASP16 affinity challenge in a retrospective evaluation [@passaro2025].

The second face is **generating**: rather than score a molecule you supply, invent one that fits the pocket.
A **molecular generative model** samples new molecules from a learned distribution — over SMILES strings, graphs, or 3D atom clouds — instead of scoring ones you hand it.
The pocket-conditioned 3D generators are the direct analogue of protein backbone design: **TargetDiff** diffuses atom coordinates and types inside a fixed pocket, growing a molecule shaped to fit [@guan2023], and **Pocket2Mol** samples atoms autoregressively from an equivariant network conditioned on the pocket, trading diffusion's iterative denoising for direct placement [@peng2022].
**DiffDock** attacks the neighboring problem of pose-finding by framing docking itself as diffusion over the ligand's position, orientation, and torsion angles [@corso2022].
Chapter 9 named these as a parallel small-molecule track in a single paragraph; here they are the main event, and they inherit two headaches the protein side largely escapes — whether a proposed molecule can actually be made, and how crudely structure alone predicts binding.

<figure>
<img src="assets/figures/score-vs-generate.svg" alt="Two mirrored rows sharing a central pocket. Top row: a molecule feeds an arrow into an affinity-score gauge, labeled scoring. Bottom row: an empty pocket feeds an arrow into a newly drawn molecule, labeled generating.">
<figcaption>Scoring and generating are inverse arrows over the same pocket–molecule fit: one asks how well a given molecule binds, the other invents a molecule to bind, and both are limited by how faithfully structure predicts affinity.</figcaption>
</figure>

!!! note "Note"
    Generation happens in whichever view the model represents. SMILES and graph generators (language models and graph diffusion over 2D structure) are cheap and produce chemically valid molecules easily, but they never see the pocket, so they optimize drug-likeness and predicted properties rather than fit. Pocket-conditioned 3D generators see the geometry but must also solve the harder problem of placing atoms in space. Which view you pick decides what the model can and cannot know.

## The bitter lesson versus physical constraints

Here is the tension the rest of the chapter has been circling.
Rich Sutton's *bitter lesson* is the observation, drawn from seventy years of AI, that general methods which leverage computation and data eventually beat methods built on hand-engineered human knowledge, and beat them by a wide margin [@sutton2019].
Language modeling is the poster child: scale the data and the parameters, and structure you would have hand-coded emerges for free.
Molecular ML feels the opposite pull.
The field's instinct is to *bake in* physics — **equivariance** so a model's predictions rotate with the molecule, explicit energy terms, known bond geometry, and at the far end a **force field** (a parameterized model of the potential energy of a set of atoms) driving a physics simulation.
The most rigorous form is **free energy perturbation (FEP)**: simulate the alchemical transformation of one ligand into another and compute the *relative* binding free energy between them, calibrated in real energy units.
Modern FEP+ protocols predict relative potencies of close analogs to roughly chemical accuracy, about 1 kcal/mol [@wang2015], which is exactly the hand-engineered, physics-heavy end of the spectrum the bitter lesson warns against.

What keeps this a genuine debate rather than a settled rout is data.
Language had trillions of tokens; well-measured protein–ligand binding data numbers in the low tens of thousands of complexes, heavily biased toward a few protein families and the chemotypes industry already explored.
In that regime, priors pay: a physical constraint is worth a great deal of missing data, which is why equivariant architectures and physics terms remain competitive and why FEP still wins for the narrow, high-value task of ranking close analogs in lead optimization.
And yet the balance is visibly shifting — Boltz-2 approaching FEP-level correlation from learned data is precisely the kind of result the bitter lesson predicts, arriving earlier than many chemists expected.
The honest position for 2026 is that the physics pole still holds where data is thin and calibration matters, the learned pole is winning where you need to triage millions of molecules fast, and neither has won outright.

<figure class="wide">
<img src="assets/figures/physics-to-learning-spectrum.svg" alt="A horizontal axis labeled MORE PHYSICS on the left and MORE LEARNED on the right. Method chips sit above the axis, left to right: FEP, force-field docking (Vina), learned scoring (Gnina), co-folding affinity (Boltz-2), pocket-conditioned generation (TargetDiff, Pocket2Mol). Contrasting annotations sit below each end.">
<figcaption>The whole field spreads along a single axis from hand-coded physics to pure learning; chemistry's data scarcity is what keeps the best place to stand genuinely unsettled rather than a march rightward.</figcaption>
</figure>

!!! collaborator "Collaborator"
    *"Why not just run a force field or FEP and skip the learned models?"* Because FEP buys calibration and mechanism at a steep price. It needs a good bound structure, careful hand-setup, a force field parameterized for your chemistry, and hours of GPU time *per pair* of ligands, so it does not scale to millions of candidates and stumbles on novel scaffolds it was never parameterized for. You use FEP late and narrow — ranking a handful of close analogs where a fraction of a kcal/mol decides the program — and cheap learned scoring early and wide, to triage a virtual library down to the few hundred worth simulating. They are complementary tools at different stages, not rivals for the same job.

!!! warning "Common trap"
    A docking score or a co-folding affinity value is a *ranking* signal, not a calibrated potency. A Vina score of −9 kcal/mol is not a measured binding energy, and a Boltz-2 affinity number orders your candidates but you cannot read a nanomolar Kd off it. These models are trained and validated to rank; treat the numbers as relative within one campaign, recalibrate against your own measured data, and never quote a predicted score as if it were an assay result.

## What they do well and what is still hard

Read the wins narrowly and they are real.
These models triage enormous virtual libraries, turning millions of candidates into a testable few hundred with meaningful enrichment; they propose pocket-fitted scaffolds a chemist would not have drawn; they rank close analogs well enough (FEP at the physics end) to guide lead optimization; and co-folding now hands you a plausible complex *and* an affinity estimate without a crystal structure to start from.
For prioritizing what to make and measure next, this is genuinely useful.

The frontier is everything causal and **in vivo** that a single scored pose cannot express.
Start with the scoring functions themselves: they correlate only weakly with measured affinity (the "scoring power" they are weakest at), and even AI dockers that post excellent pose RMSD can be producing physically invalid geometry — clashing atoms, strained bonds — and failing to generalize to targets unlike their training set, while classical physics-based tools stay more physically valid [@buttenschoen2024].
Selectivity is modeled only narrowly: within-family panels exist, but a scorer evaluates one target in isolation, the toxicity that kills a program comes from the thousands of proteins it was never scored against, and proteome-wide off-target prediction is not routine.
Then the in-vitro→in-vivo gap swallows the rest — potency in a well says little about whether a molecule is absorbed, evades metabolism, avoids toxicity, and reaches its target in a living body, the same dish-to-patient translation gap that haunts target discovery (Chapter 6) and cell engineering (Chapter 11).
Finally, generative models expose **synthesizability**: a pocket-conditioned generator will happily propose molecules no chemist can make.
Synthetic-accessibility scores are a rough filter and retrosynthesis planning the real test, and the problem compounds with distribution shift — a model confident on known drug-like space extrapolates poorly to the genuinely novel chemotypes a program most wants, which is exactly where its own scoring is least reliable.

<figure>
<img src="assets/figures/potency-to-invivo-gap.svg" alt="A vertical funnel of four narrowing boxes top to bottom: binds the target (in vitro potency), selective across roughly twenty thousand proteins, survives ADMET, works in a living body. A bracket on the left marks only the top box as what scoring models mostly see.">
<figcaption>Scoring models mostly see the top slice — binding in a tube — while a drug's fate is settled in the three slices below that no structure file shows: selectivity, ADMET, and behavior in a living body.</figcaption>
</figure>

!!! collaborator "Collaborator"
    *"Your model loves this compound. Will it be a drug?"* Almost certainly not by itself, and that is the honest answer to give. A high score means one thing: worth making and measuring. It says nothing about selectivity across the proteome, nothing about whether the liver clears it, nothing about whether it reaches the tissue that matters. Treat a top-ranked molecule as a hypothesis to enter the design–build–test–learn loop (Chapter 17), not a candidate to advance, and budget for the ones that dock beautifully and do nothing in a cell.

The mental model to carry forward: generative and scoring models have made it cheap to propose and rank pocket-fitting molecules, and the bitter-lesson-versus-physics balance is tilting slowly toward learning as data grows without ever fully abandoning the physical priors that scarce data still rewards.
What stays hard is the causal, in-vivo chain — selectivity, ADMET, and efficacy in a body — that a scored pose cannot reach, which is why evaluation must be designed to measure it (Chapter 16), why the bench remains the judge (Chapter 17), and why closing this gap is one of the open frontiers the Outlook (Chapter 18) returns to.
