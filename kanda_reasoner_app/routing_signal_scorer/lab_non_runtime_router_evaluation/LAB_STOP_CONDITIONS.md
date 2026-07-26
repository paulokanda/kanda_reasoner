# LAB Stop Conditions

The LAB phase must stop immediately if any milestone attempts to introduce a forbidden behavior.

## Stop conditions for LAB-0

Stop if the patch adds any of the following inside the LAB box:

- `.py` implementation modules;
- schema code;
- fixture data;
- corpus data;
- runner logic;
- metrics logic;
- candidate harness logic;
- provider, embedding, vector, prompt-loader, persistence, activation, field-test, Pilot, or Copilot logic.

Stop if the patch makes production code import the LAB box.

Stop if the patch creates a route from LAB output to application runtime.

Stop if the patch claims ML router prompt logic reliability has already been tested.

Stop if the patch claims the LAB has fulfilled its mission.

Stop if the patch claims ML implementation may continue.

## Required recovery

If a stop condition occurs, revert to the last frozen state and create a separate governed repair milestone.
