# Adviser Gold Set Expansion Plan v1

This folder contains M15, a pure in-memory planning helper for future seed-gold
set expansion. It does **not** add gold cases and does **not** change the current
gold set.

Boundary rules:

- adviser-offline only;
- standard-library-only;
- caller-supplied dictionaries only;
- no file I/O or case discovery;
- no source scanning or prompt auto-loading;
- no artifact I/O;
- no gold mutation;
- no automatic approvals;
- no candidate promotion;
- no registry writer, scratch writer, run-record writer, or persistence;
- no runtime router authority.

Every planned expansion item remains human-review-required and blocked until a
future governed patch creates reviewed cases and promotion criteria are satisfied.
