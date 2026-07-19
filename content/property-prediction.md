A model that reads one molecule and predicts a number you could otherwise get only from an experiment: how tightly a drug candidate binds, whether a point mutation cripples an enzyme, how well a protein survives being heated, how much of it a cell will actually express. That is property prediction. The molecule is *given* — you are not searching for a new one, as in design (Chapter 9), and you are not folding it, as in structure (Chapter 8). You want a property, and you want it cheaply, before the assay (Chapter 4) that would measure it for real. The central bet of this chapter is that the same protein language models that learned sequence statistics can score properties they were never explicitly trained on, and that when you *do* have labels, a small supervised head on top does even better.

## The problem: from sequence to phenotype

Property prediction takes a single molecule and returns a measurable quantity. For proteins the workhorse quantities are: **variant effect** or **fitness** (how much a mutation helps or hurts function), **folding stability** (the free-energy change on mutation, written ΔΔG, where a positive value means destabilizing), **binding affinity** (typically a dissociation constant Kd — smaller means tighter), and **expression / solubility** (whether the cell makes usable protein at all). For small molecules the analogous bundle is **ADMET** — absorption, distribution, metabolism, excretion, and toxicity — the pharmacological properties that decide whether a promising binder can ever become a drug.

<figure>
<img src="assets/figures/property-axes.svg" alt="One variant sequence box on the left with arrows fanning out to five property boxes: fitness, folding stability, binding affinity, expression, and ADMET.">
<figcaption>The same input — one molecule — maps to many different measurable properties, and a model that is excellent at one axis can be useless on another.</figcaption>
</figure>

Why bother predicting these instead of measuring them? Scale. **Deep mutational scanning** (DMS), an assay that measures the functional effect of thousands to millions of variants of one protein in a single experiment, is powerful but still bounded by what one lab can build. A model that generalizes from a few such experiments can score every possible variant of a protein in seconds, turning a wet-lab screen into a ranked shortlist. That shortlist feeds target discovery (Chapter 6), where you ask which variants of a gene are damaging, and it feeds engineering, where you ask which mutations to try next.

!!! intuition "Intuition"
    A property predictor is a cheap, noisy stand-in for an assay: worth running when it reorders your candidates well enough that the top of its list is enriched for real hits, even if its individual numbers are wrong.

!!! collaborator "Collaborator"
    *Which of my assays can this actually replace?* None of them, yet. Treat it as a prioritizer that tells you which 50 of your 5,000 variants to measure first. The model earns its place if the wet-lab hit rate in its top-ranked slice is meaningfully above the background rate, not by matching your assay's numbers.

## Models that attempt it

Two families do the work, and they map onto the model families from the ML on-ramp (Chapter 3). The first is **zero-shot** scoring with a protein language model — zero-shot meaning no task-specific labels are used at all. A masked language model like ESM-2, or an autoregressive one like ProGen2, is trained only to predict amino acids from sequence context across UniRef-scale data, and in doing so it learns which sequences look "natural" [@rives2021]. To score a mutation you compare how probable the model finds the mutant residue versus the wild-type residue at that position: the **log-likelihood ratio** (LLR), log p(mutant) − log p(wild type). A large negative score means the model thinks the substitution is unlike anything evolution kept. This is the ESM-1v recipe [@meier2021].

<figure>
<img src="assets/figures/variant-scoring.svg" alt="A variant sequence feeds a protein LM, which branches to two arms: a zero-shot log-likelihood-ratio score needing no labels, and a supervised trained head needing labeled assay data.">
<figcaption>The same backbone model scores a variant two ways: a label-free likelihood ratio that measures evolutionary plausibility, or a supervised head fine-tuned to predict one specific measured property.</figcaption>
</figure>

The idea that likelihood tracks fitness rests on a real mechanism: natural sequences are the survivors of selection, so residues that would break function were removed from the training data, and the model assigns them low probability. The community benchmark is **ProteinGym**, a suite of 217 DMS assays covering millions of variants against which methods are scored by Spearman rank correlation to measured fitness [@notin2023]. On it, single-sequence PLMs land around 0.4–0.5 average Spearman (ESM-1v and ESM-2 650M are essentially tied there), and — worth internalizing — they do *not* dominate. Methods that exploit a **multiple sequence alignment** (MSA), the stack of evolutionarily related sequences for a protein, remain competitive or better: the alignment-based GEMME and hybrids like TranceptEVE cluster near the top, and AlphaMissense, an AlphaFold derivative fine-tuned on population variant frequencies, is state of the art for human missense pathogenicity [@cheng2023]. Recent analyses even suggest single-sequence PLM likelihood is hitting a scaling plateau on this task.

The second family is **supervised**: when you have labeled measurements for the exact property you care about, take the PLM's per-residue embeddings and train a regression head on them. This wins whenever labels exist. The clearest case is stability: the Tsuboyama megascale dataset measured folding stability for ~776,000 domain variants by proteolysis [@tsuboyama2023], and models fine-tuned on it — ThermoMPNN — reach Spearman around 0.72; note that the strongest stability predictors read the 3D backbone (ThermoMPNN builds on ProteinMPNN) rather than sequence-PLM embeddings on held-out stability, far above any zero-shot likelihood [@dieckhaus2024]. For small-molecule ADMET the same pattern holds without a language model at all: graph neural networks trained on the Therapeutics Data Commons benchmarks [@huang2021], as in ADMET-AI, are the practical default [@swanson2024].

!!! warning "Common trap"
    Likelihood-as-fitness measures *evolutionary plausibility*, not your objective. A residue that is conserved because it stabilizes the fold will score well even if you are trying to improve catalytic rate or binding to a non-natural target. The model tells you a variant looks like a real protein, not that it is a better one for your purpose.

## What they do well and what is still hard

These models are genuinely useful at what they are for: ranking single substitutions, flagging likely-deleterious mutations, and pre-screening a large variant library down to a testable set. Where they struggle traces to a few recurring failures.

**Off-distribution generalization.** PLMs are anchored to natural sequence space, so they extrapolate poorly to de novo or heavily engineered proteins that no longer resemble anything in UniRef — exactly the regime protein design (Chapter 9) operates in. The plateau in single-sequence performance on ProteinGym is a symptom: more parameters stop helping once the model has absorbed the evolutionary signal there is to absorb.

**Epistasis.** The effect of two mutations is often not the sum of their individual effects, and likelihood-based scores, computed largely per position, miss these higher-order interactions. In **reciprocal sign epistasis**, two individually beneficial mutations combine to break the protein — the case that most punishes an additive predictor.

<figure>
<img src="assets/figures/epistasis.svg" alt="A wild-type box branches to two individually stabilizing single mutants, plus A and plus B, which converge on a double-mutant box marked in red as unfolds.">
<figcaption>Sign epistasis: two mutations that each help on their own can destroy the protein together, so a model that adds up single-mutant predictions confidently gets the double mutant wrong.</figcaption>
</figure>

**Calibration.** Scores rank well but are not calibrated probabilities, and the useful decision threshold shifts from protein to protein. An LLR of −5 may mean "dead" for one enzyme and "mildly worse" for another, so a fixed cutoff over-flags on some proteins and under-flags on others.

**Fitness versus the activity you care about.** This is the deepest gap. Likelihood and stability are correlated with function broadly, but the specific number you want — a catalytic turnover, selectivity between two targets, an off-target toxicity — is a narrow slice that generic evolutionary plausibility does not resolve. Closing that gap is what the design–build–test loop (Chapter 16) is for, and it is why property models augment rather than replace experiments.

!!! collaborator "Collaborator"
    *A Spearman of 0.5 sounds mediocre — is it good enough to act on?* For picking values, no; for ordering candidates, often yes. What matters operationally is enrichment: if the top 5% of the ranked list contains several-fold more true hits than random, the model has already paid for itself, even though its per-variant predictions are too noisy for a calibrated decision.

For interpreting *human* variants specifically — pathogenic or benign rather than fitness in a dish — the framing shifts toward mechanism and population genetics, which is the subject of variant-to-mechanism (Chapter 12); the single-cell foundation models that predict expression phenotypes are covered lightly in the appendix.
