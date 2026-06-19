# M27 - Auxiliar/Assistant Input Output Contract Design v1

M27 is design-only.

It defines the future input/output envelope for a possible later Auxiliar/Assistant human-review support step. It does not implement live input processing, live output generation, contract validation, review evidence building, observation transformation, route comparison, prompt loading, persistence, report writing, review queue writing, human decision recording, shadow-mode activation, Assistant/Auxiliar/Pilot/Copilot behavior; it does not activate shadow mode or Assistant behavior, candidate promotion, provider/model calls, embeddings, or runtime integration.

The contract is intentionally non-authoritative. Future outputs must only help a human reviewer understand already supplied evidence and must state that there is no routing effect, no prompt-loading effect, no persistence effect, and no Assistant activation effect.

M27 depends on frozen M18-M26. The next allowed milestone is M28: Auxiliar/Assistant Contract Validator Design v1.
