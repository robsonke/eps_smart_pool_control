# FILE: binary_sensor.py
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up EPS Smart Pool Control binary sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    binary_sensors = [
        EpsBinarySensor(coordinator, "pool_error", "Pool Error", "error"),
        EpsBinarySensor(coordinator, "empty_tank", "Empty Tank", "empty_tank"),
    ]

    async_add_entities(binary_sensors, update_before_add=True)

class EpsBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of an EPS Smart Pool Control binary sensor."""

    def __init__(self, coordinator: EpsDataUpdateCoordinator, sensor_type: str, name: str, api_field: str):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.api_field = api_field
        self._sensor_type = sensor_type
        self._attr_name = name

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data[self.api_field]

    @property
    def unique_id(self):
        """Return a unique ID for the binary sensor."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

    @property
    def device_info(self):
        """Return device information about this entity."""
        entry = self.coordinator.config_entry
        return {
            "identifiers": {(DOMAIN, entry.entry_id, entry.data.get("serialnumber"))},
            "name": f"EPS Smart Pool Control - {entry.data.get("serialnumber")}",
            "manufacturer": "Europe Pool Suppplies BV",
            "model": f"Smart Pool Control - {entry.data.get("serialnumber")}",
            "via_device": (DOMAIN, entry.entry_id),
        }

