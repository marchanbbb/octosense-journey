#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="$(cd "$APP_DIR/.." && pwd)"
OCTO_TOOL="${OCTO_TOOL:-$WORKSPACE_DIR/OctoScript-App-Design-Flow/tools/octo}"
exec "$OCTO_TOOL" run "$APP_DIR/bundle" "$@"
