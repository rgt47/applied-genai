# Applied Generative AI for Public Health and Biostatistics
*2026-04-26 11:45 PDT*

A graduate textbook on applied generative AI for
biostatisticians and public-health researchers, by Ronald
'Ryy' G. Thomas.

The book is the fourth in a graduate sequence on
biostatistical computing. The other three volumes:

- [*Statistical Computing in the Age of AI*](https://scai.rgtlab.org)
- [*Advanced Statistical Computing in the Age of AI*](https://scai-advanced.rgtlab.org)
- [*Biostatistics Practicum*](https://practicum.rgtlab.org)

This volume treats generative AI as the orthogonal axis: a
collaborator integrated across every stage of biostatistical
practice, with explicit attention to verification, the
jagged frontier, and the cybernetic-teammate framing.

## Structure

Twelve chapters in five parts:

1. **Foundations for the applied user.** Landscape;
   reasoning models, context, and verification.
2. **Working with biomedical knowledge and data.** RAG
   over biomedical corpora; synthetic data and privacy;
   multimodal medical AI.
3. **Agentic workflows and tool use.** Agents, tool use,
   and MCP; deep research and evidence synthesis.
4. **Evaluation, safety, and governance.** Evaluation
   beyond the benchmark; safety, bias, and red-teaming;
   regulation, privacy, and the IRB.
5. **Customisation, deployment, and practice.**
   Customisation and adoption; deploying AI in
   biostatistical practice.

## Build

Render the book locally with:

```bash
quarto render
```

Preview during writing:

```bash
quarto preview
```

PDF output requires a TeX installation; see Quarto's
documentation for setup.

## Companion documents

- `docs/syllabi-survey.md` — the curriculum survey across
  ~20 graduate-level genAI courses that shaped the
  chapter list, including the post-Mollick TOC revision.
- `docs/mollick-digest.md` — a 24-month digest of Ethan
  Mollick's *One Useful Thing* Substack used to test the
  TOC for contemporariness.
- `references.bib` — the working bibliography.

## License

Prose: CC BY-NC-ND 4.0. Code: CC0 1.0.
