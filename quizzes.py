"""Single source of truth for the end-of-chapter "Check yourself" quizzes.

Each chapter closes with a short set of challenging, collaborator-style
multiple-choice questions. `build.py` renders the quiz for a chapter after its
References section, and a small inline script makes it interactive: the reader
picks an option, the choice is marked right or wrong, the correct answer is
revealed, and an explanation appears.

The questions are meant to be *hard* in the way a sharp collaborator's question
is hard. The distractors are plausible misconceptions, stated with the same
confidence and detail as the answer, so that neither length nor specificity ever
signals which option is correct. The renderer shuffles the options on load, so
the position of the answer carries no information either — write the options in
any order and point `answer` at the right one. Each explanation carries a
second-layer detail the prose only gestures at, so the quiz teaches rather than
merely confirms.

Question strings are **plain text**. `build.py` HTML-escapes everything, which
would neutralize MathJax delimiters, so do not write `$...$` or `\\(...\\)`
here; phrase math in words or with plain symbols instead.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """One multiple-choice question.

    `options` are shuffled at render time, so their order here does not matter;
    `answer` is the index (into this tuple) of the single correct option.
    `explanation` is revealed after the reader answers and should teach, not
    just confirm. Because the display order is randomized, never write an option
    that refers to another by position (e.g. "same as A").
    """

    prompt: str
    options: tuple[str, ...]
    answer: int
    explanation: str

    def __post_init__(self) -> None:
        assert self.prompt.strip(), "Question has an empty prompt."
        assert len(self.options) >= 3, f"{self.prompt!r}: need at least 3 options."
        assert all(o.strip() for o in self.options), f"{self.prompt!r}: empty option."
        assert (
            0 <= self.answer < len(self.options)
        ), f"{self.prompt!r}: answer index {self.answer} is out of range."
        assert self.explanation.strip(), f"{self.prompt!r}: empty explanation."


# No quizzes yet. Add a tuple of 4-6 Questions under each chapter's slug as the
# chapter is drafted; the build asserts the 4-6 range and that every slug is
# real.
_QUIZZES: dict[str, tuple[Question, ...]] = {
    "introduction": (
        Question(
            prompt="What makes the foundation-model recipe unusually well-suited to biology, compared with the classic one-model-per-task approach?",
            options=(
                "Biology has huge unlabeled sequence corpora but scarce, costly labels, and self-supervision learns from the sequences alone.",
                "Biological tasks are inherently simpler than language tasks, so one model can comfortably memorize the answers to all of them.",
                "Labeled biological datasets have finally grown large enough that supervised training from scratch no longer benefits from pretraining.",
                "Biological sequences are far shorter than text passages, so one model can hold every task in memory simultaneously with room to spare.",
            ),
            answer=0,
            explanation="The leverage comes from the label economics: experimentally solved structures and measured affinities are costly and rare, while raw sequences are abundant. Self-supervision turns the abundant, unlabeled resource into a training signal, which is why the recipe transferred. Labels remain scarce, not plentiful, and biological sequences (a full genome, a long protein) are often longer than text spans, not shorter.",
        ),
        Question(
            prompt="A protein language model is trained only to predict masked amino acids and never sees a single 3D structure. Why does structural information still show up in its representations?",
            options=(
                "The masking objective quietly includes pairwise distance labels derived from Protein Data Bank structures during training.",
                "Conserved and co-varying positions are encoded in the sequences, so predicting masked residues forces the model to internalize them.",
                "The model interpolates plausible structures from an internal lookup table of the known folds it memorized during pretraining.",
                "Structural signal appears only once the model is fine-tuned on labeled crystallography data, and never from masked pretraining on its own.",
            ),
            answer=1,
            explanation="Positions that co-vary across homologous sequences are typically in physical contact, and positions that stay fixed are under functional constraint. Filling in masked residues well requires capturing that coupling, so structure emerges as a byproduct of the sequence objective. The result holds from pretraining itself, with no structural labels in the loss, which is the surprising part.",
        ),
        Question(
            prompt="In the 'two lobes' framing, what actually connects the molecular/therapeutic lobe and the genomic/regulatory lobe?",
            options=(
                "They are connected merely because both lobes happen to rely on the very same transformer architectures internally, under the hood.",
                "The central dogma: a genomic change can alter a protein's sequence or how much of it a cell makes.",
                "They currently share one set of pretrained weights spanning both DNA and protein sequence at the same time.",
                "They are connected only through shared benchmark datasets and leaderboards, not through any underlying biology.",
            ),
            answer=1,
            explanation="The biological link is the flow from DNA to RNA to protein: one lobe asks what a genomic region does, the other what a molecule does, and a single variant can act in either. Note the leak in the 'one brain' analogy — today's protein models and genome models are typically separate systems that do not share weights, so the unified model is an aspiration, and multimodal integration (Chapter 13) is the active bridge.",
        ),
        Question(
            prompt="Current sequence-to-function models like AlphaGenome top many variant-effect benchmarks. What is the honest limitation a skeptical collaborator should raise?",
            options=(
                "They cannot process DNA windows longer than a few hundred bases at a time, so distal regulation is invisible to them.",
                "They predict variation across genes and tissues well but explain inter-individual variation poorly, sometimes with the wrong sign.",
                "They only work on protein-coding regions and ignore the non-coding regulatory genome almost entirely in practice.",
                "They require a fresh multiple sequence alignment to be constructed at inference time for every single variant prediction that they make.",
            ),
            answer=1,
            explanation="Benchmarks that reward distinguishing genes or tissues can be aced while the clinically relevant question — how a given person's variant shifts expression — stays poorly answered, occasionally with the wrong sign. This is the personal-variation gap documented for genomic deep-learning models, and it is a case study in why a leaderboard win is not biological truth. These models in fact handle long windows and specialize in non-coding regulation, so those are not the gap.",
        ),
        Question(
            prompt="How does this book calibrate depth for a machine-learning practitioner learning biology?",
            options=(
                "It teaches biology all the way to a full thesis-defense level of detail and assumes no prior machine learning experience whatsoever.",
                "It teaches enough biology to reason about what assays and models mean, assumes ML fluency, and defers deeper machinery to primers.",
                "It teaches neither field in any depth and stays purely at the level of popular science news headlines throughout.",
                "It re-derives the transformer and backpropagation from first principles before introducing any biology whatsoever.",
            ),
            answer=1,
            explanation="The invariant is awareness-and-synthesis, not PhD-in-the-weeds: you learn what a variant or an assay is and when a benchmark answers your question, while ML is assumed and only briefly refreshed. Deeper foundations live in the primer chapters (2 through 5) and appendices, so the problem chapters can move fast without re-deriving backpropagation.",
        ),
    ),
    "landscape": (
        Question(
            prompt="Why does this book insist on mapping the problems before introducing the models, rather than just comparing benchmark scores?",
            options=(
                "Because a benchmark scores a proxy, and only the problem tells you whether that proxy matches the real decision and how hard the split is",
                "Because most biological problems have no established benchmarks yet, so comparable scores simply are not available to line up side by side",
                "Because foundation models are still too new for any of their reported benchmark numbers to be trustworthy or reproducible across labs",
                "Because the important benchmarks in biology are proprietary and cannot be cited or redistributed in a textbook like this one at all",
            ),
            answer=0,
            explanation="A score is meaningless without the difficulty of the task and whether the metric tracks the decision you care about. A variant model can hit high AUROC separating known pathogenic from random variants yet be useless at ranking novel variants of unknown significance, which is the actual clinical need.",
        ),
        Question(
            prompt="A collaborator says 'AlphaFold solved structure, so protein work is basically done.' What is the most accurate correction?",
            options=(
                "Structure prediction remains unreliable even for single well-behaved proteins, so essentially nothing downstream of it can really be trusted yet",
                "Structure prediction answers one station on the pipeline, not target choice, binding affinity, de novo design, or a protein's dynamics",
                "AlphaFold only works on proteins that already have an experimental structure deposited in the PDB, so it cannot generalize at all",
                "The remaining work is purely engineering and speed, since the actual scientific problems around structure are now essentially closed",
            ),
            answer=1,
            explanation="Sequence-to-structure for natural single chains is largely solved, but target choice, property prediction, de novo design, and conformational dynamics are separate problems with their own models and lower success rates. A static structure is not a function.",
        ),
        Question(
            prompt="On the allele frequency spectrum, why do common variants tend to have small effects?",
            options=(
                "Because common variants are simply older, and their effect sizes decay over evolutionary time as the surrounding sequence drifts away",
                "Because effect size is measured per carrier, so dividing one fixed total effect across many more carriers necessarily shrinks each one",
                "Because natural selection removes variants that are both common and severely damaging, leaving frequent ones with mostly small effects",
                "Because common variants overwhelmingly fall in non-coding regions, which by their very nature cannot carry large phenotypic effects",
            ),
            answer=2,
            explanation="Selection is the mechanism: a variant that badly harmed fitness could not reach high frequency. This is exactly why the modality splits into rare large-effect methods (burden tests, AlphaMissense) and common small-effect methods (GWAS).",
        ),
        Question(
            prompt="A GWAS flags a variant strongly associated with a disease. Why can you not conclude that this variant, or the gene it sits in, is the cause?",
            options=(
                "Because GWAS report correlations only for common variants, while disease is driven mostly by rare variants the arrays cannot even see",
                "Because linkage disequilibrium ties the hit to a whole block of co-inherited variants, so it usually only tags the true cause nearby",
                "Because GWAS p-values are typically not corrected for multiple testing, so the large majority of reported hits are false positives",
                "Because association studies on their own cannot distinguish coding from non-coding variants without a separate dedicated structure model",
            ),
            answer=1,
            explanation="The associated marker is often non-causal and may not even fall in the gene it is named after, because nearby variants are inherited together as an LD block. Fine-mapping and colocalization are the extra steps that move from a tagging association toward a mechanism.",
        ),
        Question(
            prompt="Sequence-to-function models like Enformer and Borzoi score well on standard benchmarks. What is the honest, well-documented gap in what they deliver?",
            options=(
                "They predict variation across genes and cell types well but explain inter-individual differences poorly, sometimes even missing a variant's direction",
                "They cannot handle long-range regulation at all, so any enhancer that sits more than a few kilobases away from its gene is effectively invisible to them",
                "They only ever predict RNA expression and are unable to output other assay types such as chromatin accessibility or physical contacts at all",
                "They overfit badly to rare variants and therefore fail whenever the particular variant being scored happens to be common in the population",
            ),
            answer=0,
            explanation="On paired personal genomes and transcriptomes, leading models often fail to capture how one person's variants shift expression. 'Predict expression across genes' and 'predict a single individual's variant effect' share an output but are different problems, and the second is where these models are weakest.",
        ),
    ),
    "ml-onramp": (
        Question(
            prompt="Why does self-supervised pretraining on unlabeled protein sequence transfer to a downstream task like stability prediction?",
            options=(
                "The pretraining corpus already contains experimental stability measurements as hidden labels, which the model quietly memorizes during training.",
                "Predicting masked residues well is impossible without internalizing the evolutionary and biochemical regularities that govern stability too.",
                "The model learns to copy each protein's curated database annotation, and stability happens to be one such stored annotation among many.",
                "Masked prediction really teaches the model to compress sequences, and the resulting compression length is a direct readout of stability.",
            ),
            answer=1,
            explanation="Transfer works because the pretraining objective is a hard proxy: a model that reliably fills in masked residues must have learned which substitutions evolution tolerates, and that knowledge overlaps with what stability tasks need. There are no stability labels or annotations in the raw sequence corpus, which is exactly why the free self-supervised signal is so valuable.",
        ),
        Question(
            prompt="You want to prioritize point mutations as likely damaging, with no labeled data for your protein. What do you compute?",
            options=(
                "The attention weight the model places on the mutated position, averaged across all of its layers and heads.",
                "The Euclidean distance in embedding space between the wild-type and the mutant sequence representations.",
                "The model's log-probability of the mutant residue minus that of the wild-type residue at the same site.",
                "A fine-tuned regression head trained on the ProteinGym benchmark first, before you are able to score anything.",
            ),
            answer=2,
            explanation="Zero-shot variant scoring uses the log-likelihood ratio: a large negative value means the model finds the mutant surprising relative to wild-type, which correlates with damage. ESM-1v reaches about 0.5 Spearman with deep mutational scans this way, with no per-protein training. Embedding distance and attention weights are not calibrated to variant effect, and fine-tuning would defeat the point of a zero-shot method.",
        ),
        Question(
            prompt="A collaborator wants to generate a novel 3D protein backbone from scratch. Which model family is the natural fit, and why?",
            options=(
                "A diffusion model, because iterative denoising turns noise into valid 3D coordinates where left-to-right order is meaningless.",
                "A masked encoder like ESM-2, because bidirectional context over the whole sequence is precisely what pins down a protein's fold.",
                "An autoregressive decoder, because emitting coordinates one atom after the next guarantees a physically valid and unbroken chain.",
                "Any of the three families, since the choice is set by sheer model size rather than by the training objective that was used.",
            ),
            answer=0,
            explanation="3D coordinates have no natural left-to-right order, so autoregressive generation is awkward; diffusion instead denoises a whole structure at once and is the basis of RFdiffusion and AlphaFold3's structure head. The family is fixed by the training objective, not by parameter count, which is why the same transformer blocks appear across all three families doing different jobs.",
        ),
        Question(
            prompt="A model assigns your engineered enzyme variant a high likelihood. Your collaborator concludes it will have higher catalytic activity. What is wrong with this reasoning?",
            options=(
                "Likelihood is only ever defined for true wild-type sequences, so it simply cannot be computed for an engineered variant in the first place.",
                "High likelihood means the sequence looks evolutionarily natural, which is not the same as being optimal for an engineered goal like turnover.",
                "Likelihood measures structural stability directly, so it predicts how well a protein folds but says nothing at all about the sequence itself.",
                "The conclusion is perfectly correct, since evolution reliably optimizes every natural protein for its maximal possible catalytic activity.",
            ),
            answer=1,
            explanation="Likelihood scores naturalness, a decent prior over plausible sequences, but your objective may pull away from what evolution produced; the two can diverge when you optimize for a designed goal. Evolution optimizes for organismal fitness under constraints, not for any single enzyme's turnover, so 'natural-looking' and 'best for my assay' are genuinely different targets.",
        ),
        Question(
            prompt="What most sharply distinguishes an autoregressive decoder like Evo 2 from a masked encoder like ESM-2?",
            options=(
                "The decoder factors probability left to right and samples new sequence; the encoder fills masked tokens from bidirectional context.",
                "The decoder is essentially always far larger in parameter count, and that sheer scale is precisely what lets it generate sequence at all.",
                "The encoder is fundamentally unable to assign any probability to a sequence whatsoever, whereas the decoder can do so directly and easily.",
                "The encoder is trained with supervised labels throughout, while the decoder is trained entirely without any labels of its own to guide it.",
            ),
            answer=0,
            explanation="The defining difference is the factorization: left-to-right for the decoder, which makes sampling natural, versus bidirectional masked fill-in for the encoder, which yields context-aware representations. Both are self-supervised and both can score sequences; encoders assign per-site pseudo-likelihoods even though they do not generate autoregressively, so 'encoders cannot score' is a common misconception.",
        ),
    ),
    "data-modalities": (
        Question(
            prompt="A collaborator hands you an ATAC-seq track and asks which genes are highly expressed in the sample. What is the correct response?",
            options=(
                "ATAC-seq measures chromatin accessibility, not transcript levels; an open region can host a silent gene, so RNA-seq is what reads expression",
                "ATAC-seq peaks are essentially a direct count of transcripts, so the very tallest peaks reliably mark the most-expressed genes in the sample",
                "ATAC-seq measures where transcription factors sit bound to DNA, so peak height gives expression once you normalize by the factor's identity",
                "ATAC-seq reports 3D contact frequency, so you must first fold the track into a contact map before you can read any expression off it",
            ),
            answer=0,
            explanation="Accessibility marks where regulation can happen, not what was transcribed. A promoter can be open yet transcriptionally silent, so accessibility and expression are correlated but distinct measurements. ChIP-seq is the assay for protein binding and Hi-C for 3D contacts, which the distractors conflate.",
        ),
        Question(
            prompt="In Enformer and Borzoi, what is the relationship between DNA sequence and the RNA-seq / ATAC / CAGE readouts?",
            options=(
                "The DNA sequence and the assay tracks are both fed in as inputs, and the model predicts a separate downstream phenotype from them",
                "The DNA sequence is the input and the assay tracks are the prediction targets the model is trained to reproduce",
                "The assay tracks are the inputs and the model outputs a cleaned, corrected version of the reference genome from them",
                "Each assay is predicted by its own separate model, and the DNA sequence merely selects which of those models to run",
            ),
            answer=1,
            explanation="These are sequence-to-function models: one DNA window in, thousands of coverage tracks out, trained against measured ENCODE/GTEx data. The key habit is that a modality's role depends on the question; RNA-seq is a target here but could be an input in a model that predicts cell type from expression.",
        ),
        Question(
            prompt="Why is experimentally determined 3D structure a far scarcer training resource than protein sequence?",
            options=(
                "Structures are routinely withheld from public databases for intellectual-property reasons, while raw sequences are almost always shared freely",
                "Structures are simply computed directly from sequence, and so they only ever exist in the cases where someone actually bothered to run the prediction",
                "Each structure demands slow, costly crystallography or cryo-EM, so the PDB holds far fewer entries than the hundreds of millions of known sequences",
                "Structures physically decay while sitting in storage and have to be re-measured periodically, which keeps the total usable count persistently low",
            ),
            answer=2,
            explanation="The supply gap is experimental, not legal or computational: solving one structure by X-ray or cryo-EM is expensive and slow, so the PDB (~220k) trails known sequences (hundreds of millions) by orders of magnitude. That scarcity is exactly the gap AlphaFold was built to close by predicting structure from abundant sequence.",
        ),
        Question(
            prompt="A protein language model trained only to predict masked amino acids, with no fitness labels, still scores well on ProteinGym. What does this show?",
            options=(
                "The likelihood a self-supervised model assigns a variant already tracks its measured fitness, so DMS data is a held-out yardstick, not an input",
                "The model must have been secretly trained on the DMS assays themselves, since a purely unsupervised model cannot possibly rank variants at all",
                "ProteinGym really just measures raw sequence recovery, so essentially any language model scores well on it regardless of the true fitness",
                "The result only holds because the ProteinGym labels are themselves derived from the very same UniProt sequences the model already saw in training",
            ),
            answer=0,
            explanation="Evolution already filtered sequences for fitness, so a model that learns the statistics of natural proteins assigns lower likelihood to deleterious variants without ever seeing an effect label. Here the assay is the evaluation, not the input, illustrating that the same DMS data is a target in one setup and a benchmark in another.",
        ),
        Question(
            prompt="Enformer predicts expression across many genes impressively. A statistician asks whether it will explain why two patients differ in expression of the same gene. What is the honest answer?",
            options=(
                "Yes, the cross-gene accuracy transfers over directly, since predicting the differences between genes is strictly harder than predicting between two individuals",
                "Not reliably; these models capture cross-gene variation far better than inter-individual variation, sometimes even getting a variant's direction wrong",
                "Yes, but only after the model is first retrained on patient-specific Hi-C contact maps for each individual being compared",
                "No, because the model is architecturally unable to accept a given individual's personal variants as an input in the first place",
            ),
            answer=1,
            explanation="Cross-gene skill and personal-genome skill are different tests, and current models pass the first far better than the second, sometimes mispredicting the sign of a cis-variant's effect. The models can accept individual sequences; the failure is in accuracy on inter-individual differences, an open problem for variant interpretation.",
        ),
    ),
    "genetics-primer": (
        Question(
            prompt="Why do common genetic variants tend to have small individual effect sizes on traits?",
            options=(
                "Purifying selection prevents strongly deleterious alleles from drifting to high frequency, keeping large effects rare.",
                "Genotyping arrays measure only common variants, so any large effects are simply missed by the assay.",
                "Common alleles are older, so compensatory mutations have accumulated to buffer their original effects.",
                "Statistical power is higher for common variants, which shrinks their estimated effects toward zero.",
            ),
            answer=0,
            explanation="The empty upper-right corner of the frequency-versus-effect plot is a selection phenomenon, not a measurement artifact. A large-effect deleterious allele lowers reproductive success and is removed before it can become common, so the common variants that survive are individually weak. This is also why ML predictors can treat high cross-species allele frequency as a proxy for benign.",
        ),
        Question(
            prompt="A GWAS lead SNP passes genome-wide significance. What is the most defensible conclusion?",
            options=(
                "It is the causal variant, since surviving multiple-testing correction rules out chance.",
                "It marks a region containing a causal variant but is often just a correlated tag, not the cause.",
                "It necessarily alters a protein-coding sequence, which is what drove the strong signal.",
                "It is causal, though only within the specific ancestry group that was sampled.",
            ),
            answer=1,
            explanation="Linkage disequilibrium makes every variant in a haplotype block rise together, so the smallest p-value marks the best tag, not necessarily the cause. Most GWAS hits are non-coding and act through regulation, and localizing the actual variant requires fine-mapping the correlated block rather than trusting the lead SNP.",
        ),
        Question(
            prompt="The bulk of the 'missing heritability' for common traits is now best explained by which account?",
            options=(
                "Overestimated twin-study heritability that inflated the target the hits were compared against.",
                "Gene-by-environment interactions that no additive genetic model can ever capture.",
                "Rare structural variants that remain invisible even to whole-genome sequencing.",
                "Many sub-threshold common variants of tiny effect that individual hits fail to capture.",
            ),
            answer=3,
            explanation="SNP-heritability estimates that read the whole genome jointly recover most of the gap, showing the signal was hiding in thousands of weak variants below the significance line rather than truly missing. This polygenic picture, taken to its extreme, is the omnigenic model: signal smeared across most of the genome.",
        ),
        Question(
            prompt="Colocalization analysis (as in coloc) is designed to test what?",
            options=(
                "Whether a GWAS signal and a nearby molecular QTL are driven by the same causal variant.",
                "Whether two SNPs are in linkage disequilibrium within the same haplotype block.",
                "Whether a gene's expression level correlates with the trait across many individuals.",
                "Whether an association replicates when the study is repeated in a second ancestry cohort.",
            ),
            answer=0,
            explanation="Colocalization asks whether two signals at a locus share a causal variant, which is stronger than mere proximity. The tempting near-miss is the expression-trait correlation, which is closer to a TWAS-style test and can be confounded by two distinct nearby causal variants that coloc is specifically built to distinguish.",
        ),
        Question(
            prompt="Mendelian randomization treats a genetic variant as a natural experiment. Which assumption is most central to that being valid?",
            options=(
                "The exposure and outcome must be measured in the very same individuals.",
                "The variant must reach genome-wide significance in the discovery cohort.",
                "The variant must influence the outcome only through the exposure, not other pathways.",
                "The variant must be in strong linkage disequilibrium with the true causal variant.",
            ),
            answer=2,
            explanation="The instrumental-variable logic breaks under horizontal pleiotropy, when the variant reaches the outcome through routes other than the exposure. Random inheritance handles ordinary confounding, but a pleiotropic variant biases the causal estimate, which is why careful MR uses multiple instruments and tests for heterogeneity among their estimates.",
        ),
        Question(
            prompt="An ML practitioner will recognize population stratification most readily as which familiar problem?",
            options=(
                "A batch effect: ancestry correlates with both allele frequency and trait, faking associations.",
                "Label noise from genotyping error that mainly inflates false negatives.",
                "Overfitting caused by having more variants than samples in the design matrix.",
                "Data leakage from including the outcome among the model's input features.",
            ),
            answer=0,
            explanation="Ancestry is a confounder that shifts allele frequencies and trait prevalence together, so an allele can track a trait purely because of where it was sampled. The fix mirrors batch-effect correction: regress out genetic principal components or use a mixed model before trusting any association.",
        ),
    ),
}


def _validate(
    quizzes: dict[str, tuple[Question, ...]],
) -> dict[str, tuple[Question, ...]]:
    """Assert every chapter's quiz has a sensible number of questions."""
    for slug, questions in quizzes.items():
        assert (
            4 <= len(questions) <= 6
        ), f"Chapter '{slug}' must have 4-6 questions, has {len(questions)}."
    return quizzes


QUIZZES: dict[str, tuple[Question, ...]] = _validate(_QUIZZES)
