# ML Advisory Signal Phase 1a Threat Model v1

Feature: Routing Signal Scorer ML Advisory-Signal and Governed Prompt
Intake Boundary Contract v1

Threats controlled in Phase 1a:

- ML advisory output becoming a route decision.
- Advisory fields implying winners, rankings, selected routes, or final
  prompts.
- Free-text advisory explanations smuggling route authority.
- Provider, embedding, vector-store, network, subprocess, file-write, or
  persistence capability entering the boundary.
- Prompt library, router canon, or freeze memory being read by the advisory
  layer.
- Manual prompt codes being treated as commands instead of classification
  hints.
- New prompts bypassing governed prompt intake, validation, and freeze.

Phase 1a response:

- Use frozen dataclass contracts and enum reason codes.
- Use NullAdvisor and deterministic MockAdvisor only.
- Validate output through an egress firewall.
- Reject authority-like field names and authority-like text tokens.
- Keep Prompt Intake as the only safe door for new prompts.
- Keep manual prompt codes as removable references, not route commands.

Non-goals:

- No real ML.
- No MLRT-113.
- No runtime shadow mode.
- No router final-selection modification.
