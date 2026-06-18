"""The binary sensor implementation for the EPS Smart Pool Control integration."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .eps_entity import EpsEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(_hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control binary sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data
    async_add_entities([EpsPoolOnlineBinarySensor(coordinator)], update_before_add=True)


class EpsPoolOnlineBinarySensor(EpsEntity, BinarySensorEntity):  # type: ignore[misc]
    """Binary sensor reporting pool connectivity based on the V2 API status field."""

    _attr_name = "Pool Online"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_icon = "mdi:wifi"

    def __init__(self, coordinator: EpsDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_id = "binary_sensor.eps_pool_online"
        entry_id = coordinator.config_entry.entry_id if coordinator.config_entry else ""
        self._attr_unique_id = f"{entry_id}_eps_pool_online"

    @property
    def is_on(self) -> bool:  # type: ignore[override]
        """Return true when the pool reports as online."""
        return self.coordinator.data.get("status") == "online"

    @property
    def extra_state_attributes(self) -> dict[str, object]:  # type: ignore[override]
        """Return last-activity timestamp and human-readable age."""
        attributes: dict[str, object] = {}
        activity_at_ms = self.coordinator.data.get("activity_at")
        if isinstance(activity_at_ms, int | float):
            last_update = datetime.fromtimestamp(activity_at_ms / 1000, tz=UTC)
            current_time = datetime.now(UTC)
            time_diff = current_time - last_update
            attributes["last_update_timestamp"] = last_update
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            attributes["time_since_update"] = f"{hours}h {minutes}m"
        return attributes
