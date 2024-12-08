import asyncio
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

        try:
            async with self.hass.helpers.aiohttp_client.async_get_clientsession().get(
                f"https://api.smartpoolcontrol.eu/publicapi/realtimedata?serialnumber={self.serialnumber}&api_key={self.api_key}"
            ) as response:
                if response.status != 200:
                    self._raise_update_failed(response)
                return await response.json()

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
