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
    "target-discovery": (
        Question(
            prompt="A gene is the single most strongly upregulated transcript in patient tissue versus healthy controls. Why is this, on its own, weak evidence that it is a good drug target?",
            options=(
                "Differential expression is correlational: the gene may be responding to the disease rather than driving it, so perturbing it need not change the phenotype",
                "RNA-seq reports transcript abundance, which is several steps removed from the protein level a drug actually engages, so a strong signal need not mark a druggable protein at all",
                "Strongly upregulated genes are usually a compensatory, protective response to the disease, so inhibiting one would remove a safeguard and make the phenotype worse",
                "Expression fold-changes this large sit within the noise band of bulk RNA-seq, so the ranking cannot reliably separate real targets from technical artifacts",
            ),
            answer=0,
            explanation="The core problem is direction of causation, not measurement. A gene can be upregulated because it causes the disease, because the disease changed it, or because both share an upstream driver — only the first makes it a target. This is exactly why human genetics and direct perturbation, which carry causal information, are prized over expression correlation.",
        ),
        Question(
            prompt="Why is a genetic variant treated as a stronger causal signal for a target than a case-control expression difference?",
            options=(
                "Genetic genotypes are measured far more precisely than noisy gene-expression readouts, so a variant association carries much less experimental noise than a case-control comparison ever could",
                "A variant is fixed at conception before the disease begins, so an association points from gene to disease rather than the reverse",
                "Variants always sit inside the very gene whose function they alter, which removes any ambiguity about which gene the association actually implicates",
                "Genetic effects are consistently larger in magnitude than expression differences, which makes a variant association much easier to detect above the noise",
            ),
            answer=1,
            explanation="The temporal ordering is what buys causality: because the variant is assigned quasi-randomly and precedes the disease, the disease cannot have caused the variant. Note the third option is actually false in a way that matters — the causal variant usually sits outside its target gene, which is why the locus-to-gene mapping problem exists at all.",
        ),
        Question(
            prompt="Human genetic support roughly doubles a target's probability of clinical success. What does this NOT imply?",
            options=(
                "Greater confidence in exactly which causal gene sits behind the association makes the success-rate boost larger, not smaller",
                "The roughly two-fold boost still holds even for variants of modest effect size, since the benefit tracks gene-level confidence rather than effect magnitude",
                "A target without any genetic support should be abandoned, since genetic evidence is required for approval",
                "Most genetically supported targets nonetheless still fail somewhere in clinical development, because the baseline success rate stays low",
            ),
            answer=2,
            explanation="Genetic support is a strong filter, not a requirement: the base success rate is low, so even a 2 to 2.6-fold boost leaves most programs failing, and many good targets have no detectable common-variant signal. Minikel and colleagues also showed the effect grows with confidence in the causal gene but is largely independent of the variant's effect size.",
        ),
        Question(
            prompt="What makes a Perturb-seq readout a fundamentally different kind of evidence from a network-embedding prediction?",
            options=(
                "Perturb-seq assays the entire genome one knockout at a time, whereas a network embedding can only score the few hundred genes that already sit close to known disease genes",
                "Perturb-seq measures each gene's protein structure directly, while a network embedding only ever captures coarse sequence similarity between genes",
                "Perturb-seq is causal by construction because you performed the intervention, whereas embedding proximity is a correlational hypothesis",
                "Perturb-seq requires no prior knowledge at all, while network embeddings are strictly limited to the genes that already have known variants",
            ),
            answer=2,
            explanation="Perturb-seq actually knocks the gene out and reads the downstream transcriptome, so the effect it reports is caused by your intervention. A network embedding infers 'guilt by association' from proximity to known disease genes, which is a testable hypothesis, not a demonstrated effect. Both still face the dish-to-patient gap: a causal effect in an immortalized cell line may not hold in the relevant tissue.",
        ),
        Question(
            prompt="Why are LLM-agent systems that synthesize the target literature best treated as producing leads rather than decisions?",
            options=(
                "They can only read papers published before their training cutoff date, so they systematically miss the most recent biology and sometimes cite work that has since been retracted",
                "They synthesize existing knowledge and can hallucinate confident mechanisms, so their nominations must be independently verified",
                "They cannot query structured resources like Open Targets and are confined to free text, so their nominations rest on an incomplete slice of the evidence",
                "They systematically favor already-undruggable targets, because those are the ones that dominate the published literature they were trained to summarize",
            ),
            answer=1,
            explanation="These systems are fast, tireless synthesizers but inherit the literature's biases and can assert mechanisms that are not supported, so a nomination is a hypothesis to check. Systems like OriGene close part of this loop by pairing nomination with experimental validation, which is what turns a plausible lead into evidence.",
        ),
        Question(
            prompt="A collaborator argues that because in-silico target nomination is now cheap and fast, the main bottleneck in target discovery has been solved. What is the flaw?",
            options=(
                "Nomination is actually still the slow step, because a genome-scale Perturb-seq screen followed by careful curation takes years before any candidate can even be proposed",
                "Validation — knockouts, animal models, and eventually trials — remains expensive and slow, so the constraint has shifted to which few candidates you can afford to test",
                "In-silico methods still cannot rank the candidates they surface, so a human expert must sift the raw list and nominate each target by hand",
                "Druggability can now be predicted almost perfectly from structure, so causality is the only remaining source of uncertainty in the pipeline",
            ),
            answer=1,
            explanation="Cheap nomination moves the bottleneck rather than removing it: because generating candidates is now abundant and experimental validation is costly, the binding constraint is choosing the few hypotheses worth the years and millions to confirm. A wrong pick is most expensive precisely at this validation gate.",
        ),
    ),
    "property-prediction": (
        Question(
            prompt="Why does a protein language model's log-likelihood ratio predict variant fitness at all, given that it never saw fitness labels?",
            options=(
                "It was quietly pretrained on deep mutational scanning fitness values alongside the sequences, so the log-likelihood ratio is really just recalling those memorized experimental labels",
                "Natural sequences are survivors of selection, so substitutions that break function are rare in training data and get low probability",
                "It computes each variant's folding free energy from a built-in physics-based energy function and reads fitness straight off that thermodynamic estimate",
                "It aligns each variant back to a reference genome and simply counts up the mismatched positions",
            ),
            answer=1,
            explanation="The likelihood-as-fitness bet works because the training corpus is filtered by evolution: harmful residues were purged, so the model assigns them low probability. That is why the signal exists without labels, and also why it tracks broad evolutionary plausibility rather than any one engineering objective.",
        ),
        Question(
            prompt="On ProteinGym, how do single-sequence protein language models compare to alignment-based methods for zero-shot variant effect?",
            options=(
                "The largest single-sequence PLMs now decisively beat every MSA-based method on ProteinGym, which is exactly why alignment-based predictors have become obsolete",
                "MSA-based and hybrid methods remain competitive with or ahead of single-sequence PLMs, which sit around 0.4 to 0.5 Spearman",
                "MSA-based methods quietly require labeled DMS data to work while PLMs need none, so the two families are not really comparable on a zero-shot benchmark",
                "Essentially all of these methods clear 0.9 Spearman on ProteinGym, so which family you pick rarely changes the outcome in practice",
            ),
            answer=1,
            explanation="Single-sequence PLMs cluster near 0.4 to 0.5 average Spearman and do not dominate; alignment-based GEMME and hybrids like TranceptEVE, plus AlphaMissense, remain at or above them. Both approaches are label-free, and single-sequence performance appears to be plateauing rather than pulling ahead with scale.",
        ),
        Question(
            prompt="You add up a protein language model's single-mutant scores to predict a double mutant and get it badly wrong. What is the most likely cause?",
            options=(
                "The scores are epistatic in reality: two beneficial mutations can interact to break the protein, which an additive sum cannot capture",
                "The tokenizer split the double mutation across two separate tokens, corrupting the input so the model never actually scored the true combined sequence",
                "The model's per-position scores are poorly calibrated, so their absolute magnitudes drift by a constant offset that only grows when you add two of them together",
                "The multiple sequence alignment for this protein was far too shallow to cover both mutated positions jointly, so the pairwise term was never estimated",
            ),
            answer=0,
            explanation="Higher-order interaction, especially sign epistasis, means the combined effect is not the sum of parts, and per-position likelihood scores largely miss it. Calibration is a separate problem about absolute magnitudes; the failure here is the additive assumption itself.",
        ),
        Question(
            prompt="You have 20,000 labeled folding-stability measurements for your protein family. What is the strongest approach to predict stability for new variants?",
            options=(
                "Use the zero-shot likelihood ratio, since supervised heads overfit small biological datasets",
                "Fine-tune a supervised regression head on the model's embeddings using your measurements",
                "Average the predictions of several unrelated pretrained language models",
                "Rely on the model's raw perplexity, which already equals stability up to a scale factor",
            ),
            answer=1,
            explanation="When labels for the exact property exist, a supervised head on learned features wins: models trained on the megascale stability data reach roughly 0.72 Spearman, far above zero-shot likelihood. Likelihood measures evolutionary plausibility, which correlates with but does not equal folding stability.",
        ),
        Question(
            prompt="A variant-effect model reaches Spearman 0.5 against a DMS assay. What decision does that most justify?",
            options=(
                "Reporting calibrated per-variant probabilities of pathogenicity directly to a clinic for diagnostic use",
                "Prioritizing which variants to test first, if its top-ranked slice is enriched for true hits",
                "Assigning precise change-in-folding-free-energy values to each variant to feed a thermodynamic stability model",
                "Replacing the deep mutational scanning assay entirely for every protein in that family",
            ),
            answer=1,
            explanation="A moderate rank correlation supports ordering candidates, not calibrated numbers: what matters operationally is top-k enrichment over the background hit rate. It does not license precise per-variant values or clinical classification, and it complements rather than replaces the assay.",
        ),
    ),
    "protein-structure": (
        Question(
            prompt="A structure predictor gives a confident, sharp fold for a well-studied enzyme but a low-confidence, tangled result for a newly discovered orphan protein with no known relatives. What is the most likely reason?",
            options=(
                "The orphan protein is intrinsically disordered and so simply has no single stable structure for the predictor to converge on in the first place",
                "The orphan protein has too few homologs to build an informative MSA, so the co-evolution signal is weak",
                "Orphan proteins are almost always longer than the model's maximum context window, so the fold is truncated before it can be predicted",
                "The predictor was never trained on any sequences from that particular organism, so it cannot generalize to its unusual residue usage",
            ),
            answer=1,
            explanation="MSA-based predictors depend on co-evolution across many relatives. With few homologs, the alignment carries little contact signal and accuracy drops. This is exactly the regime where single-sequence models like ESMFold become attractive, though they too lose accuracy on genuinely hard, relative-poor targets.",
        ),
        Question(
            prompt="Why does AlphaFold2 alone struggle to model a protein bound to a small-molecule drug and a magnesium ion, and what changed with AlphaFold3?",
            options=(
                "AlphaFold2 predicts single amino-acid chains only; AlphaFold3 replaced the output with an all-atom diffusion decoder that jointly models proteins, nucleic acids, ligands, and ions",
                "AlphaFold2 was closed-source, whereas AlphaFold3 opened its weights so that individual labs could bolt on their own ligand and ion support",
                "AlphaFold2 emitted no confidence scores for ligands, so its poses could not be trusted, a gap that AlphaFold3's calibrated per-atom scores finally closed",
                "AlphaFold2 was trained before most small-molecule drug structures had been deposited in the PDB, and AlphaFold3 simply retrained on that newer, ligand-rich data without changing the architecture",
            ),
            answer=0,
            explanation="AlphaFold2 is a monomer/protein predictor. AlphaFold3's key architectural change is an atom-level diffusion generator that represents and folds arbitrary chemical components together, letting one network handle complexes and beat specialized docking tools. Open weights are a separate story that belongs to Boltz and Chai.",
        ),
        Question(
            prompt="A collaborator says 'AlphaFold solved protein structure, so we can stop doing crystallography.' What is the sharpest correction?",
            options=(
                "Crystallography is still required because AlphaFold cannot fold any protein larger than roughly 400 residues without its accuracy collapsing",
                "The models predict a single most-likely fold well for many proteins, but not conformational ensembles, dynamics, or disordered regions, and a fold is not the same as function",
                "AlphaFold is only accurate for proteins whose close relatives already sit in the PDB, so genuinely novel folds still demand experimental determination",
                "Cryo-EM has now fully replaced X-ray crystallography, so the real choice is between two competing experimental methods rather than between computational prediction and any experiment at all",
            ),
            answer=1,
            explanation="The models return one static structure and collapse the population of states a molecule visits. Dynamics, intrinsic disorder, large assemblies, and the leap from shape to function all remain open, which is why 'solved' overstates the case even though the first-draft fold is often excellent.",
        ),
        Question(
            prompt="What does a per-residue pLDDT confidence score most usefully flag when it is very low over a contiguous stretch of a prediction?",
            options=(
                "That the residues across that low-confidence stretch mark the enzyme's catalytically active site, which the model deliberately flags with reduced certainty",
                "That the model was forced to average several conflicting structural templates in that region, blurring the coordinates it ultimately reports there",
                "That the region may be intrinsically disordered or otherwise unreliable, even though coordinates were still drawn for it",
                "That the underlying sequence in that stretch contains a sequencing error and should be re-checked before the structure is used",
            ),
            answer=2,
            explanation="A model that outputs coordinates will place atoms even for a floppy, fold-free region; low pLDDT is your signal that the drawn shape is untrustworthy there. Disordered regions are common and functional, so a confident-looking ribbon over a low-pLDDT stretch is a classic way to be misled.",
        ),
        Question(
            prompt="By 2025-2026, what is the most accurate statement about open-weight structure models like Boltz and Chai relative to AlphaFold3?",
            options=(
                "They match AlphaFold3-level accuracy on biomolecular complexes and can be run and fine-tuned in-house",
                "They can only predict single isolated chains and still cannot handle the ligands or nucleic acids that AlphaFold3 folds jointly",
                "They run considerably faster but are substantially less accurate on complexes, making them useful only for rough, early-stage screening",
                "They still require a paid AlphaFold3 license to run at all, because under the hood they reuse its released weights",
            ),
            answer=0,
            explanation="The 2024-2026 shift is that co-folding capability is no longer confined to one lab: open models reproduce AlphaFold3-level accuracy on complexes under permissive licenses, and Boltz-2 even added a binding-affinity head that led the CASP16 affinity challenge. For a practitioner, in-house runnability and fine-tuning are the practical payoff.",
        ),
    ),
    "protein-design": (
        Question(
            prompt="A colleague calls ProteinMPNN 'basically ESM for design.' What is the sharpest correction?",
            options=(
                "ProteinMPNN reads 3D backbone coordinates and outputs a sequence, whereas ESM reads sequences; they solve different problems from different inputs",
                "ProteinMPNN is trained on far more raw sequences than ESM ever saw, so it generalizes better to novel folds while sharing the same masked objective",
                "They are essentially equivalent models, except that ProteinMPNN bolts a diffusion sampler on top of the ESM encoder to draw its designs",
                "ProteinMPNN predicts a full 3D structure from sequence, while ESM works in the opposite direction and predicts a sequence from a given structure",
            ),
            answer=0,
            explanation="ProteinMPNN is an inverse-folding model: its input is backbone geometry and its output is a compatible sequence, learned from PDB structure-sequence pairs via message passing. ESM is a protein language model trained on sequences alone. Neither predicts structure from sequence in the AlphaFold sense, and ProteinMPNN uses no diffusion and far fewer training examples than ESM's sequence corpora.",
        ),
        Question(
            prompt="A design paper reports '90% of designs bind the target.' What does that number most accurately describe?",
            options=(
                "The fraction of survivors after self-consistency and developability filtering that bound in an assay tuned to the method, not the raw yield from generation",
                "The fraction of all raw generated backbones that end up folding correctly once they are expressed and tested in the wet lab",
                "The probability that any single generated sequence, drawn at random straight from the model, binds its target with nanomolar affinity in the very first assay",
                "The clinical success rate of the binder once it has been developed all the way into an approved drug",
            ),
            answer=0,
            explanation="Headline success rates are measured late in the funnel, after aggressive in-silico filtering, and in an assay calibrated to that pipeline. The end-to-end yield from raw generation is far lower, because most designs never survive the self-consistency and developability filters. This is why the design loop, not any single model, is the real unit of progress.",
        ),
        Question(
            prompt="Why is designing an enzyme that catalyzes a reaction much harder than designing a binder to a target?",
            options=(
                "Catalysis needs several residues held in precise geometry to stabilize a transition state and cycle substrate, whereas binding mainly needs a complementary surface",
                "Enzymes are simply much larger proteins, so current diffusion models cannot generate a backbone long enough to hold a working active site together",
                "No structure predictor available today can score a candidate enzyme design for self-consistency, so the generate-filter loop cannot even be closed for them",
                "Binders can be fully validated in silico by refolding the design, whereas an enzyme's catalytic activity can only ever be confirmed slowly and expensively at the bench",
            ),
            answer=0,
            explanation="Binding is largely a matter of shape and chemical complementarity, exactly what diffusion plus self-consistency handle well. Catalysis demands sub-angstrom positioning of multiple catalytic residues, transition-state stabilization, and substrate turnover in a moving protein. Designed enzymes exist and improve, but still fall orders of magnitude below evolved turnover. Size is not the barrier, and self-consistency scoring applies to both.",
        ),
        Question(
            prompt="In the generate-filter-validate loop, what does the self-consistency filter actually check?",
            options=(
                "Whether an independent structure predictor folds the designed sequence back to the intended backbone with low RMSD and high confidence",
                "Whether the designed protein will express solubly, resist aggregation, and avoid triggering an immune response once it is produced in living cells",
                "Whether the small molecule generated to fill the binding pocket can actually be chemically synthesized at reasonable cost",
                "Whether the designed binder's measured affinity for its target comfortably exceeds a nanomolar threshold in the assay",
            ),
            answer=0,
            explanation="Self-consistency closes the loop between design and prediction: you designed a sequence for a backbone, so you refold that sequence with an independent predictor (AlphaFold, ESMFold) and keep it only if it returns to the intended shape. It scores foldability, not developability, synthesizability, or measured affinity, which is why passing designs are still hypotheses for the bench.",
        ),
        Question(
            prompt="A design passes self-consistency with excellent pLDDT but fails in your collaborator's lab. Which explanation is consistent with what the filter can and cannot see?",
            options=(
                "The design may fail to express, aggregate, or need dynamics its single static predicted structure never captured",
                "A high pLDDT score guarantees soluble expression in any host, so the bench failure has to come down to a pipetting or handling error",
                "Self-consistency already tests solubility and immunogenicity alongside the fold, so the model must simply have been wrong about the backbone geometry",
                "The predictor already scored the protein's dynamics correctly, so low binding affinity is the only explanation left for the bench failure",
            ),
            answer=0,
            explanation="Self-consistency and pLDDT judge whether a sequence folds to the intended static shape; they say nothing about expression yield, aggregation, storage stability, or immunogenicity, and a single rigid snapshot cannot capture function that depends on motion. Developability is measured at the bench, not scored by the predictor, so a fold-perfect design can still clump in the tube.",
        ),
    ),
    "cell-engineering": (
        Question(
            prompt="A 2025 benchmark compared scGPT, scFoundation, and GEARS against deliberately simple baselines. What did it find?",
            options=(
                "For unseen genes and two-gene combinations, the deep models did not beat predicting the training mean or an additive model",
                "The deep models clearly beat the simple baselines on unseen single genes, but lost their edge only on the harder two-gene combinations",
                "The deep models beat every simple baseline handily, but only once they were fine-tuned on a large enough number of cells from the target context",
                "The simple baselines failed almost entirely, because perturbation-driven expression changes are far too nonlinear for a constant or additive rule to predict",
            ),
            answer=0,
            explanation="The headline result is that on the hardest, most useful splits (unseen genes, novel pairs) the deep models roughly tied a constant mean or additive baseline. This works because most perturbations move most genes very little, so a constant prediction already scores high; the correct lesson is to always report the gap over mean and additive baselines, not raw correlation.",
        ),
        Question(
            prompt="How does GEARS predict the effect of a gene it never saw perturbed in training?",
            options=(
                "It embeds the gene in a gene-gene graph and borrows signal from perturbed neighbors",
                "It memorizes every training perturbation and simply returns the single nearest exact match when queried with a new gene",
                "It folds the unseen gene's protein product and reads the perturbation effect directly off the predicted 3D structure",
                "It averages across all of the training perturbations, weighting each one equally by the number of cells it was measured in",
            ),
            answer=0,
            explanation="GEARS represents a perturbation by its neighborhood in a network built from pathways and co-expression, so an unseen gene inherits a prediction from related genes that were perturbed. The graph is the whole mechanism for generalizing beyond observed perturbations, which is also why performance depends heavily on the quality and coverage of that prior network.",
        ),
        Question(
            prompt="In Arc Institute's State model, what is the division of labor between its two modules?",
            options=(
                "State Embedding maps transcriptomes into a latent space; State Transition predicts how that embedding shifts under a perturbation",
                "State Embedding predicts which perturbation was applied, while State Transition decodes that guess back into raw single-cell expression counts",
                "Both modules independently predict the full expression profile, and the pipeline simply averages their two outputs together at the end",
                "State Embedding handles the genetic perturbations while State Transition is reserved for the chemical, small-molecule ones, splitting the work by modality",
            ),
            answer=0,
            explanation="State Embedding (SE) learns a smooth, noise-dampened representation of cell state, and State Transition (ST), a transformer, predicts the perturbation-induced shift in that latent space before a decoder returns to expression. Separating representation from transition is what lets the model aim at transfer across cell types rather than memorizing one context.",
        ),
        Question(
            prompt="Why is predicting two-gene perturbations fundamentally harder than just scaling up compute?",
            options=(
                "Gene effects are non-additive, so a pair's effect is often not the sum of the two singles",
                "Two-gene combinatorial screens simply produce far too few cells per pair to train any model that scales with added compute",
                "CRISPR cannot reliably target two separate genes inside the same cell, so genuine combinations can never be measured directly",
                "Gene combinations always collapse to the simple mean of the two single-gene responses, which no amount of extra compute can improve",
            ),
            answer=0,
            explanation="Epistasis means the combined effect can amplify, cancel, or redirect the singles, so the response surface does not factorize into independent choices. That non-additivity is both the interesting biology and the reason an additive baseline is a nontrivial bar to clear on genuinely interacting pairs.",
        ),
        Question(
            prompt="What is the most important caveat when moving a perturbation-response model toward an actual therapy?",
            options=(
                "It is trained mostly in immortalized cell lines and predicts a transcriptome shift, which is far from a clinical phenotype, and it says nothing about delivery",
                "The model can only ever predict gene knockouts and is architecturally unable to represent an activating perturbation",
                "Single-cell readouts are so dominated by dropout noise that no real perturbation signal can be detected in them at all",
                "The model's predictions are valid only for the exact immortalized cell line used during training and cannot be scored or trusted for any other cellular context whatsoever",
            ),
            answer=0,
            explanation="Perturb-seq lives in a dish of immortalized cells, and a predicted expression change is several steps removed from phenotype and clinical benefit, with distribution shift to primary cells and the unsolved delivery problem on top. Treating a ranked prediction as a hypothesis to confirm in the target cells, not a result, is the honest posture.",
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
