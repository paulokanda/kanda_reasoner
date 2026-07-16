# 0000 PROMPT SUBSTITUTION MAP REASONER v1.1

Version: 1.1
Status: Prompt substitution map for Project Reasoner

Install location:
_project_reference\PROMPTS\

New prompts and substitutions:

1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
   Substitutes:
   - 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.0.md

2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md
   Substitutes:
   - 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.2.md
   - 0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md
   - 0000 6 HOW SEND FILES UPDATED.md

3. 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
   Substitutes:
   - 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.3.md
   - 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md

4. 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
   Substitutes:
   - 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.1.md
   - 0000 2.0 PYARCHITECT DAILY REASONER CANON STARTUP PROMPT V14.0.md

5. 0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md
   Substitutes:
   - 0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
   - 0000 3.5 KANDA REASONER PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md

6. 0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md
   Substitutes:
   - 0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.2.md
   - 0000 4.10 ACTIVE PROJECT REASONER GOVERNANCE RUN AT END OF CHAT.md

7. 0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
   Substitutes:
   - 0000 5.6 REASONER LARGE MODULE REFACTOR AND SOURCE-PRESERVING FACADE PROTOCOL v5.6.md
   - 0000 5 1b HOW REFACTOR LARGE MODULE 14.5.26_claude.md
   - 0000 6 best techinic to split giant files.md

8. 0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
   Substitutes:
   - 0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

9. 0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md
   Substitutes:
   - 0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.0.md
   - 0000 7 SOLVE A SET OF PROBLEMS.28.06.2026.md

Removed from active stack:
- 0000 6.1 REASONER CHECKPOINT ZIP PROTOCOL v1.0.md
  Reason: checkpoint guidance is now optional backup guidance inside the delivery
  and refactor protocols. It is not a daily prompt.

Key delivery changes in v1.1:
- No normal prompt/source update uses a install script.
- No normal prompt/source update requires a separate backup-script folder.
- Files are created or updated in the AI sandbox and delivered as a ZIP with final
  project-relative folders.
- Runtime/source BUNDLE_MANIFEST files go inside _bundle_temp.
- the older Reasoner-specific manifest folder is no longer the active source-bundle
  manifest folder.
- Governance-only ZIPs still use _project_reference\ACTIVE_PROJECT_ GOVERNANCE.
