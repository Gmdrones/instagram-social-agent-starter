#!/usr/bin/env sh
set -eu
TARGET="${1:-$HOME/.local/share/instagram-social-agent}"
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ required"'
mkdir -p "$TARGET"
cp "$(dirname "$0")/src/social_agent/core.py" "$TARGET/social_agent.py"
python3 "$TARGET/social_agent.py" init
printf 'Installed. Run: python3 "%s/social_agent.py" draft\n' "$TARGET"
