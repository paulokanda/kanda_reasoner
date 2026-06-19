# Problem-Set Roadmap Solver

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.1
Status: Optional problem-set roadmap prompt
Use: When the user gives multiple Reasoner problems and asks for the best solving order.

Workflow:
1. Identify each problem.
2. Map each problem to its owner box.
3. Identify dependencies.
4. Identify risk.
5. Identify which problems can be bundled safely.
6. Identify which must remain separate.
7. Produce a numbered roadmap.
8. Warn if the set contains complex updates.
9. Request required prompts before implementation.
10. Request current files if needed.

Bundling rule:
Bundle only when problems share the same owner box, validation path, and risk
surface. Do not bundle unrelated GUI, schema, retrieval, prompt, runtime, and
governance changes.

Output format:
Roadmap:
1. <problem or bundle>
   - owner box:
   - risk:
   - standalone or bundled:
   - reason:
   - validation:

2. <problem or bundle>
   - owner box:
   - risk:
   - standalone or bundled:
   - reason:
   - validation:

Before implementation:
- Say which prompt files are needed.
- Request source ZIP/logs if needed.
- Do not implement until the user approves the roadmap for complex work.

Delivery:
- One focused bundle per approved step.
- Direct ZIP with final project-relative paths.
- _bundle_temp manifest for source/runtime bundles.
- No install script.
- Wait for validation before next step.
