"""The binary sensor implementation for the EPS Smart Pool Control integration."""

from datetime import UTC, datetime, timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import EpsDataUpdateCoordinator
from .eps_entity import EpsEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control binary sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    binary_sensors = [
        EpsBinarySensor(
            coordinator,
            "eps_pool_error",
            "Pool Error",
            "realtimedata",
            "error",
            "mdi:alert-circle",
            "problem",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_empty_tank",
            "Empty Tank",
            "realtimedata",
            "empty_tank",
            "mdi:storage-tank-outline",
            "problem",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_pool_dirty",
            "Pool Dirty",
            "configuration",
            "is_dirty",
            "mdi:liquid-spot",
            "problem",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_cover_error",
            "Cover Error",
            "status",
            "cover_error",
            "mdi:alert-circle",
            "problem",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_flow",
            "Flow",
            "status",
            "flow",
            "mdi:waves-arrow-right",
            "moving",
        ),
        EpsPoolOnlineBinarySensor(
            coordinator,
            "eps_pool_online",
            "Pool Online",
            "status",
            "datetime",
            "mdi:wifi",
            "connectivity",
        ),
    ]

    async_add_entities(binary_sensors, update_before_add=True)


class EpsBinarySensor(EpsEntity, BinarySensorEntity):
    """Representation of an EPS Smart Pool Control binary sensor."""

    def __init__(
        self,
        coordinator: EpsDataUpdateCoordinator,
        sensor_type: str,
        name: str,
        data_key: str,
        api_field: str,
        icon: str,
        device_class: str | None = None,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._sensor_type = sensor_type
        self._attr_name = name
        self._icon = icon
        self._device_class = device_class
        self.entity_id = f"binary_sensor.{self._sensor_type}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the binary sensor."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return self._icon

    @property
    def device_class(self) -> str | None:
        """Return the device class of the sensor."""
        return self._device_class


class EpsPoolOnlineBinarySensor(EpsBinarySensor):
    """Representation of the EPS Pool Online binary sensor."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the datetime field is within the last 4 hours."""
        value = self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)

        if value is None or value == "0000-00-00 00:00:00":
            return False

        try:
            # Parse the datetime string (format: '2025-10-10T09:01:18.719000Z')
            last_update = datetime.fromisoformat(value.removesuffix("Z")).replace(tzinfo=UTC)
            current_time = datetime.now(UTC)
            time_diff = current_time - last_update

            # Return True if the last update was within the last 4 hours
            return time_diff <= timedelta(hours=4)
        except (ValueError, AttributeError):
            # If parsing fails, return False
            return False

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional state attributes."""
        attributes = {}
        value = self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)

        if value and value != "0000-00-00 00:00:00":
            try:
                last_update = datetime.fromisoformat(value.removesuffix("Z")).replace(tzinfo=UTC)
                current_time = datetime.now(UTC)
                time_diff = current_time - last_update

                # Add last update as datetime object for Home Assistant
                attributes["last_update_timestamp"] = last_update

                # Add human-readable time difference
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                attributes["time_since_update"] = f"{hours}h {minutes}m"

            except (ValueError, AttributeError):
                pass

        return attributes
