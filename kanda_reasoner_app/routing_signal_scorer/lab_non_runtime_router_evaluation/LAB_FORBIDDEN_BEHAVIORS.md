# LAB Forbidden Behaviors

The following behaviors are forbidden in LAB-0 and remain forbidden unless a later governed milestone explicitly authorizes a narrower safe form.

## Absolutely forbidden in LAB-0

- Creating Python lab implementation modules inside the LAB box.
- Creating schema code.
- Creating fixture files.
- Creating corpus files.
- Creating a runner.
- Creating a metrics engine.
- Creating a candidate harness.
- Creating provider adapters.
- Creating embedding or vector-store logic.
- Loading prompts.
- Reading live prompt-library content as runtime behavior.
- Mutating router canon.
- Mutating prompt library files outside the approved patch scope.
- Mutating freeze memory outside the normal local freeze workflow.
- Mutating gold registry or routing registry as runtime behavior.
- Persisting ML decisions.
- Writing review queues.
- Recording human approval automatically.
- Creating an activation key.
- Creating a maturity on/off switch.
- Creating field-test mode.
- Creating runtime Pilot behavior.
- Creating Copilot behavior.
- Adding batch mode.
- Adding provider calls.
- Adding network calls.
- Adding subprocess-driven model execution.
- Adding PySide6/UI integration for the lab.

## Dangerous misroutes

If the user says `next`, `go`, or `continue` after RG-LAB-000, the system must not interpret that as direct ML implementation.

The safe route is LAB-0 first, then frozen documentation gates, then later lab implementation only after explicit governed milestones.
