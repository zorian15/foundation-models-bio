Every model in this book learns from a surprisingly short menu of experiments. A protein language model reads amino-acid strings; AlphaFold reads sequence and writes coordinates; a regulatory-genome model reads DNA and writes a stack of signal tracks. Before any architecture makes sense, you need to know what each experiment actually measures, what its numbers mean, and whether a given readout is something the model *reads in* or something it is asked to *predict*. This chapter is the data primer: it defines the load-bearing assays and, at the end, threads each one to the model that consumes it. Keep the genetics primer (Chapter 5) nearby, since several of these readouts only make sense against the biology it covers.

## Sequence, structure, and fitness

Start with the three faces of a single molecule, ordered by how much data exists for each.

**Sequence is abundant and cheap.** A protein is a string over a 20-letter alphabet (the amino acids); a genome is a string over a 4-letter alphabet (the DNA bases A, C, G, T). UniProt, the reference database of known protein sequences, holds hundreds of millions of entries, and the clustered version (UniRef) is what protein language models such as ESM-2 train on. On the DNA side, a *reference genome* is one agreed-upon consensus sequence for a species (GRCh38 is the current human build), against which everyone else's genome is described as a set of differences. Sequence is the substrate: it is nearly free to read, so there is enough of it to pretrain large models by self-supervision (Chapter 3).

**Structure is precious and scarce.** The 3D shape a protein folds into is measured, atom by atom, by X-ray crystallography (shining X-rays through a crystallized protein and inferring atom positions from the diffraction pattern) or cryo-electron microscopy (cryo-EM, imaging flash-frozen molecules with an electron beam). These structures are deposited in the Protein Data Bank (PDB), which holds well over 230,000 entries. That sounds like a lot until you compare it to the hundreds of millions of known sequences: structure is orders of magnitude rarer because each one is slow and expensive to solve. That scarcity is the whole reason AlphaFold matters, and we return to it in the structure chapter (Chapter 8).

**Fitness is the label for "does this variant work?"** Deep mutational scanning (DMS) is the workhorse here: you build a library containing many mutant versions of a protein, put them all under a selection pressure (say, bind a target or survive), and then sequence the surviving pool. A variant that got more common was beneficial or tolerated; one that vanished was deleterious. The result is a *fitness map*, an effect score for potentially every single-amino-acid substitution in the protein. ProteinGym, the standard benchmark, aggregates over 2.5 million such measurements across 217 substitution assays [@notin2023]. When you read "the model predicts variant effects," DMS data is usually the ground truth it is scored against, a thread we pick up in property prediction (Chapter 7).

<figure>
<img src="assets/figures/sequence-structure-fitness.svg" alt="Three panels for one protein: a one-dimensional amino-acid string labeled abundant, a three-dimensional folded shape labeled scarce, and a grid of mutation-by-position effect scores labeled the label.">
<figcaption>One molecule, three data types, three very different supplies. The model's task is often to buy the scarce view (structure, fitness) with the cheap one (sequence).</figcaption>
</figure>

!!! intuition "Intuition"
    Sequence is the input almost everywhere; structure and fitness are the expensive answers we wish we could read off the sequence directly.

## Reading the regulatory genome

Only about 2% of the human genome codes for protein. The rest includes the regulatory machinery that decides *when and where* each gene turns on, and a different family of assays reads it out. Each one measures a specific physical quantity along the genome, and confusing them is the most common beginner mistake.

- **RNA-seq** measures transcript abundance: how many RNA copies of each gene are present in a sample, which is the standard proxy for how strongly that gene is expressed. Its single-cell version, scRNA-seq, gives you that expression profile *per individual cell* rather than averaged over a tissue.
- **ATAC-seq** and **DNase-seq** measure chromatin accessibility: which stretches of DNA are physically open and reachable rather than wound up tight. Open regions are where regulatory proteins can dock, so accessibility marks candidate regulatory elements.
- **ChIP-seq** measures protein-DNA binding: it pulls down a specific protein along with the DNA it was gripping, then sequences that DNA to map where a particular transcription factor binds, or where a given histone modification (a chemical mark on the DNA-packaging proteins) sits.
- **CAGE** measures transcription start site (TSS) activity: it captures the exact base where transcription begins and how much starts there, sharpening the fuzzy "expression" signal into a precise on-switch location.
- **Hi-C** measures 3D contacts: which far-apart stretches of DNA physically touch when the genome folds inside the nucleus, revealing that an enhancer megabases away can loop over to control a gene.

The unifying output form is a *coverage track*: a number for (almost) every position along the genome, one track per experiment per cell type. Large public consortia produced these at scale, and their names recur throughout the book: ENCODE and FANTOM5 for regulatory tracks, GTEx for tissue-level RNA-seq, and 4D Nucleome for Hi-C. One more assay to know is the massively parallel reporter assay (MPRA), which measures the enhancer activity of thousands of short synthetic DNA snippets at once by wiring each to a readout gene, giving a designed, causal test rather than an observation of the natural genome.

<figure>
<img src="assets/figures/regulatory-tracks.svg" alt="A shared horizontal genome axis with four stacked signal lanes above it: RNA-seq peaks over a gene body, ATAC peaks at open regions, ChIP-seq peaks at a binding site, and CAGE a sharp spike at the transcription start, plus a small triangular contact map for Hi-C.">
<figcaption>Five assays, five different physical questions asked of the same stretch of DNA. Each becomes a coverage track along the genome; together they are the regulatory readout a sequence model tries to reproduce.</figcaption>
</figure>

!!! collaborator "Collaborator"
    *"RNA-seq gives me one expression number per gene. Why does the model predict a whole wiggly track instead?"* Because position matters. A coverage track keeps the shape of the signal across the locus, so the model can learn splicing, alternative start sites, and where within a gene the signal concentrates, all of which a single per-gene number throws away. Borzoi predicts RNA-seq coverage at fine 32-bp resolution to recover that structure [@linder2025].

## From assay to training signal

Now make the thread explicit, because the same assay plays opposite roles in different models. The organizing question is always: *is this readout an input the model reads, or a target it predicts?*

- **DNA sequence in, regulatory tracks out.** Enformer takes a long DNA window and predicts thousands of tracks at once (CAGE, ATAC/DNase, ChIP-seq) [@avsec2021]; its successor Borzoi adds fine-grained RNA-seq coverage at 32-bp resolution, four times sharper than Enformer, as a target [@linder2025]. The sequence is the input; every assay from the previous section is a *label*. We devote the sequence-to-function chapter (Chapter 11) to this family.
- **Amino-acid sequence in, structure out.** AlphaFold2 reads a protein sequence (with an alignment of its evolutionary relatives) and predicts atomic coordinates, trained against the PDB [@jumper2021]; AlphaFold3 extends this to complexes of proteins, nucleic acids, and small molecules [@abramson2024]. Here structure is the target the model buys with cheap sequence.
- **Sequence in, fitness out.** A protein language model trained only to predict masked amino acids assigns a likelihood to any variant; that likelihood, with no labels at all, correlates with the DMS fitness maps in ProteinGym [@notin2023]. The assay is not an input here either; it is the held-out yardstick.

The lesson is that a modality is not intrinsically "input" or "output." RNA-seq is a *target* for Borzoi but could be a model's *input* elsewhere (say, to predict cell type). What fixes the role is the modeling question, not the assay. When you meet a new model, the first thing to pin down is which readouts flow in and which it is graded on, a habit that pays off again in evaluation (Chapter 15) and when the data gets messy (Chapter 14).

<figure>
<img src="assets/figures/assay-to-signal.svg" alt="Three input-arrow-model-arrow-output rows: DNA sequence into Enformer or Borzoi out to regulatory tracks; amino-acid sequence into AlphaFold or ESMFold out to 3D structure; sequence plus variant into a protein language model out to a fitness score.">
<figcaption>The same short menu of assays, wired three ways. Reading the arrows tells you what each model actually learned, and what it was allowed to see.</figcaption>
</figure>

!!! collaborator "Collaborator"
    *"You said Enformer predicts expression well. Will it tell me why my patient's expression differs from the reference?"* Be careful. These models predict variation *across genes* impressively, but they explain *inter-individual* variation, the differences between two people's genomes, poorly, and often get even the direction of a variant's effect wrong [@huang2023]. Cross-gene skill and personal-genome skill are different tests; the field passes the first far better than the second, an open problem we revisit in variant-to-mechanism (Chapter 12).

!!! warning "Common trap"
    Chromatin accessibility (ATAC) is not expression (RNA-seq). Open DNA marks where regulation *can* happen; transcript counts measure what *did* happen. A region can be accessible and silent, or an enhancer can loop in from far away, so treating one as a stand-in for the other will mislead you.
