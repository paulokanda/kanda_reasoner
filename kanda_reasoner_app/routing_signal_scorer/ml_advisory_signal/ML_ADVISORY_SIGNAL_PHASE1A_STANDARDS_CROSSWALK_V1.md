# ML Advisory Signal Phase 1a Standards Crosswalk v1

This file maps the Phase 1a implementation to the project guide.

Guide requirement: isolated ml_advisory_signal subbox.
Implementation: this package is isolated from runtime router authority.

Guide requirement: frozen dataclass contracts.
Implementation: AdvisoryInput, AdvisoryGroupObservation, and
AdvisoryOutput are frozen dataclasses.

Guide requirement: AdvisorProtocol, NullAdvisor, and deterministic
MockAdvisor.
Implementation: advisor_interface.py, null_advisor.py, and mock_advisor.py.

Guide requirement: output and egress firewall.
Implementation: output_firewall.py rejects authority-like field names,
generic dictionaries, mutable lists, and authority-like text tokens.

Guide requirement: no provider, embedding, persistence, prompt loading,
freeze-memory, router-canon, or prompt-library access.
Implementation: tests inspect imports and capability tokens.

Guide requirement: no advisory rankings or free-text explanations.
Implementation: forbidden field names and tests reject rankings,
advisory_explanation, explanation, notes, and free_text.

Guide requirement: ML is advisory, not pilot.
Implementation: no function returns or accepts final route authority.
