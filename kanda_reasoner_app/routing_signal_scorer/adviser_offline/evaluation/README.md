# Adviser Candidate v0 Evaluation Runner

This folder contains M12 offline evaluation runner code for Adviser Candidate v0.

Boundary:

- in-memory evaluation only;
- caller supplies seed-gold cases;
- no case discovery;
- no file reads or writes;
- no source scanning;
- no prompt auto-loading;
- no artifact IO;
- no candidate-output persistence;
- no scratch writer;
- no registry writer;
- no model/provider/network/embedding/vector behavior;
- no runtime router authority.

The runner calls the M11 candidate, applies M3/M4 guard/resource/severity checks,
and returns a structured report that identifies safety failures and mismatches for
future human review. The report is evidence only and must not be treated as
runtime routing authority.
