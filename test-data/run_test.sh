#!/usr/bin/env bash
set -euo pipefail

SESSION_FILE="/home/paul/projects/esql/test-data/session.json"
QUERY_FILE="/home/paul/projects/esql/test-data/query.json"

echo "[1/3] Creating session..." >&2
SESSION_RESP=$(curl -s -X POST http://localhost:8000/sessions \
  -H 'Content-Type: application/json' \
  -d @"${SESSION_FILE}")
echo "${SESSION_RESP}" | jq . >/dev/null

CHAT_ID=$(echo "${SESSION_RESP}" | jq -r '.chat_id // empty')
if [[ -z "${CHAT_ID}" ]]; then
  echo "Failed to create session or extract chat_id:" >&2
  echo "${SESSION_RESP}" >&2
  exit 1
fi
echo "chat_id: ${CHAT_ID}" >&2

echo "[2/3] Sending query..." >&2
QUERY_PAYLOAD=$(jq --arg id "${CHAT_ID}" '.chat_id=$id' "${QUERY_FILE}")
QUERY_RESP=$(curl -s -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d "${QUERY_PAYLOAD}")

echo "[3/3] Summary:" >&2
echo "${QUERY_RESP}" | jq '{success, nl_confidence, took: .data.search_stats.took, logs: (.data.logs | length)}'



