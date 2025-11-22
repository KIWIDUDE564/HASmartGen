# Home Assistant Add-on: SmartGen Cloud Bridge

This add-on packages the SmartGen Cloud Bridge client so it can run under Home Assistant's Supervisor.

## Configuration options

Set the following options in the add-on UI:

- `username` – SmartGen Cloud Plus username (email)
- `password` – SmartGen Cloud Plus password
- `company_id` – Company identifier used by the API
- `language` – Optional language header (default: `en-US`)
- `timezone` – Optional timezone header (default: `UTC`)

## What it does

The add-on writes these options into `/data/config.yaml` and then launches `bridge.py`, which performs login and prints monitor list data to the add-on log output.

## Notes
- The add-on maps `/config` with read/write permissions so you can persist logs or alternate configs if needed.
- Logs are available from the add-on details page in Home Assistant.
