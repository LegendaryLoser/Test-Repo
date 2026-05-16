#!/usr/bin/env bash
# Install / upgrade BMAD v6.x in this repo.
#
# Pinned command per CHG-0010 and ADR-0002. Run from the repository root.
# After running, commit the diff and create a substrate PR (BMAD upgrade
# = substrate change per the hybrid merge policy).
#
# Outputs land in:
#   - _bmad/                            (framework, vendored)
#   - .claude/skills/                   (42 Claude Code Skills, vendored)
#   - openspec/_bmad-output/            (BMAD planning/implementation/knowledge
#                                        artifacts; configured below)
#
# Defaults wiped by side effects of install:
#   - docs/                             (empty side effect; remove after install)
#   - openspec/_bmad-output/planning-artifacts/    (default-named, replaced by configured)
#   - openspec/_bmad-output/implementation-artifacts/

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PINNED_VERSION="6.6.0"

echo "Installing BMAD ${PINNED_VERSION} (or compatible v6.x latest)…"

npx -y bmad-method install \
  --yes \
  --directory . \
  --tools claude-code \
  --modules bmm \
  --action install \
  --user-name "spec-lint" \
  --communication-language English \
  --document-output-language English \
  --output-folder openspec/_bmad-output \
  --set bmm.planning_artifacts=openspec/_bmad-output/planning \
  --set bmm.implementation_artifacts=openspec/_bmad-output/implementation \
  --set bmm.project_knowledge=openspec/_bmad-output/knowledge

# Clean up side-effect directories that the install creates before reading
# the routed config:
[[ -d docs ]] && rmdir docs 2>/dev/null || true
[[ -d openspec/_bmad-output/planning-artifacts ]] && rmdir openspec/_bmad-output/planning-artifacts 2>/dev/null || true
[[ -d openspec/_bmad-output/implementation-artifacts ]] && rmdir openspec/_bmad-output/implementation-artifacts 2>/dev/null || true

# Preserve the routing namespace even when empty:
mkdir -p openspec/_bmad-output
touch openspec/_bmad-output/.gitkeep

echo
echo "BMAD install complete."
echo "Installed version: $(grep '^  version:' _bmad/_config/manifest.yaml | head -1 | awk '{print $2}')"
echo
echo "Next steps:"
echo "  1. Review git diff (large; mostly vendored skill markdown)."
echo "  2. Commit as a substrate PR (CHG-NNNN)."
echo "  3. Open PR for merge review per the hybrid policy."
