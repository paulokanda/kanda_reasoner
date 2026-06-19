# Adviser Active Review Queue v1

This package contains the M13 active review queue builder for the Routing Signal
Scorer v3 Adviser path.

Boundary:

- adviser-offline only;
- standard-library-only;
- pure over caller-supplied in-memory evaluation reports;
- no file reads or writes;
- no case discovery;
- no source scanning;
- no prompt auto-loading;
- no artifact generation;
- no queue persistence;
- no candidate output persistence;
- no scratch writer;
- no registry writer;
- no gold mutation;
- no model/provider/embedding/vector/network/dependency behavior;
- no runtime router authority.

The queue is evidence for human review. It does not approve candidates, promote
candidate behavior, mutate gold sets, or grant router authority.
