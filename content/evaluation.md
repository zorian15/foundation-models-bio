A benchmark number is a promise about the future.
It says: on data like this, expect performance like that.
This chapter is about when that promise is honest and when it quietly lies.
The core idea is uncomfortable and load-bearing: a benchmark does not measure how good a model *is*, it measures whatever its metric and its data split happen to let it measure, and on biological data those two choices decide almost everything.
Change the metric and a mediocre model looks brilliant; change the split and a brilliant model looks mediocre, or the other way around.
Evaluation, done right, is the discipline of making the number you report mean the thing you actually care about — and refusing to celebrate a leaderboard win that answers a different question than yours.
This is the counterpart to the honest-limits half of every problem chapter, collected in one place and made rigorous.

## What a good benchmark measures

Three choices define a benchmark's number: the data it scores on, the metric that summarizes performance, and the split that divides training from test.
The data is the obvious one and the least interesting; the metric and the split are where evaluations quietly succeed or fail.

Start with the metric, because matching it to the biological question is the first fork.
Some questions are *ranking* questions: which fifty of my five thousand variants should I measure first?
There, a rank correlation like Spearman's, or the enrichment of true hits in your top slice (Chapter 7), is exactly right, and a model whose absolute numbers are nonsense can still win if it orders candidates well.
Other questions are *value* questions: is this predicted probability of pathogenicity high enough to act on, in absolute terms?
Those need calibration, not just ranking, and a docking score or a co-folding affinity that only ranks (the ranking-not-a-Kd trap of Chapter 10) fails them by construction.
The sharpest metric trap is class imbalance, the theme of data realities (Chapter 15).
Suppose 1% of variants are truly pathogenic and your classifier posts an **AUROC** of 0.95 — the area under the receiver-operating-characteristic curve, equal to the chance it ranks a random positive above a random negative.
That looks triumphant, but with 99% negatives a large absolute number of false positives barely moves the false-positive rate, so AUROC stays flattering while your actual precision, which that same pile of false positives wrecks, is poor.
**AUPRC** — the area under the precision–recall curve — and precision among your top-ranked calls tell the honest story, because they focus on the rare positive class you are hunting.
The rule is blunt: under heavy imbalance, report AUPRC or precision-at-k, and treat a high AUROC as decoration.

<figure>
<img src="assets/figures/auroc-vs-auprc-imbalance.svg" alt="Two ROC and precision-recall curves for the same imbalanced classifier. The ROC curve sits high near the top-left corner with an AUROC of about 0.95, while the precision-recall curve sags with a much lower AUPRC, annotated to show precision collapses among the rare positives.">
<figcaption>The same model, two verdicts: under 99-to-1 imbalance AUROC stays near 0.95 because abundant true negatives dominate, while AUPRC exposes that most flagged variants are wrong. The metric, not the model, decides whether the result looks like a triumph.</figcaption>
</figure>

Now the split, which is the heart of this chapter.
On ordinary tabular data a random train/test split is fine.
On biological data it is usually a lie, because biological data is not made of independent points — it is riddled with structure that ties test examples to training ones.
Two proteins can be 95% identical; two people can be cousins; two small molecules can share a scaffold; two genomic windows can sit on the same chromosome.
A random split scatters these near-duplicates across the train/test line, so the model is tested on things it has effectively already seen, and its score is inflated.
The fix is a split that matches the generalization your deployment actually demands.
A **homology-aware split** clusters proteins by sequence identity (say with MMseqs2) and keeps each cluster wholly in train or wholly in test, so the model must generalize to genuinely new families rather than recite close relatives.
A **temporal split** trains only on data released before a cutoff date and tests on what came after, mimicking the real task of predicting the future and defeating memorization of known answers.
A **scaffold split** groups small molecules by chemical core so the test set demands new chemotypes, not decorated copies.
**Leave-one-group-out cross-validation** holds out an entire cell type, gene, or assay to ask whether the model transfers to a context it never trained on.
And an **ancestry-aware split** holds out a genetic ancestry group, the check a polygenic score must pass before anyone deploys it (Chapter 13).
Each of these is a different question wearing the same word "accuracy," and the split you pick is the question you are actually asking.

<figure>
<img src="assets/figures/split-defines-question.svg" alt="A central dataset icon fans out to five split strategies, each paired with the deployment question it tests: homology-aware split to a new protein family, temporal split to future data, scaffold split to a new chemotype, leave-one-group-out to an unseen cell type or gene, and ancestry-aware split to a new population.">
<figcaption>The split is not a technicality, it is the question. Each strategy tests a different kind of generalization, so a benchmark's split silently defines what its number actually certifies.</figcaption>
</figure>

ProteinGym (Chapter 7), the standard variant-effect benchmark, makes the point concrete: for supervised evaluation it ships three cross-validation schemes — random, contiguous, and modulo — and the random one is explicitly the leaky one, because a mutated position can appear in both train and test so the model memorizes per-position effects [@notin2023].
The contiguous and modulo schemes keep positions disjoint, so they are harder and more honest, and a model's score drops when you move to them.
Same model, same data, different split, different truth.

!!! intuition "Intuition"
    A benchmark measures generalization only across the boundary its split draws; draw the boundary where your real deployment does not, and the number certifies a skill you will never use.

!!! collaborator "Collaborator"
    *A statistician asks: your model beats the baseline on AUROC — which metric did you preregister, and does it match the decision?* If the decision is "measure the top 50," the honest metric is precision or enrichment in the top 50, not a threshold-free average over every operating point. AUROC answers "can the model rank at all," which is rarely the question a wet-lab budget is asking, and under imbalance it is the most flattering summary available, which is exactly why it should not be the headline.

## Leakage, calibration, and statistics

If the split is the question, **data leakage** is the answer being whispered to the model during the exam.
Leakage is any path by which information from the test set reaches training, and it is the single most common reason a published number fails to reproduce in your hands [@bernett2024].
The subtle, biology-specific form is *homology leakage*: not the identical example in both sets, but a near-duplicate — a homolog, a related individual, a decorated scaffold — that the model recognizes and scores well without having generalized at all.
Genomics is especially prone to it because of the correlation structure the data carries everywhere, and the fix is to split along the natural units of that structure rather than at random [@whalen2022].
Co-folding and docking (Chapter 10) show the failure vividly: AI structure-and-affinity models can post excellent pose accuracy on a benchmark and yet be recalling protein–ligand complexes close to ones in training, so that when PoseBusters tested them on genuinely novel sequences and checked for physically valid geometry, several produced clashing atoms and strained bonds and failed to generalize, while a classical physics-based docker held up better [@buttenschoen2024].
The lesson is that a low error on a memorization-friendly split certifies memory, not skill, and a temporal or homology-aware split is what tells the difference.

<figure>
<img src="assets/figures/leakage-inflates-score.svg" alt="Two panels sharing a score axis. Left, a random split shows a homologous pair straddling the train and test sets connected by a dashed leak arrow, with a tall inflated score bar. Right, a homology-aware split keeps the cluster wholly on the train side, with a shorter honest score bar and a gap labeled leakage.">
<figcaption>The same model scored two ways: a random split lets a near-duplicate leak across the train/test line and lifts the number, while a homology-aware split removes the shortcut. The gap between the bars is the leakage, and it is the part that will not survive contact with new data.</figcaption>
</figure>

A second gap opens even on a clean split: a model can rank beautifully and still be miscalibrated.
**Calibration** is whether a model's numeric outputs can be read as reliable probabilities or values, not merely as a correct ordering.
Modern deep networks are, as a rule, overconfident — they assign 99% probabilities to predictions that are right far less than 99% of the time — a finding robust enough to be treated as a default expectation [@guo2017].
You diagnose it with a **reliability diagram**, which bins predictions by their claimed confidence and plots claimed against observed accuracy; a calibrated model hugs the diagonal, an overconfident one bows below it, and the average vertical gap is the expected calibration error.
Calibration matters the moment you need a fixed threshold rather than a within-list ranking: recall from property prediction (Chapter 7) that a variant-effect score's cutoff drifts from protein to protein, which is a calibration failure across contexts even when the ranking inside each protein is fine.
The reassuring part is that calibration is often cheap to repair — temperature scaling, a one-parameter rescale of the logits, fixes much of it, and because it is monotonic it leaves AUROC and Spearman untouched.
Fixing calibration and improving ranking are two separate jobs, and a benchmark that reports only one hides the other.

<figure>
<img src="assets/figures/calibration-reliability.svg" alt="A reliability diagram with predicted confidence on the x-axis and observed accuracy on the y-axis. A dashed diagonal marks perfect calibration. One curve bows well below the diagonal labeled overconfident, and a second curve after temperature scaling lies close to the diagonal, with the shaded gap labeled expected calibration error.">
<figcaption>Ranking and calibration are different virtues: the overconfident curve can still order candidates perfectly while its probabilities are wrong, and temperature scaling pulls it onto the diagonal without changing the ranking at all.</figcaption>
</figure>

Finally, the statistics a collaborator expects before they believe you.
A single point estimate — "0.72 Spearman" — is not a result, it is one draw from a distribution.
Report an **effect size** with a **confidence interval**, a range that would contain the true value in a stated fraction of repeated experiments, so the reader sees the uncertainty and not just the mean.
When you compare two models, compare them *paired* on the same assays and bootstrap a confidence interval on the difference, because a two-point gap on a noisy benchmark is often not significant.
And when you score many hypotheses at once — every gene, every variant, every assay — apply a **multiple testing correction** (Bonferroni for the strict familywise bound, Benjamini–Hochberg to control the false-discovery rate), the same discipline that gives GWAS its genome-wide significance threshold (Chapter 5); skip it and some of your "hits" are the inevitable tail of pure chance.

!!! warning "Common trap"
    Trusting a headline number without asking how the test set was built.
    A spectacular score on a random split of homologous proteins, related individuals, or shared scaffolds is measuring leakage, and a spectacular accuracy on a 1%-positive task with no confidence interval is measuring imbalance and luck.
    The number is only as trustworthy as the split and the statistics behind it, and neither is usually printed next to the headline.

!!! collaborator "Collaborator"
    *A statistician asks: you beat the prior model by two points — is that real?* Only if the interval says so.
    Bootstrap the per-assay differences and report the confidence interval on the gap, not two bare means; on a benchmark with a few dozen noisy assays a two-point lead frequently straddles zero.
    And confirm the two models were scored on identical splits with identical leakage controls, or you are comparing a memorizer to a generalizer and calling it progress.

## From leaderboard to your assay

Here is the disappointment the whole chapter has been preparing you for: a model that tops a public benchmark usually underperforms on your target, and often by a lot.
The reason is **distribution shift** (Chapter 15) — the benchmark's data and yours are drawn from different distributions, so skill on one does not carry to the other.
The shift hides in every dimension.
The benchmark's proteins may come from families yours does not resemble; its molecules may cluster in chemical space far from your series; its expression labels may come from cell lines while your assay runs on primary patient cells; and its measurements were taken on other instruments, in other batches, with other noise.
A leaderboard rewards average performance over *its* distribution, which is a weighted bet on which examples are common there, and your single target is one specific point that the average never promised to cover.

<figure>
<img src="assets/figures/benchmark-to-assay-shift.svg" alt="Two overlapping but offset distribution clouds labeled public benchmark and your assay, with a shifted mean. A bar chart beside them shows a tall public-benchmark score for the top model and a much shorter score for the same model evaluated on the user's assay, with an arrow marking the drop.">
<figcaption>Why the leaderboard rarely transfers: the public benchmark and your assay are different distributions, so the model's average skill over the former is a weighted bet that need not pay out on your one target. The honest number is the shorter bar, measured on your own data.</figcaption>
</figure>

The most instructive example lives in the regulatory lobe.
Sequence-to-function models (Chapter 12) top variant-effect leaderboards by predicting variation *across genes and tissues*, yet they explain variation *between individuals* at a single locus poorly, sometimes inverting the sign of a real cis-regulatory effect [@huang2023; @sasse2023].
Cross-gene skill and personal-genome skill are simply different tests, and a benchmark that scores the first says almost nothing about the second — precisely the question a population cohort asks.
The demographic version is just as sharp: a polygenic score can look accurate on a European-ancestry benchmark and lose much of its accuracy in another ancestry, because the correlation patterns and allele frequencies it learned do not transfer [@martin2019].
An evaluation that never splits by ancestry cannot see this, which is why the ancestry-aware split earned its place in the first section.

!!! collaborator "Collaborator"
    *A wet-lab partner asks: this model is state of the art — should we trust it on our program?* Trust it only after it survives your distribution.
    Carve out a small, clean, leakage-free held-out set from your own assay — a few dozen compounds or variants you have measured — and score the model there before you let it triage anything.
    A modest number on your data beats an impressive number on someone else's, because the second was never a promise about your target, and the cheapest way to learn that a model does not transfer is to check before you have spent the wet-lab budget acting on it.

The honest posture follows directly, and it is the through-line of the book's last act.
An in-silico score is a hypothesis, not a result (Chapters 9 and 10), and the leaderboard it came from certifies a distribution that is not yours.
So evaluate on the distribution you will deploy on: build your own small benchmark from your own measurements, split it to defeat the leakage your data structure invites, pick the metric that matches your decision, and report it with an interval.
That local, unglamorous evaluation is worth more than any public rank, and it is the measurement that tells you whether to enter the design–build–test loop (Chapter 17) — where the bench, not the benchmark, writes the final verdict.

!!! intuition "Intuition"
    A leaderboard tells you which model is best on average over someone else's world; only an evaluation on your own leakage-controlled data tells you which model is best for the one target that is actually yours.
