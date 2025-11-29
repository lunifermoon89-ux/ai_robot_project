#!/usr/bin/env bash
# Simple POSIX-friendly start script for `serve.py`.
# Usage: ./scripts/start-server.sh start|stop

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
PID_FILE="$ROOT_DIR/server.pid"
OUT_LOG="$ROOT_DIR/flask_stdout.log"
ERR_LOG="$ROOT_DIR/flask_stderr.log"
PYTHON="$ROOT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON=python3
fi

case "$1" in
  stop)
    if [ -f "$PID_FILE" ]; then
      PID=$(cat "$PID_FILE")
      echo "Stopping PID=$PID"
      kill "$PID" 2>/dev/null || true
      rm -f "$PID_FILE"
    else
      echo "No pid file"
    fi
    ;;
  start|)
    if [ -f "$PID_FILE" ]; then
      echo "Server may already be running (pid file exists): $PID_FILE"
      exit 0
    fi
    rm -f "$OUT_LOG" "$ERR_LOG"
    nohup "$PYTHON" "$ROOT_DIR/serve.py" >"$OUT_LOG" 2>"$ERR_LOG" &
    PID=$!
    echo "$PID" > "$PID_FILE"
    echo "Started PID=$PID, logs: $OUT_LOG / $ERR_LOG"
    ;;
  *)
    echo "Usage: $0 start|stop"
    exit 2
    ;;
esac
