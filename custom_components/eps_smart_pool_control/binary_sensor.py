"""The binary sensor implementation for the EPS Smart Pool Control integration."""

from config.custom_components.eps_smart_pool_control.eps_entity import EpsEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
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
        ),
        EpsBinarySensor(
            coordinator,
            "eps_empty_tank",
            "Empty Tank",
            "realtimedata",
            "empty_tank",
            "mdi:storage-tank-outline",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_pool_dirty",
            "Pool Dirty",
            "configuration",
            "is_dirty",
            "mdi:liquid-spot",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_cover_error",
            "Cover Error",
            "status",
            "cover_error",
            "mdi:alert-circle",
        ),
        EpsBinarySensor(
            coordinator,
            "eps_flow",
            "Flow",
            "status",
            "flow",
            "mdi:waves-arrow-right",
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
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._sensor_type = sensor_type
        self._attr_name = name
        self._icon = icon
        self.entity_id = f"binary_sensor.{self._sensor_type}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._get_nested_value(
            self.coordinator.data[self._data_key], self._api_field
        )

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the binary sensor."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return self._icon
