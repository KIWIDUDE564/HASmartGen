"""CLI bridge for SmartGen Cloud Plus."""
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
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found. Please create it before running the bridge.")

    config = load_config(config_path)
    client = SmartGenClient(config)

    login_response = client.login()
    print("Login response:")
    print(json.dumps(login_response, indent=2, ensure_ascii=False))

    monitor_data = client.get_monitor_list()
    print("\nMonitor list:")
    print(json.dumps(monitor_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
