"""The number implementation for the EPS Smart Pool Control integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.number import NumberEntity

from .eps_entity import EpsEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(_hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control number based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    numbers = [
        EpsNumber(coordinator, "eps_pool_rx_target_value", "RX Target", "cl", "config.rx.target", "mdi:water-percent", 500, 1000),
        EpsNumber(coordinator, "eps_pool_pk_target_value", "PH Target", "ph", "config.target", "mdi:water-percent", 0, 14, 0.1),
        EpsNumber(coordinator, "eps_pool_temperature_water_target", "Water Temperature Target", "temperature", "config.target", "mdi:thermometer-water", 0, 40, 0.1),
    ]

    async_add_entities(numbers, update_before_add=True)


class EpsNumber(EpsEntity, NumberEntity):  # type: ignore[misc]
    """Representation of an EPS Smart Pool Control number entity."""

    def __init__(
        self,
        coordinator: EpsDataUpdateCoordinator,
        sensor_type: str,
        name: str,
        data_key: str,
        api_field: str,
        icon: str,
        min_value: float,
        max_value: float,
        step: float = 1,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        entry_id = coordinator.config_entry.entry_id if coordinator.config_entry else ""
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self.entity_id = f"number.{sensor_type}"

    @property
    def native_value(self) -> float | None:  # type: ignore[override]
        """Return the current value."""
        value = self._get_nested_value(self.coordinator.data.get(self._data_key, {}), self._api_field)
        return round(value, 1) if isinstance(value, int | float) else None

    async def async_set_native_value(self, value: float) -> None:
        """PATCH the new value to the module config endpoint."""
        await self.coordinator.set_value(self._data_key, {"target": value})
