import random
import string
from typing import Any

import aiohttp
from aiohttp_socks import ProxyConnector
from config import MAIL_API_BASE, PROXY_URL


def _get_connector() -> ProxyConnector | None:
    if PROXY_URL:
        return ProxyConnector.from_url(PROXY_URL)
    return None


async def _get_random_domain() -> str | None:
    connector = _get_connector()
    async with aiohttp.ClientSession(connector=connector) as session, session.get(f"{MAIL_API_BASE}/domains") as response:
        if response.status == 200:
            data = await response.json()
            domains = data.get("hydra:member", [])
            if domains:
                return domains[0].get("domain")
        return None

def _generate_random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

async def create_temp_mail() -> dict[str, str] | None:
    domain = await _get_random_domain()
    if not domain:
        return None

    username = f"wastle_{_generate_random_string(8)}"
    email = f"{username}@{domain}"
    password = _generate_random_string(12)

    connector = _get_connector()
    async with aiohttp.ClientSession(connector=connector) as session:
        # Create account
        async with session.post(
            f"{MAIL_API_BASE}/accounts",
            json={"address": email, "password": password}
        ) as resp:
            if resp.status not in (200, 201):
                return None
            acc_data = await resp.json()
            mail_id = acc_data.get("id")

        # Get token
        async with session.post(
            f"{MAIL_API_BASE}/token",
            json={"address": email, "password": password}
        ) as resp:
            if resp.status != 200:
                return None
            token_data = await resp.json()
            token = token_data.get("token")

    return {
        "email": email,
        "mail_id": mail_id,
        "token": token
    }

async def get_messages(token: str) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    connector = _get_connector()
    async with aiohttp.ClientSession(connector=connector) as session, session.get(f"{MAIL_API_BASE}/messages", headers=headers) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data.get("hydra:member", [])
    return []

async def get_message_detail(token: str, message_id: str) -> dict[str, Any] | None:
    headers = {"Authorization": f"Bearer {token}"}
    connector = _get_connector()
    async with aiohttp.ClientSession(connector=connector) as session, session.get(f"{MAIL_API_BASE}/messages/{message_id}", headers=headers) as resp:
        if resp.status == 200:
            return await resp.json()
    return None
