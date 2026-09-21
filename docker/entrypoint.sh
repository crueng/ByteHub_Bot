#!/bin/sh
set -eu

: "${BYTEHUB_REPOSITORY:=https://github.com/crueng/ByteHub_Bot.git}"
: "${BYTEHUB_BRANCH:=main}"
: "${BYTEHUB_PULL:=1}"

if [ "$BYTEHUB_PULL" != "0" ]; then
    echo "entrypoint: updating from $BYTEHUB_REPOSITORY ($BYTEHUB_BRANCH)"

    if [ ! -d /app/.git ]; then
        git init --quiet /app
    fi

    git -C /app remote set-url origin "$BYTEHUB_REPOSITORY" 2>/dev/null \
        || git -C /app remote add origin "$BYTEHUB_REPOSITORY"

    git -C /app fetch --quiet --depth 1 origin "$BYTEHUB_BRANCH"
    git -C /app reset --quiet --hard "origin/$BYTEHUB_BRANCH"
    git -C /app clean --quiet -fd -e settings.local.yaml

    echo "entrypoint: now at $(git -C /app rev-parse --short HEAD)"
else
    echo "entrypoint: pulling disabled, running the code already in /app"
fi

if [ ! -f /app/requirements.txt ]; then
    echo "entrypoint: /app holds no requirements.txt, is the volume empty?" >&2
    exit 1
fi

pip install --no-cache-dir --quiet --requirement /app/requirements.txt

exec "$@"