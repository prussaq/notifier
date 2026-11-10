#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
NOTIFIER="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$NOTIFIER"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "Deploy aborted: current git branch is '$CURRENT_BRANCH' (expected 'main')." >&2
  exit 1
fi

CONF_FILE="$SCRIPT_DIR/targets.conf"

usage() {
    echo "Usage: $0 <full|lite> <target>" >&2
    exit 1
}

[[ $# -eq 3 ]] || usage

TARGET="$1"
CONFIG="$2"
VAULT="$3"

# Load target configuration.
[[ -f "$CONF_FILE" ]] || {
    echo "Config file not found: $CONF_FILE" >&2
    exit 1
}

source "$CONF_FILE"

# Target must define HOST, USER and PATH.
if [[ -z "${TARGETS[$TARGET]+x}" ]]; then
    echo "Unknown target: '$TARGET'." >&2
    exit 1
fi

IFS=':' read -r HOST USER TARGET_ROOT <<< "${TARGETS[$TARGET]}"

TARGET_PATH="$TARGET_ROOT/apps/notifier"
VAULT_PATH="$TARGET_ROOT/vault"

case "$HOST" in
    local|localhost|127.0.0.1)
        DESTINATION="$TARGET_PATH"
        echo "Deploying locally to '$DESTINATION'..."
        mkdir -p "$DESTINATION" "$VAULT_PATH"
        ;;
    *)
        DESTINATION="$USER@$HOST:$TARGET_PATH"
        echo "Creating remote directory '$TARGET_PATH' on host '$HOST'..."
        ssh "$USER@$HOST" "mkdir -p '$TARGET_PATH' '$VAULT_PATH'" 
        ;;
esac

# Copy application source and required files.
echo "Copying application files to $DESTINATION"

rsync -av --chmod=D700,F600 --delete \
    --include='runs/' \
    --include='runs/run.sh' \
    \
    --exclude-from="$NOTIFIER/.gitignore" \
    --exclude='AGENTS.md' \
    --exclude='TODO.md' \
    --exclude='.gitignore' \
    --exclude='.git' \
    --exclude='deploy/' \
    --exclude='tests/' \
    \
    --include='src/' \
    --include='src/notifier/***' \
    --include='scripts/***' \
    --include='requirements.txt' \
    --include='pyproject.toml' \
    --include='README.md' \
    --include='LICENSE' \
    \
    --exclude='*' \
    \
    "$NOTIFIER/" "$DESTINATION/"

# Copy selected configuration.
CONFIG_DEST="$DESTINATION/src/notifier/config"

echo "Copying $CONFIG config to $CONFIG_DEST/"

rsync -av --chmod=D700,F600 --delete \
    "$NOTIFIER/src/notifier/config/$CONFIG/" \
    "$CONFIG_DEST/"

# Copy vault
VAULT_DEST="$USER@$HOST:$VAULT_PATH"

echo "Copying vault to $VAULT_DEST/"

rsync -avL --chmod=D700,F600 --delete \
    "$VAULT/" \
    "$VAULT_DEST/"

case "$HOST" in
    local|localhost|127.0.0.1)
        echo "Running install script '$TARGET_ROOT/scripts/install.sh' with target path '$TARGET_PATH'..."
        bash "$TARGET_ROOT/scripts/install.sh" "$TARGET_PATH"
        ;;
    *)
        echo "Running remote install script '$TARGET_ROOT/scripts/install.sh' with target path '$TARGET_PATH' on host '$HOST'..."
        ssh "$USER@$HOST" "bash '$TARGET_ROOT/scripts/install.sh' '$TARGET_PATH'"
        ;;
esac

echo "Deployment complete: config='$CONFIG', target='$TARGET', destination='$DESTINATION'."