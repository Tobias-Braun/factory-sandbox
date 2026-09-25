# The agent's toolbox. Add the project's language toolchain below; the factory only needs git, gh,
# jq and Claude Code.
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update \
 && apt-get install -y --no-install-recommends gh jq python3 python3-venv python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Claude Code is installed for the non-root user: bypassPermissions refuses to run as root.
USER vscode
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/home/vscode/.local/bin:${PATH}"
