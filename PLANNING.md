# Planning — *Foundation Models for Biology*

**Status: pre-scaffold planning doc.** Scope hashed out via `/grill` on 2026-07-16.
This is the handoff for (a) scaffolding the repo from the engine and (b) the first
drafting session. Nothing here is built yet.

## Identity

- **Working title:** *Foundation Models for Biology* (exact wording still open).
- **Repo / slug:** `foundation-models-bio` → `zorian15.github.io/foundation-models-bio/`.
- **Spine:** every problem chapter runs **problem → models that attempt it → what
  they do well + what's still hard**.
- **Audience:** an **ML practitioner learning the biology**. Assume neither side
  deeply, but the ML/foundation-model side gets one quick-but-adequate on-ramp,
  not book-1 depth; `../llm-textbook` is the "go deeper" pointer.
- **Depth invariant:** awareness-and-synthesis, **never PhD-in-the-weeds**. Favor
  adequate coverage over a tight word count — book 1's 800–1,600-word ceiling is
  relaxed here.
- **Shape:** one two-lobed journey — *molecular/therapeutic* and
  *genomic/regulatory* — bridged by a climactic multi-modal integration chapter.
  Motivated by two real job descriptions (protein/target-discovery/cell-engineering;
  and Calico's Borzoi sequence-to-function/gene-regulation/aging line).

## Structure (TOC)

- **I · Foundations (shared)**
  1. Intro — the synthesis premise (proteins and genomes as one story)
  2. Landscape of biological problems (the map; problems-first framing)
  3. On-ramp — modern ML & foundation models (quick but adequate)
  4. Primer — data & modalities: what each assay *measures*
  5. Primer — genetics for the ML practitioner (allele-frequency spectrum, GWAS,
     LD, heritability, confounding, association vs. causation)
- **II · Molecular & therapeutic problems** (each a problem→models→gaps unit)
  6. Target discovery
  7. Function & property prediction
  8. Protein structure determination
  9. Protein / binder design
  10. Cell engineering
- **III · Genomic & regulatory problems** (two problems, folded in as their own
  chapters — no third genomic chapter)
  11. Sequence → regulatory function (the Enformer/Borzoi line)
  12. From variant to mechanism (population cohorts, causal mapping; aging as the
      running example)
- **IV · Multi-modal integration** (climax — fuses proteins + regulation)
  13. Multi-modal integration
- **V · Doing it for real (shared)**
  14. The hard realities of biological data
  15. Evaluating models in biology
  16. Closing the loop with the lab
- **VI · Outlook**
  17. Outlook / open frontiers (flagged speculative)
- **Glossary** (auto-built; every jargon term/abbreviation defined on first use)

Out of scope for now, reserved as **future appendices** (structure must stay
extensible to add them): single-cell foundation models, spatial omics, cell
imaging / Cell Painting, mass-spec proteomics.

## The modality → model thread (researched 2026-07-16)

This is the "common thread": each data modality is produced by an assay and
ingested by an identifiable family of SOTA models. It drives Primer 4, the model
chapters, and much of `references.py`.

**Molecular / therapeutic lobe**

| Modality (assay) | Representative SOTA models |
|---|---|
| Amino-acid **sequence** (seq → UniRef, MGnify, BFD) | Protein LMs: ESM-2, ESM-3, ESM C, ProtT5, ProGen2/3, AMPLIFY |
| **3D structure** (X-ray, cryo-EM, NMR → PDB) | Structure: AlphaFold2/3, ESMFold, RoseTTAFold-AA, Boltz-1/2, Chai-1 · Design: RFdiffusion, ProteinMPNN, Chroma |
| **Variant fitness maps** (deep mutational scanning / MAVEs) | Zero-shot variant effect via PLMs; benchmark ProteinGym |
| **Binding affinity** (SPR/BLI/ITC) | Boltz-2 affinity head; design validation |
| **Small molecules** (SMILES / graph / 3D point cloud) | DiffDock, TargetDiff, Pocket2Mol; co-folding in AF3/Boltz/Chai |

**Genomic / regulatory lobe**

| Modality (assay) | Representative SOTA models |
|---|---|
| **DNA sequence** (reference genomes, 1000G, multispecies) | DNA LMs: DNABERT-2, Nucleotide Transformer, HyenaDNA, Caduceus, Evo / Evo 2 |
| **Functional tracks** — RNA-seq, CAGE, ATAC/DNase, ChIP-seq, Hi-C | Sequence-to-function: Enformer, Borzoi (Calico), Sei, AlphaGenome, Decima |
| **Population variation** — allele freqs (gnomAD), cohorts (UK Biobank, All of Us, FinnGen), GWAS summary stats | Variant effect: AlphaMissense, PrimateAI-3D, EVE, CADD; causal mapping via fine-mapping / coloc / MR |

**Integration bridge (the multi-modal thesis, concrete):** AlphaFold3 (protein +
nucleic acid + ligand + ion); Evo 2 (DNA + RNA + protein in one stream);
Perturb-seq models (State, GEARS, scGPT-perturb).

## What's still hard (honest "open frontier" hooks)

- **Personal / inter-individual variation.** Sequence-to-function models
  (Enformer/Borzoi) predict *cross-gene* variation well but explain
  *inter-individual* transcriptome variation poorly — sometimes wrong even in the
  direction of a cis-regulatory effect (Huang et al. 2023; Sasse et al. 2023, both
  *Nat. Genet.*). This sits directly under the Calico cohort application — frame it
  as an open frontier, not a solved problem. Prime Collaborator-box material.
- Noncoding/regulatory variant effect is far less solved than missense.
- "Foundation model" is used loosely in genomics: Enformer/Borzoi are supervised
  multi-*output* models, not self-supervised pretrained FMs. Be precise.

## Naming & scope corrections (bake these in)

- **Decima** is a **Genentech** model (gReLU/Borzoi lineage), *not* Calico.
- **AlphaGenome** is **DeepMind's** Enformer successor (2025 preprint → *Nature* 2026).
- **Evo 2** first author is **Brixi et al.** — "Nguyen et al." is Evo 1 (2024).
- **Borzoi** is genuinely **Calico / Kelley lab** — correct for the JD framing.

## Citation seed + verify-before-use

Research returned verified references (arXiv/DOI) for most models above — this
pre-seeds `references.py`. **Per the citation rule, verify each against the actual
paper before it lands.** Flagged as "from memory, re-verify": Boltz-1, ProGen3,
Evo 2 (bioRxiv suffix + *Nature* 2026 DOI), Genebass, Sasse-2023 DOI, TargetDiff
arXiv id. Do not commit any of these without opening the source.

## Book-specific conventions (beyond the inherited engine conventions)

- **Glossary on first use.** Every jargon term or abbreviation is defined inline
  the first time it appears and added to the glossary. Needs a build mechanism
  (there's a `build-glossary` skill) — decide at scaffold time whether the glossary
  is generated from inline definitions or a hand-maintained module like
  `references.py`.
- **"Collaborator" boxes** replace book 1's "Interview" boxes — what a wet-lab
  partner or a skeptical statistician/geneticist would ask (association vs.
  causation is rich here). Quizzes and all other callouts inherit unchanged. May
  mean repurposing/renaming the `interview` admonition in CSS/build.
- **Research SOTA before drafting; verify references.** (Now a general convention
  — see the shared authoring guide.)

## Open questions for scaffolding (not blocking)

- Exact title wording.
- Glossary mechanism (generated vs. hand-maintained module).
- "Collaborator" admonition: rename the type in CSS/build, or reuse `interview`
  with a new title?
- Stub the future-field appendices now (empty outlines) or omit until needed?
