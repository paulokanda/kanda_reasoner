# KANDA Reasoner Portable hardening state

The stable Portable builder identity remains `kanda-reasoner-portable-builder-install-v1r12`.

Completed hardening capabilities, in order:

1. `registry-boundary-gate`
2. `packaged-gui-smoke-isolation`
3. `governed-root-exact-rollback`
4. `runtime-path-hash-allowlist`
5. `exact-builder-member-governance`
6. `external-build-control-hash-binding`

Stage 6 is identified separately by
`kanda-reasoner-portable-external-build-control-hash-binding-v1r1`.

Seven external build-control authorities are bound by exact relative path, role,
size, and SHA-256: the PyInstaller specification, both import-time package
initializers, the archive-policy owner, its Kilo-workspace dependency, and the
two policy manifests. They are checked during environment preflight, immediately
before PyInstaller, and immediately after PyInstaller. Any mutation fails closed
before staging or publication.

The exact `portable/` builder member baseline is now 29 files and 0 directories.
Production Portable creation remains blocked until Stage 6 is independently
validated, frozen, memorized, and a separate final readiness authorization
explicitly opens the production gate.
