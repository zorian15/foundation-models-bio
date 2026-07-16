A foundation model turns a biological sequence into a vector of *meaning*, learned by chewing through mountains of unlabeled sequence, and that representation transfers to tasks it was never explicitly trained for.
That single sentence is most of what you need to read the rest of this book.
This chapter is a fast refresher on the machine learning you probably already half-know, retooled for biology: what a representation is, the three model families you will keep meeting, and why pretraining then transferring works.
It assumes you can read a training loop and know what a gradient is, so we do not re-derive backpropagation.
For the mechanics of transformers in full, see the companion volume, *Foundations of Large Language Models*; here we take just enough to build the mental model the biology chapters lean on.

## Representations and transformers

Start with the object every model consumes: a **token**, one discrete unit of the input.
For a protein the natural token is an amino acid; for DNA it is a nucleotide, or a short **k-mer** or **byte-pair** chunk (a learned merge of frequent character runs, the same trick that tokenizes English).
The first thing the model does is look each token up in a table and replace it with an **embedding**, a learned vector of a few hundred to a few thousand numbers.
Training nudges those vectors so that biochemically or evolutionarily similar tokens land near each other, which is why an embedding space is more than a lookup: it is a geometry where distance means something.

A fixed embedding still gives every leucine the same vector no matter where it sits.
Biology does not work that way; a residue's role depends on its neighbors and its long-range partners.
**Attention**, the core operation of the **transformer** architecture [@vaswani2017], fixes this by letting each position read a weighted blend of every other position, so the vector for a residue becomes *context-aware*: the same amino acid in an active site and in a flexible loop end up with different representations.
Stack many attention layers and the model builds representations that quietly encode structure, conservation, and function, without ever being told those words.

<figure>
<img src="assets/figures/attention-context.svg" alt="A row of amino-acid tokens each map down to a vector; curved lines show attention blending the other positions into the center vector.">
<figcaption>A token becomes a vector, and attention blends the rest of the sequence into it, so a residue's representation reflects its context, not just its identity.</figcaption>
</figure>

Why does this transfer?
Because the pretraining task, predicting hidden or next tokens, is impossible to do well without internalizing the regularities that also govern the tasks you care about.
A model that reliably guesses a masked residue has, along the way, learned which substitutions evolution tolerates, and that knowledge is exactly what a stability or variant-effect task needs.

!!! intuition "Intuition"
    Attention turns a sequence into a set of context-aware vectors; pretraining shapes that space so that geometry encodes biology.

!!! collaborator "Collaborator"
    *A skeptical statistician asks: isn't an embedding just a fancy regression feature?* Yes, and that is the point. The difference is that the features are learned from billions of unlabeled sequences rather than hand-picked, so they capture higher-order dependencies a linear feature set would miss. You still fit a plain model on top, and you should still cross-validate it.

## The model families you will meet

Almost every biology model in this book is one of three families, distinguished by how they factor probability and therefore by what they are good at.

**Encoders** (masked language models, in the style of BERT) see the whole sequence at once and are trained to fill in hidden tokens from both sides.
Their output is a representation, one context-aware vector per token, so their job is understanding, not generation.
This is the family behind protein models like ESM-2 [@lin2023] and ESM C, and DNA models like Nucleotide Transformer and DNABERT-2.
Reach for an encoder when you want embeddings to feed a downstream predictor, or a per-site plausibility score.

**Autoregressive decoders** factor a sequence left to right, predicting each token from the ones before it.
That factorization makes them natural generators: sample a token, feed it back, repeat.
It also hands you a clean probability for any whole sequence, a measure of how "natural" it looks.
Protein generators like ProGen2 and the genome model Evo 2 [@brixi2026], trained on 9.3 trillion nucleotides across the tree of life, live here.
Reach for a decoder when you want to *make* new sequence or score whole-sequence likelihood.

**Diffusion models** learn to reverse a gradual noising process: start from noise and denoise, step by step, into a valid object.
In biology that object is usually 3D coordinates, atoms of a protein backbone or a small molecule, where left-to-right generation makes no sense but iterative refinement does.
AlphaFold3 pairs a transformer trunk with a diffusion head to predict all-atom structures of proteins with nucleic acids, ligands, and ions [@abramson2024], and RFdiffusion generates novel backbones for de novo design [@watson2023].
Reach for diffusion when the answer is a shape.

<figure>
<img src="assets/figures/model-families.svg" alt="Three labeled columns: Encoder (masked fill-in), Decoder (next-token), Diffusion (iterative denoise), each listing example models and what it is good for.">
<figcaption>Encoders represent, decoders generate sequence, diffusion builds 3D structure; the training objective, not the size, is what fixes each one's job.</figcaption>
</figure>

The boundaries blur in practice, and it helps to know where.
ESM-3 is a generative *masked* model that reasons jointly over sequence, structure, and function, so it does not fit the tidy encoder box.
AlphaFold3 is a transformer with a diffusion head.
The families are a map of objectives, not a taxonomy of products.

!!! collaborator "Collaborator"
    *A wet-lab partner asks: which model do I use to design a binder against my target?* Usually a pipeline, not one model. Diffusion (RFdiffusion) proposes a backbone that fits the target; an inverse-folding model (ProteinMPNN, Chapter 9) picks a sequence that will fold into that backbone; a structure predictor checks the design in silico before you order anything. No single family does the whole job.

## Pretraining, fine-tuning, zero-shot

The reason these models exist at all is **self-supervised pretraining**: you train on a task whose labels come free from the data itself.
Mask a residue and predict it; predict the next nucleotide.
No experiment, no annotation, just raw sequence, which is the one thing biology has in abundance, in UniProt and metagenomic and genome databases.
This is why a **foundation model**, a large model pretrained once on broad data, can then be pointed at many downstream tasks: the expensive learning already happened, off the labels you do not have.

You transfer that learning in three ways, in rough order of how much labeled data they need.
**Fine-tuning** adds a small task head and continues training the weights on your labeled set (thousands of examples might do).
A *linear probe* is the cheap cousin: freeze the model, fit a simple model on its frozen embeddings.
And **zero-shot** prediction asks the pretrained model directly, with no task-specific training at all.

The zero-shot trick you will meet constantly is scoring a mutation by likelihood.
To ask whether a variant is damaging, compare how probable the model finds the mutant residue versus the wild-type one at that site, the **log-likelihood ratio** log P(mutant) − log P(wild-type).
A large negative number says the model, having learned what evolution permits, finds the mutation surprising, which correlates with functional damage.
ESM-1v does exactly this and reaches roughly 0.5 Spearman correlation with deep mutational scans across dozens of proteins, matching older alignment-based methods with no per-protein training [@meier2021].
Evo 2 runs the same play one level down, scoring genomic variants by their likelihood under a genome model.

<figure>
<img src="assets/figures/pretrain-transfer.svg" alt="An unlabeled corpus feeds a foundation model, which branches to a fine-tune path needing labels and a zero-shot path that masks a site and scores mutant versus wild-type probability.">
<figcaption>Pretrain once on unlabeled sequence, then transfer: fine-tune when you have labels, or read effects straight off the model's likelihood when you do not.</figcaption>
</figure>

!!! intuition "Intuition"
    Zero-shot scoring reads a variant's effect off the model's surprise; "unlikely under evolution" is a decent proxy for "probably broken."

!!! warning "Common trap"
    High likelihood means "looks natural," not "good for my goal." A sequence the model finds plausible is one evolution might have produced, which is not the same as one that maximizes your engineered enzyme's turnover or binds your novel target. When you optimize for a specific objective, likelihood is a prior, not the fitness function, and the two can pull apart. Chapters 7 and 9 return to this gap.
