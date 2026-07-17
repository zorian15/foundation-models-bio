This is a working textbook about how foundation models — the same kind of large, pretrained models behind modern AI — are being used to read and design the molecules of life: proteins, genomes, and cells. It is written for someone who already knows machine learning — you can read a training loop, you know what an embedding is, you have used PyTorch or JAX — but who wants the current, load-bearing picture of what these models actually do in biology, and where they still break.

## What this book assumes

You are comfortable with the mechanics of training a neural network and with the idea of a pretrained model whose representations transfer to new tasks. You do not need a biology degree. Where a biological concept matters — what an assay measures, what a variant is, why a benchmark number does or does not answer your question — we teach it, in enough depth to reason correctly and no more. The machine learning is assumed and refreshed quickly (Chapter 3); the biology is the part we slow down for.

The goal is not encyclopedic coverage. It is the *load-bearing* set of ideas: the ones that come up when you nominate a drug target, score a genetic variant, design a protein, or sit across from a wet-lab collaborator who asks whether your model's prediction is worth an experiment.

## How it is organized

The book runs on one spine, chapter after chapter: the *problem*, the *models* that attack it, and *what is still hard*. That last part is not a formality — these models are genuinely useful and genuinely oversold, and telling the difference is the whole skill.

**Part I** builds the shared vocabulary: the landscape of problems, a machine-learning on-ramp, and the data and genetics you need. The problem chapters then split into two lobes. **Part II** is the molecular and therapeutic side — target discovery, property prediction, structure, design, and cell engineering. **Part III** is the genomic and regulatory side — predicting function from a stretch of DNA, and tracing a variant to a mechanism. **Part IV** is the bridge: multimodal models that reason across both lobes at once. **Part V**, "doing it for real," covers what a benchmark hides — messy data, honest evaluation, and closing the loop with the lab. **Part VI** looks at the frontier, and doubles as the conclusion.

Appendices hold the fields this edition leaves at the door — single-cell, spatial, and imaging models — plus a glossary, because the book crosses two jargon-dense worlds.

## How to read it

The callouts do specific jobs, and you can lean on them:

!!! intuition "Intuition"
    The one-sentence mental model. If you remember nothing else from a section, remember the intuition box.

!!! analogy "Analogy"
    A concrete comparison. Analogies are lies that fit in your head; each one leaks somewhere, and we say where.

!!! collaborator "Collaborator"
    A question a wet-lab partner or a skeptical statistician would put to you, and the crisp answer behind it.

!!! note "Note"
    A useful detail that would otherwise interrupt the flow.

!!! warning "Common trap"
    A place people reliably get it wrong.

Every jargon term is defined the first time it appears, and collected in the glossary at the back.

## A note on how this book is made

This is a folder of linked HTML files generated from Markdown by a small Python build. The table of contents lives in one file (`toc.py`); the prose lives in `content/`. A chapter that is not written yet renders as a navigable stub from its planned outline, so the whole book is always browsable. See `CLAUDE.md` for the authoring workflow.

Nothing here is final. It is a scaffold meant to be argued with, corrected, and filled in.
