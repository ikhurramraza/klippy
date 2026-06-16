#!/usr/bin/env bash

set -euo pipefail

# Keep post-create output quiet: the dev container echoes every line of stdout
# as "info" noise. Send verbose tool chatter to /dev/null while letting errors
# (stderr) through, so a real failure is still visible.

# Named volumes mount root-owned on first create, and mounting one at a
# subdirectory (.cache/zsh) leaves the parent (.cache) root-owned too. Hand
# the whole tree to the dev user so tools can create their own caches under it.
sudo chown -R vscode:vscode "$HOME/.claude" "$HOME/.config" "$HOME/.cache"

# Build a virtualenv and install klippy editable with dev deps
# (same command the CI workflows use).
python -m venv .venv >/dev/null
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
pip install --quiet -e . --group dev

# Install the Claude CLI via the native installer (no Node required).
if ! command -v claude >/dev/null 2>&1; then
  curl -fsSL https://claude.ai/install.sh | bash >/dev/null
fi

# Install cship (Claude Code statusline). The installer also wires up the
# statusLine entry in ~/.claude/settings.json, which the claude volume persists.
# --yes auto-installs its prerequisites non-interactively (including Starship).
if ! command -v cship >/dev/null 2>&1; then
  curl -fsSL https://cship.dev/install.sh | bash -s -- --yes >/dev/null
fi

# Seed the cship config on first boot. The .config volume persists it, so we
# only copy when absent to avoid clobbering live tweaks on rebuild.
if [ ! -f "$HOME/.config/cship.toml" ]; then
  cp .devcontainer/cship.toml "$HOME/.config/cship.toml"
fi

# Auto-configure klippy to talk to the redis sidecar so `klippy doctor`
# passes on first boot. Schema mirrors src/klippy/config.py.
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/klippy"
mkdir -p "$config_dir"
if [ ! -f "$config_dir/config.ini" ]; then
  cat >"$config_dir/config.ini" <<'EOF'
[main]
namespace = default

[redis]
host = redis
port = 6379
password =
EOF
fi

# Make the native-installed `claude` discoverable and auto-activate the venv.
if ! grep -q "# Klippy devcontainer" "$HOME/.zshrc" 2>/dev/null; then
  {
    echo ""
    echo "# Klippy devcontainer"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
    echo "source /workspaces/klippy/.venv/bin/activate"
  } >>"$HOME/.zshrc"
fi
