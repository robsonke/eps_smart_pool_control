"""The switch implementation for the EPS Smart Pool Control integration."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity

from .eps_entity import EpsEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EpsDataUpdateCoordinator


def _set_nested_value(data: dict, path: str, value: object) -> None:
    """Set a value in a nested dict in-place using a dot-separated path, creating intermediate dicts as needed."""
    keys = path.split(".")
    current = data
    for key in keys[:-1]:
        current = current.setdefault(key, {})
    current[keys[-1]] = value


async def async_setup_entry(_hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control switch based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    switches = [
        EpsSwitch(coordinator, "eps_filterschedule1_enabled", "Filter Schedule 1", "filter", "config.schedule_1.enabled", "mdi:pump"),
        EpsSwitch(coordinator, "eps_filterschedule2_enabled", "Filter Schedule 2", "filter", "config.schedule_2.enabled", "mdi:pump"),
        EpsSwitch(coordinator, "eps_filterschedule3_enabled", "Filter Schedule 3", "filter", "config.schedule_3.enabled", "mdi:pump"),
        EpsSwitch(coordinator, "eps_filter_pump_force", "Filter Pump Force On", "filter", "config.always_active", "mdi:pump"),
    ]

    async_add_entities(switches, update_before_add=True)


class EpsSwitch(EpsEntity, SwitchEntity):  # type: ignore[misc]
    """Representation of an EPS Smart Pool Control switch."""

    def __init__(
        self,
        coordinator: EpsDataUpdateCoordinator,
        switch_type: str,
        name: str,
        data_key: str,
        api_field: str,
        icon: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._attr_name = name
        self._attr_icon = icon
        entry_id = coordinator.config_entry.entry_id if coordinator.config_entry else ""
        self._attr_unique_id = f"{entry_id}_{switch_type}"
        self.entity_id = f"switch.{switch_type}"

    @property
    def is_on(self) -> bool | None:  # type: ignore[override]
        """Return true if the switch is on."""
        value = self._get_nested_value(self.coordinator.data.get(self._data_key, {}), self._api_field)
        return bool(value) if value is not None else None

    @property
    def entity_registry_enabled_default(self) -> bool:  # type: ignore[override]
        """Disable entities belonging to modules the device reports as unsupported (status -1)."""
        return self._is_module_enabled(self._data_key)

    async def async_turn_on(self, **_kwargs: object) -> None:
        """Turn the switch on."""
        await self._async_set_value(value=True)

    async def async_turn_off(self, **_kwargs: object) -> None:
        """Turn the switch off."""
        await self._async_set_value(value=False)

    async def _async_set_value(self, *, value: bool) -> None:
        """PATCH the full module config with the changed field merged in."""
        # The API 422s on a single-field body (untagged enum deserialization needs the full config shape).
        write_path = self._api_field.removeprefix("config.")
        config = copy.deepcopy(self.coordinator.data.get(self._data_key, {}).get("config", {}))
        _set_nested_value(config, write_path, value)
        await self.coordinator.set_value(self._data_key, config)
