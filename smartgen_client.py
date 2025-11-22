"""SmartGen Cloud Plus client implementation.

This module provides a simple, documented Python client for interacting with
SmartGen Cloud Plus using SM4 encryption and the X-Sign header logic.
"""
from __future__ import annotations

import base64
import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from gmssl.sm4 import CryptSM4, SM4_DECRYPT, SM4_ENCRYPT

BASE_URL = "https://www.smartgencloudplus.cn/yewu"
SM4_KEY_HEX = "7346346d54327455307a55366d4c3775"
SM4_KEY_BYTES = bytes.fromhex(SM4_KEY_HEX)
X_SIGN_SECRET = "fsh@TRuZ4dvcp5uY"


def _md5_hex(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)


def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        return data
    padding_len = data[-1]
    if padding_len < 1 or padding_len > len(data):
        raise ValueError("Invalid PKCS7 padding")
    return data[:-padding_len]


def sm4_encrypt_plaintext(plaintext: str) -> str:
    cipher = CryptSM4()
    cipher.set_key(SM4_KEY_BYTES, SM4_ENCRYPT)
    padded = pkcs7_pad(plaintext.encode("utf-8"))
    encrypted = cipher.crypt_ecb(padded)
    return base64.b64encode(encrypted).decode("utf-8")


def sm4_decrypt_ciphertext(ciphertext: str) -> str:
    cipher_bytes = base64.b64decode(ciphertext)
    cipher = CryptSM4()
    cipher.set_key(SM4_KEY_BYTES, SM4_DECRYPT)
    decrypted = cipher.crypt_ecb(cipher_bytes)
    unpadded = pkcs7_unpad(decrypted)
    return unpadded.decode("utf-8")


def make_x_sign(ts: int, token: Optional[str]) -> str:
    """Generate X-Sign header following nested MD5 rules."""
    if token:
        inner = _md5_hex(f"{token}{ts}{X_SIGN_SECRET}")
        return _md5_hex(f"{token}{ts}{inner}")
    inner = _md5_hex(f"{ts}{X_SIGN_SECRET}")
    return _md5_hex(f"{ts}{inner}")


@dataclass
class SmartGenConfig:
    username: str
    password: str
    company_id: str
    language: str = "en-US"
    timezone: str = "UTC"
    base_url: str = BASE_URL


class SmartGenClient:
    """Client for SmartGen Cloud Plus operations."""

    def __init__(self, config: SmartGenConfig, session: Optional[requests.Session] = None) -> None:
        self.config = config
        self.session = session or requests.Session()
        self.token: Optional[str] = None

    def _headers(self, ts: int, token: Optional[str]) -> Dict[str, str]:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": self.config.language,
            "User-Agent": "okhttp/4.9.0",
            "X-Time": str(ts),
            "X-Timezone": self.config.timezone,
            "X-UpdateDate": "20250321",
            "X-Companyid": self.config.company_id,
            "X-Sign": make_x_sign(ts, token),
            "Content-Type": "text/plain;charset=UTF-8",
        }
        if token:
            headers["X-Token"] = token
            headers["Referer"] = "https://www.smartgencloudplus.cn/index"
        else:
            headers["Referer"] = "https://www.smartgencloudplus.cn/login"
        return headers

    def _post(self, path: str, payload: Dict[str, Any], token: Optional[str]) -> Dict[str, Any]:
        ts = int(time.time())
        body = sm4_encrypt_plaintext(json.dumps(payload, ensure_ascii=False))
        url = f"{self.config.base_url}{path}"
        response = self.session.post(url, data=body, headers=self._headers(ts, token), timeout=30)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        return self._decode_response(data)

    def _decode_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        decoded = dict(response_data)
        payload = response_data.get("data")
        if isinstance(payload, str):
            try:
                decrypted = sm4_decrypt_ciphertext(payload)
                decoded["data"] = json.loads(decrypted)
            except Exception:
                decoded["data"] = payload
        return decoded

    def login(self) -> Dict[str, Any]:
        payload = {
            "userName": self.config.username,
            "password": self.config.password,
            "companyId": self.config.company_id,
            "language": self.config.language,
        }
        result = self._post("/user/login", payload, token=None)
        self.token = result.get("token") or result.get("data", {}).get("token")
        return result

    def get_status(self, device_code: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"companyId": self.config.company_id}
        if device_code:
            payload["deviceCode"] = device_code
        return self._post("/devicedata/getstatus", payload, token=self.token)

    def get_monitor_list(self) -> Dict[str, Any]:
        payload = {
            "companyId": self.config.company_id,
            "page": 1,
            "pageSize": 20,
        }
        return self._post("/realTimeData/monitorList", payload, token=self.token)


__all__ = [
    "SmartGenClient",
    "SmartGenConfig",
    "make_x_sign",
    "sm4_decrypt_ciphertext",
    "sm4_encrypt_plaintext",
]
