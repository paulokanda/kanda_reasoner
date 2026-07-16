Next milestone should be design-only:

routing_signal_scorer_v2_similarity_design

Purpose:

Define whether similarity scoring is safe and useful before adding TF-IDF, embeddings, or any fuzzy matching runtime.

Recommended scope:

1. No code that changes runtime routing.
2. No real ML dependency.
3. No embeddings.
4. No self-learning.
5. No router override.
6. No May proceed now decision.
7. Only a design/spec/test-plan artifact.

The next safe patch would add a small
design document and tests that verify
the design rules are present. 
It should not modify the scorer behavior yet.
Diagnostic, manual-pilot, 
and advisory freezes are already closed and clean;
diagnostic and manual-pilot freeze logs also show 
LOCAL FREEZE WRITE OK, used hint marking, AI-send refresh, 
startup context refresh, and FREEZE_MEMORY_STATUS: OK.