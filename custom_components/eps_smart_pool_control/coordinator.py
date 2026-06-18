"""The EpsDataUpdateCoordinator class which manages fetching data from the EPS Smart Pool Control API."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Never

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
_API_BASE = "https://api.smartpoolconnect.eu"


class EpsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the EPS Smart Pool Control API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.api_key: str = entry.data.get("api_key", "")
        self.mac_address: str = entry.data.get("mac_address", "")
        self.pid: str | None = None
        self.hass = hass

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _raise_update_failed(self, response: aiohttp.ClientResponse) -> Never:
        try:
            body = await response.text()
        except aiohttp.ClientError:
            body = "<unreadable>"
        msg = f"API {response.method} {response.url} failed: {response.status} {response.reason} — {body}"
        _LOGGER.error(msg)
        raise UpdateFailed(msg)

    async def _async_update_data(self) -> dict:
        """Fetch data from the API."""
        if not self.pid:
            self.pid = await self._resolve_pid()
        return await self._fetch_pool_data()

    async def _resolve_pid(self) -> str:
        """Resolve the pool UUID from the MAC address via the pool list endpoint."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                f"{_API_BASE}/pool",
                headers={"X-API-Key": self.api_key},
                params={"mac": self.mac_address},
            ) as response:
                if not response.ok:
                    await self._raise_update_failed(response)
                data = await response.json()
        except UpdateFailed:
            raise
        except Exception as err:
            msg = f"Error resolving pool ID: {err}"
            raise UpdateFailed(msg) from err

        items = data.get("items", [])
        if not items:
            msg = f"No pool found for MAC address {self.mac_address}"
            raise UpdateFailed(msg)
        return items[0]["pid"]

    async def _fetch_pool_data(self) -> dict:
        """Fetch the full pool state from GET /pool/{pid}."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                f"{_API_BASE}/pool/{self.pid}",
                headers={"X-API-Key": self.api_key},
            ) as response:
                if not response.ok:
                    await self._raise_update_failed(response)
                return await response.json()
        except UpdateFailed:
            raise
        except Exception as err:
            msg = f"Error fetching pool data: {err}"
            raise UpdateFailed(msg) from err

    async def set_value(self, module: str, data: dict) -> None:
        """PATCH a partial update to a pool module endpoint."""
        session = async_get_clientsession(self.hass)
        async with session.patch(
            f"{_API_BASE}/pool/{self.pid}/{module}",
            headers={"X-API-Key": self.api_key},
            json=data,
        ) as response:
            if not response.ok:
                await self._raise_update_failed(response)
        await self.async_request_refresh()
