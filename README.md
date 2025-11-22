# smartgen-cloud-bridge

A clean Python bridge for SmartGen Cloud Plus. It logs in with SM4-encrypted payloads, builds the required X-Sign headers, and fetches live generator data.

## Features
- SM4 (ECB + PKCS7 + Base64) encryption helper utilities
- X-Sign nested MD5 signing with and without tokens
- Login and token handling for SmartGen Cloud Plus
- Convenience methods for `get_status` and `get_monitor_list`
- CLI bridge script that prints JSON responses in a readable format

## Requirements
- Python 3.10+
- Access to SmartGen Cloud Plus credentials (username, password, company ID)
- Network connectivity to `https://www.smartgencloudplus.cn/yewu`

## Install
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Create a `config.yaml` file in the project root:
```yaml
username: "your@email.com"
password: "your-password"
company_id: "1"
language: "en-US"
timezone: "America/Anchorage"
```

## How to run
1. Ensure `config.yaml` is populated.
2. Run the bridge:
   ```bash
   python bridge.py
   ```

## Example output
```
Login response:
{
  "code": 200,
  "message": "OK",
  "data": {
    "token": "example-token"
  }
}

Monitor list:
{
  "code": 200,
  "message": "OK",
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20
  }
}
```

## Security notice
- Keep `config.yaml` out of version control (already in `.gitignore`).
- Treat the SM4 key and X-Sign secret as sensitive; they are included here for interoperability only.
- Rotate credentials regularly and store secrets securely.
