Audit the next prompts automatically and sequentially, one at a time.

For each prompt:

1. Open only that prompt as the primary audit target.
2. Inspect its canonical source, metadata, fingerprints, duplicate sources, generated artifacts, routing registrations, active references, validators, relevant Error Memory lessons, and current canonical owners.
3. Complete the full audit report.
4. Record its disposition, dependencies, unresolved conflicts, and exact fingerprints.
5. Formally close that prompt as the primary target.
6. Only after closing it, open the next prompt.
7. Continue automatically without waiting for me to say “go” between prompts.

Choose the batch size adaptively before beginning each cycle:

* Audit 3 prompts when the targets are large, governance-heavy, highly interconnected, startup-loaded, routing-related, freeze-related, Brick-Wall-related, patch-delivery-related, or dependent on many validators.
* Audit 5 prompts when the targets have normal size and complexity.
* Audit up to 8 prompts only when they are short, isolated, have clear ownership, and have few references, duplicates, generated artifacts, or validators.

Do not use a larger batch merely to move faster. Prefer the smaller batch whenever complexity is uncertain.

Maintain strict audit independence:

* Do not inspect the next prompt as a primary target before finishing the current report.
* Related prompts may be opened only as comparison evidence.
* Do not silently convert a related prompt into an additional audit target.
* Do not combine several prompts into one generalized assessment.
* Preserve a separate report, verdict, fingerprint record, dependency record, and stopping point for every prompt.

After each adaptive batch:

1. Produce a consolidated checkpoint.
2. Record all audited prompt IDs and filenames.
3. Record each keep, update, consolidate, deprecate, or delete recommendation.
4. Record newly discovered owner conflicts and cross-prompt dependencies.
5. Record prompts requiring focused verification before correction.
6. State whether the context remains reliable for another cycle.
7. State the exact next unopened prompt.

Continue without asking for confirmation unless:

* canonical source identity cannot be resolved;
* a required source file is unavailable;
* two sources appear equally authoritative and cannot be distinguished from available evidence;
* continuing would materially reduce assessment quality;
* the next prompt requires unavailable historical evidence;
* a safe conclusion would require modifying files;
* the accumulated context is no longer sufficient for an independent, detailed audit.

Do not modify source files, metadata, routing, generated artifacts, validators, Error Memory, freeze memory, or Project state during the audit phase.

Do not claim that validation passed unless the relevant validation was actually executed and evidenced.

When a cycle contains unusually large prompts, stop at the smaller safe boundary even when the nominal batch would allow more prompts.

Audit quality takes priority over batch size and speed.
