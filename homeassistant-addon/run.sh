#!/usr/bin/env bash
set -euo pipefail

OPTIONS_FILE="/data/options.json"
CONFIG_OUT="/data/config.yaml"
APP_DIR="/usr/src/app"

if [[ ! -f "${OPTIONS_FILE}" ]]; then
  echo "Home Assistant options file not found at ${OPTIONS_FILE}." >&2
  exit 1
fi

USERNAME=$(jq -r '.username // empty' "${OPTIONS_FILE}")
PASSWORD=$(jq -r '.password // empty' "${OPTIONS_FILE}")
COMPANY_ID=$(jq -r '.company_id // empty' "${OPTIONS_FILE}")
LANGUAGE=$(jq -r '.language // "en-US"' "${OPTIONS_FILE}")
TIMEZONE=$(jq -r '.timezone // "UTC"' "${OPTIONS_FILE}")

if [[ -z "${USERNAME}" || -z "${PASSWORD}" || -z "${COMPANY_ID}" ]]; then
  echo "username, password, and company_id are required options." >&2
  exit 1
fi

cat > "${CONFIG_OUT}" <<EOF_CONFIG
username: "${USERNAME}"
password: "${PASSWORD}"
company_id: "${COMPANY_ID}"
language: "${LANGUAGE}"
timezone: "${TIMEZONE}"
EOF_CONFIG

cd "${APP_DIR}"
python3 bridge.py --config "${CONFIG_OUT}"
