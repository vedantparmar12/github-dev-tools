#!/bin/bash
# GitHub Dev Tools Skill - Installation Script

set -e

echo "Installing GitHub Dev Tools Skill for Codex CLI..."
echo ""

# Determine installation location
if [ -n "$1" ]; then
    INSTALL_DIR="$1"
else
    # Default to user skills directory
    INSTALL_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
fi

# Create skills directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy skill files
echo "Installing to: $INSTALL_DIR/github-dev-tools"
cp -r "$SCRIPT_DIR" "$INSTALL_DIR/github-dev-tools"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r "$INSTALL_DIR/github-dev-tools/scripts/requirements.txt"
elif command -v pip &> /dev/null; then
    pip install -r "$INSTALL_DIR/github-dev-tools/scripts/requirements.txt"
else
    echo "Warning: pip not found. Please install Python dependencies manually:"
    echo "  pip install -r $INSTALL_DIR/github-dev-tools/scripts/requirements.txt"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Set your GitHub Personal Access Token:"
echo "   export GITHUB_PERSONAL_ACCESS_TOKEN='ghp_your_token_here'"
echo ""
echo "2. Add to your shell profile (~/.bashrc or ~/.zshrc):"
echo "   echo 'export GITHUB_PERSONAL_ACCESS_TOKEN=\"ghp_your_token_here\"' >> ~/.bashrc"
echo ""
echo "3. Start using the skill in Codex:"
echo "   - Just describe GitHub tasks naturally"
echo "   - Or use: \$github-dev-tools <description>"
echo ""
echo "For more information, see: $INSTALL_DIR/github-dev-tools/README.md"
