#!/usr/bin/env bash
# Align chapter @cite keys with actual references.bib keys.
# Uses perl for reliable \b word-boundary matching across macOS / Linux.

set -euo pipefail
cd "$(dirname "$0")/.."

apply() {
  local from="$1" to="$2"
  for f in 0[1-9]-*.qmd 1[0-2]-*.qmd; do
    perl -i -pe "s/\@${from}\\b/\@${to}/g" "$f"
  done
}

apply anthropic_2025_extended       anthropic_2025_extended_thinking
apply bender_2021_stochastic        bender_2021_stochastic_parrots
apply bubeck_2023_sparks            bubeck_2023_sparks_agi
apply dwork_2014_dp                 dwork_2014_dp_foundations
apply eu_2024_aiact                 eu_2024_ai_act
apply fda_2024_pccp                 fda_2024_pccp_final
apply finlayson_2021_datasetshift   finlayson_2021_dataset_shift
apply greshake_2023_promptinjection greshake_2023_prompt_injection
apply kuhn2024tidymodels            kuhn_2022_tidymodels
apply mcp_2025_spec                 mcp_2025_specification
apply mollick_2024_15times          mollick_2024_15_times
apply mollick_2024_foursingularities mollick_2024_four_singularities
apply mollick_2024_goodenough       mollick_2024_good_enough_prompting
apply mollick_2024_latent           mollick_2024_latent_expertise
apply mollick_2024_thinkinglike     mollick_2024_thinking_like_ai
apply mollick_2025_cyberteammate    mollick_2025_cybernetic_teammate
apply mollick_2025_endsearch        mollick_2025_deep_research
apply mollick_2025_jagged           mollick_2025_jagged_agi
apply mollick_2025_jobinterview     mollick_2025_job_interview
apply mollick_2025_opinionated      mollick_2025_opinionated_guide
apply mollick_2025_persuasion       mollick_2025_personality_persuasion
apply mollick_2025_realagents       mollick_2025_real_agents
apply mollick_2026_dispatch         mollick_2026_claude_dispatch
apply mollick_2026_management       mollick_2026_management_superpower
apply obermeyer_2019_dissecting     obermeyer_2019_racial_bias
apply openai_2024_o1                openai_2024_o1_system_card
apply singhal_2023_medpalm          singhal_2023_med_palm
apply thirunavukarasu_2023_lmm      thirunavukarasu_2023_llms_medicine
apply tierney_2024_aiscribe         tierney_2024_ai_scribe
apply wei_2022_cot                  wei_2022_chain_of_thought
apply zheng_2023_llmjudge           zheng_2023_llm_judge

echo "Citation key alignment complete."
