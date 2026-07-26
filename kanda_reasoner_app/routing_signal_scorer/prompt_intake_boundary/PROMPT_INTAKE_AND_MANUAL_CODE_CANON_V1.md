# Prompt Intake and Manual Code Canon v1

Prompt Intake handles future prompt proposal, classification, duplicate
review, boundary review, testing, validation, router binding, and freeze.

Manual Prompt Code Hint Gate handles user disambiguation when classification
is difficult. Codes are namespaced internally, such as RSS-0005,
PLIB-0005, FRZ-0005, TEST-0005, or PROJECT-KANDA-RSS-0005.

A manual code is:

- a classification hint: yes
- a prompt registry reference: yes
- a shortcut to reduce ambiguity: yes
- final route authority: no
- a router override: no
- a prompt execution command: no
- a bypass of validation or freeze: no

A future prompt can be considered by router logic only after it is
validated, router-bound, frozen, active, and not superseded.
