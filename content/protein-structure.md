A protein is a chain of amino acids that folds into one specific three-dimensional shape, and that shape is most of what determines what the protein does. For fifty years, learning the shape meant running a hard, slow experiment. The load-bearing idea of this chapter is that the folded coordinates are, to a startling degree, predictable from the sequence alone, because evolution leaves a statistical fingerprint of which residues sit next to each other in space. Modern predictors read that fingerprint and return atomic coordinates in seconds instead of months. But a predicted structure is a single snapshot, and a snapshot is not the whole biology. The temptation, after 2021, is to say structure is "solved." It is not. It is *predicted* well for many proteins, which is a different and more useful claim.

## The problem: from sequence to 3D

The sequence of a protein is one-dimensional: a string over an alphabet of twenty amino acids, which you met in the genetics primer (Chapter 5). The function lives in three dimensions. Two residues far apart in the string can be neighbors in the folded shape, forming the pocket that binds a drug or the cleft that cuts a bond. Going from the string to the coordinates is the *protein folding problem*, and for most of its history the only reliable route was experiment.

Those experiments are the ground truth, and they are expensive. **X-ray crystallography** (measuring how a crystal of the protein diffracts X-rays) can resolve atoms sharply but first demands that the protein crystallize, which many proteins simply refuse to do. **Cryo-electron microscopy**, or **cryo-EM** (imaging flash-frozen molecules with an electron beam), skips crystals and now handles large machines and membrane proteins, and it has grown to roughly a third of new depositions. Both feed the **Protein Data Bank (PDB)**, the open archive of experimentally determined structures introduced in the data chapter (Chapter 4) [@berman2000]. The PDB holds on the order of 200,000 structures, which sounds like plenty until you compare it with the hundreds of millions of known sequences. That gap is the whole opportunity.

What makes prediction possible is **co-evolution**. Line up many evolutionary relatives of a protein into a **multiple sequence alignment (MSA)** (a stack of homologous sequences, one per row, with corresponding positions in columns; a **homolog** is a related sequence from another species or gene copy). If two positions are in physical contact, a mutation at one that would disrupt the pair tends to be compensated by a mutation at the other. Across enough relatives, those two columns *change together*. Contact leaves a correlation, and correlation is something a model can learn to read.

<figure>
<img src="assets/figures/coevolution-signal.svg" alt="A multiple sequence alignment with two highlighted columns whose residues vary together, and an arrow to a folded chain where those two positions touch in space.">
<figcaption>Positions that touch in the folded structure co-vary across evolution: the signal that lets a model recover 3D contacts from a stack of related sequences.</figcaption>
</figure>

!!! intuition "Intuition"
    A structure predictor is a decoder for a code evolution already wrote: which columns of an alignment vary in lockstep tells you which residues are neighbors in space.

!!! collaborator "Collaborator"
    *"If it just needs an alignment, what happens to a protein with no known relatives?"* The co-evolution signal weakens, and MSA-based accuracy drops. Orphan proteins, fast-evolving viral proteins, and designed sequences are exactly where you should distrust a confident-looking prediction, and where single-sequence models (below) become interesting rather than merely faster.

## Models that attempt it

The breakthrough was **AlphaFold2** [@jumper2021]. Its input is an MSA plus any known template structures; its network reasons jointly over the alignment and a map of pairwise residue relationships, then folds that into coordinates. At **CASP14** in 2020, the biennial blind competition where predictors get sequences whose structures are withheld, AlphaFold2 reached accuracy competitive with experiment for a large fraction of targets. That result is what reset the field. It also ships a calibrated confidence score, **pLDDT**, per residue, and low pLDDT is your first warning that a region is unreliable or disordered.

AlphaFold2 predicts a single protein chain (a **monomer**). Real biology is assemblies: proteins bound to other proteins, to DNA and RNA, to small-molecule **ligands** and metal ions. **AlphaFold3** [@abramson2024] rebuilds the output end as a **diffusion model** (a generator that starts from noise and iteratively denoises toward a structure, the same family you will meet again in protein design, Chapter 9). Working at the level of individual atoms rather than only amino-acid residues lets one unified network predict **complexes**: protein–ligand, protein–nucleic-acid, ion-bound. It beats specialized docking tools at their own tasks. **RoseTTAFold All-Atom** [@krishna2024] reaches the same generality by a different route, mixing a residue-level representation for the protein backbone with an atom-level one for everything else.

A second axis is how much evolutionary context the model demands. **ESMFold** [@lin2023] drops the MSA entirely: it reads structure off the internal representations of **ESM-2**, a **protein language model (PLM)** trained on tens of millions of raw sequences (roughly 65 million unique UniRef sequences) (the PLM idea from Chapter 4). One sequence in, coordinates out. It trades some accuracy on hard targets for a large speedup and no alignment step, which makes it the tool of choice for scanning millions of sequences or for proteins with no relatives to align.

The 2024–2026 shift is that AlphaFold3-class capability is no longer a single lab's. Open-weight **co-folding** models (predicting the joint structure of a complex, sequence and ligand folded together) now match it closely: **Boltz-1 (MIT) and Boltz-2 (MIT and Recursion)** [@wohlwend2024] and **Chai-1** from Chai Discovery both reproduce AlphaFold3-level accuracy under open licenses, and Boltz-2 adds a binding-affinity head that topped the CASP16 affinity challenge. For an ML practitioner, this matters: you can run and fine-tune these yourself.

<figure>
<img src="assets/figures/structure-model-families.svg" alt="Three model families side by side: MSA-based AlphaFold2, single-sequence ESMFold, and all-atom diffusion co-folders AlphaFold3, Boltz, and Chai, with their inputs above and output scope below.">
<figcaption>Two axes organize the field: how much evolutionary context the model needs (MSA versus a single sequence) and what it can model (a lone chain versus a full complex with ligands and ions).</figcaption>
</figure>

!!! collaborator "Collaborator"
    *"Which one should my lab actually run?"* If you have relatives and want the single best monomer, AlphaFold2 is still a strong default. If you need a complex with a ligand, nucleic acid, or ion, reach for an all-atom co-folder (AlphaFold3, Boltz, Chai, or RoseTTAFold All-Atom). If you are screening millions of orphan sequences or want it fully in-house, ESMFold or an open co-folder wins on speed and control.

!!! note "Note"
    Do not read a benchmark headline as a promise about *your* protein. CASP scores are averages over a target set; a model near the top can still be wrong on a specific membrane protein, a large assembly, or a region with few homologs. Always check the per-residue confidence.

## What they do well and what is still hard

Be precise about the win. For a single, well-behaved protein with plenty of evolutionary relatives, these models return a fold that is often as good as an experimental one, in seconds, for free. That genuinely changes how biology gets done. The honest boundary of the win is just as important.

The deepest limitation is that the models return **one static structure**, and a protein is not one shape. Most proteins flex between multiple functional states, an open and a closed form, a bound and an unbound one, and the biology often lives in the *motion*, not any single frame. AlphaFold was trained to predict the single most probable structure, so it collapses a **conformational ensemble** (the population of shapes a molecule actually visits) down to its dominant mode [@jing2024]. Active work now coaxes ensembles out of these networks, by injecting experimental data or by pairing the predictor with flow-matching generators, but returning a faithful *distribution* of states rather than a point estimate remains open.

<figure>
<img src="assets/figures/static-vs-ensemble.svg" alt="On the left a single predicted backbone labeled one state; on the right several overlaid backbones in different conformations plus a wavy disordered tail, labeled an ensemble.">
<figcaption>The predictor returns the single most likely fold; the molecule visits a population of states and may leave whole regions disordered. The gap between them is where much of function hides.</figcaption>
</figure>

Related failure modes cluster here. **Intrinsically disordered regions (IDRs)**, stretches that have no fixed fold at all and stay floppy in the cell, are common and functional, and a model that outputs coordinates will draw *some* shape anyway, flagged only by low confidence. Large multi-component **assemblies** stress the models more than single chains. And a prediction that depends on a strong MSA degrades exactly where relatives are scarce.

!!! warning "Common trap"
    A confident-looking ribbon diagram is not the same as understanding function. The model gives you coordinates; it does not tell you which pocket is the active site, how tightly a drug binds, or how the shape changes when it does its job. Structure is an input to those questions, not an answer to them. Binding affinity and function are separate prediction problems (property prediction, Chapter 7; design, Chapter 9).

!!! collaborator "Collaborator"
    *"So can I skip the experiment now?"* For a first pass, often yes, and that saves real time. But when the answer must be right, a mechanism claim, a drug program, a novel fold with no close relatives, you still validate against experiment. The models are a powerful prior over structure, not a replacement for measuring it.

The mental model to carry forward: sequence-to-structure went from a grand-challenge problem to a fast, reliable *first draft* for most proteins. The frontier moved to what a single frame cannot express: dynamics, ensembles, disorder, and the leap from a shape to the function that shape performs.
