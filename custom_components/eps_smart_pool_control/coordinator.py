
"""The EpsDataUpdateCoordinator class which manages fetching data from the EPS Smart Pool Control API."""

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class EpsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the EPS Smart Pool Control API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the coordinator."""
        self.api_key = entry.data.get("api_key")
        self.serialnumber = entry.data.get("serialnumber")
        self.hass = hass

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    def _raise_update_failed(self, response):
        raise UpdateFailed(f"Error fetching data: {response.status}")

    async def _async_update_data(self):
        """Fetch data from the API."""
        return {
                "realtimedata": await self._fetch_api_data("realtimedata"),
                "status": await self._fetch_api_data("status"),
                "configuration": await self._fetch_api_data("configuration"),
                "settings": await self._fetch_api_data("settings"),
            }

    async def _fetch_api_data(self, path: str):
        """Fetch realtime data from the API."""
        try:
            async with self.hass.helpers.aiohttp_client.async_get_clientsession().get(
                f"https://api.smartpoolcontrol.eu/publicapi/{path}?serialnumber={self.serialnumber}&api_key={self.api_key}"
            ) as response:
                if response.status != 200:
                    self._raise_update_failed(response)
                response = await response.json()
                # the response can be a list
                if isinstance(response, list):
                    return response[0]
                return response

        except Exception as err:
            raise UpdateFailed(f"Error fetching realtime data: {err}") from err

    async def _push_api_data(self, endpoint: str, data: dict):
        """Push data to a specific API endpoint."""
        async with self.hass.helpers.aiohttp_client.async_get_clientsession().put(
            f"https://api.smartpoolcontrol.eu/publicapi/{endpoint}?serialnumber={self.serialnumber}&api_key={self.api_key}",
            json=data,
        ) as response:
            return response

    async def set_value(self, endpoint: str, data: dict):
        """Set a value through the API."""
        # we need to build up the json body, which should be the original GET body with the modified value
        original_data = await self._fetch_api_data(endpoint)
        body = self._update_body(original_data, data)
        print(body)
        # and we need the pool id for the PUT call
        pool_id = await self._get_pool_id()
        endpoint = f"{endpoint}/{pool_id}/"

        # push the data
        response = await self._push_api_data(endpoint, body)

        if response.status != 200:
            self._raise_update_failed(response)
        await self._async_update_data()

    async def _get_pool_id(self):
        """Get the pool id from the status endpoint."""
        async with self.hass.helpers.aiohttp_client.async_get_clientsession().get(
            f"https://api.smartpoolcontrol.eu/publicapi/status?serialnumber={self.serialnumber}&api_key={self.api_key}"
        ) as response:
            if response.status != 200:
                self._raise_update_failed(response)
            return (await response.json())[0]["id"]

    def _update_body(self, original_data, data):
        for k, v in data.items():
            if isinstance(v, dict):
                original_data[k] = self._update_body(original_data.get(k, {}), v)
            else:
                original_data[k] = v
        return original_data
