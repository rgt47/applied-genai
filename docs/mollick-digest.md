# Mollick *One Useful Thing* Digest
*2026-07-25 09:00 PDT*

This document is the master digest of Ethan Mollick's *One Useful
Thing* Substack as it bears on *Applied Generative AI for Health
Sciences Research*. It is referenced from the preface as the
contemporary touchstone against which the chapter list was tested. The
digest is maintained by `scripts/mollick_refresh.py`, which pages the
Substack archive, maps each new post to a chapter, assesses its
chapter-affecting impact, appends BibTeX entries, and updates this
file. This checked-in version records the essays the book currently
draws on; running the refresh script re-establishes the live cutoff and
adds any posts published since.

A note on scope: the essays below are practitioner commentary, not
peer-reviewed sources. The book cites them for framing and for the
vocabulary that has become standard in applied practice (the *jagged
frontier*, the *cybernetic teammate*, working *with wizards*), and
anchors its technical claims in the peer-reviewed literature.

## The load-bearing ideas

Three of Mollick's framings thread through the book and earn the
'applied' orientation.

- **The jagged frontier.** Capability is uneven and its edge is
  opaque; capability and the difficulty of verifying it rise together.
  See *On Jagged AGI* and *The Shape of AI*.
- **The cybernetic teammate.** AI assistance is more fruitfully framed
  as collaboration with a teammate than as operation of a tool; the
  binding skill shifts from prompting to management. See *The
  Cybernetic Teammate* and *Management as AI Superpower*.
- **Verification under opacity.** As models grow more capable and less
  inspectable, the researcher's contribution becomes the design of
  proportionate verification. See *On Working with Wizards*.

## Post-by-post

Grouped by year. Bibliography keys are given for cross-reference; full
citations are in `references.bib`.

### 2023

- *How to Use AI to Do Stuff: An Opinionated Guide*
  [`mollick_2023_how_to_use_ai`]. Entry-level orientation to practical
  use.

### 2024

- *Something New: On OpenAI's 'Strawberry' and Reasoning*
  [`mollick_2024_strawberry_reasoning`]. Early framing of reasoning
  models; relevant to Chapter 3.
- *When You Give a Claude a Mouse* [`mollick_2024_claude_mouse`].
  Computer-use agents; relevant to Chapter 8.
- *Thinking Like an AI* [`mollick_2024_thinking_like_ai`].
- *Getting Started with AI: Good Enough Prompting*
  [`mollick_2024_good_enough_prompting`]. Relevant to Chapter 3.
- *What Just Happened* [`mollick_2024_what_just_happened`].
- *15 Times to Use AI, and 5 Not To* [`mollick_2024_15_times`].
- *On Speaking to AI* [`mollick_2024_speaking_to_ai`].
- *Four Singularities for Research* [`mollick_2024_four_singularities`].
- *Latent Expertise: Everyone Is in R&D*
  [`mollick_2024_latent_expertise`]. Adoption; relevant to Chapter 13.
- *Captain's Log: The Irreducible Weirdness of Prompting AIs*
  [`mollick_2024_captains_log`].

### 2025

- *The End of Search, the Beginning of Research*
  [`mollick_2025_deep_research`]. Deep research; relevant to Chapter 9.
- *Prophecies of the Flood* [`mollick_2025_prophecies_flood`].
- *The Cybernetic Teammate* [`mollick_2025_cybernetic_teammate`]. The
  RCT on AI-augmented teams; relevant to Chapter 13.
- *No Elephants: Breakthroughs in Image Generation*
  [`mollick_2025_no_elephants`]. Relevant to Chapter 7.
- *On Jagged AGI: o3, Gemini 2.5, and Everything After*
  [`mollick_2025_jagged_agi`]. Relevant to Chapters 2 and 3.
- *Personality and Persuasion* [`mollick_2025_personality_persuasion`].
  Relevant to Chapter 11.
- *GPT-5: It Just Does Stuff* [`mollick_2025_gpt5_just_does`].
- *Mass Intelligence* [`mollick_2025_mass_intelligence`].
- *On Working with Wizards* [`mollick_2025_wizards`]. Competence and
  opacity rise together; relevant to Chapter 3.
- *Real AI Agents and Real Work* [`mollick_2025_real_agents`]. Relevant
  to Chapter 8.
- *An Opinionated Guide to Using AI Right Now*
  [`mollick_2025_opinionated_guide`].
- *Giving Your AI a Job Interview* [`mollick_2025_job_interview`].
  Evaluation; relevant to Chapter 10.
- *The Shape of AI: Jaggedness, Bottlenecks and Salients*
  [`mollick_2025_shape_of_ai`]. Relevant to Chapter 2.

### 2026

- *Claude Code and What Comes Next* [`mollick_2026_claude_code`].
  Agentic coding; relevant to Chapters 4 and 8.
- *Management as AI Superpower* [`mollick_2026_management_superpower`].
  The manager mindset; relevant to Chapter 8.
- *The Shape of the Thing* [`mollick_2026_shape_of_thing`].
- *Claude Dispatch and the Power of Interfaces*
  [`mollick_2026_claude_dispatch`]. Interfaces over raw capability;
  relevant to Chapter 14.
- *Sign of the Future: GPT-5.5* [`mollick_2026_gpt55`].

## Maintenance

To refresh: `python scripts/mollick_refresh.py`. The script determines
its cutoff from the most recent dated entry recorded in this file and
processes only posts published after it; with no dated entry present it
falls back to a conservative default and rebuilds from there. See the
script header for the required environment variables.
