"""CLI bridge for SmartGen Cloud Plus."""
import argparse
import json
from pathlib import Path

import yaml

from smartgen_client import SmartGenClient, SmartGenConfig


def load_config(config_path: Path) -> SmartGenConfig:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return SmartGenConfig(
        username=data["username"],
        password=data["password"],
        company_id=str(data["company_id"]),
        language=data.get("language", "en-US"),
        timezone=data.get("timezone", "UTC"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="SmartGen Cloud Plus bridge")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to YAML configuration file (default: config.yaml)",
    )
    args = parser.parse_args()

    if not args.config.exists():
        raise FileNotFoundError(
            f"Config file {args.config} not found. Please create it before running the bridge."
        )

    config = load_config(args.config)
    client = SmartGenClient(config)

    login_response = client.login()
    print("Login response:")
    print(json.dumps(login_response, indent=2, ensure_ascii=False))

    monitor_data = client.get_monitor_list()
    print("\nMonitor list:")
    print(json.dumps(monitor_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
