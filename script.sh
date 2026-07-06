#!/usr/bin/env bash
set -euo pipefail

echo "Creating project structure..."

mkdir -p \
    src/ai_kernel/{kernel,model,agent,tool,plugin,memory,policy,capability,message,cli} \
    tests \
    scripts

find src -type d -exec touch {}/__init__.py \;

cat > src/ai_kernel/__main__.py <<'EOF'
from ai_kernel.cli.main import app

app()
EOF

cat > src/ai_kernel/cli/main.py <<'EOF'
"""
CLI entry point for AI Kernel.
"""

import typer

app = typer.Typer(help="AI Kernel")


@app.command()
def version():
    """Print version information."""
    print("AI Kernel MVP")
EOF

echo "Done."
