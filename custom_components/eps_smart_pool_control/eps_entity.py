"""Base entity for EPS Smart Pool Control integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EpsDataUpdateCoordinator


class EpsEntity(CoordinatorEntity[EpsDataUpdateCoordinator]):
    """Base entity for EPS Smart Pool Control integration."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EpsDataUpdateCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        entry = coordinator.config_entry
        if entry is not None:
            mac = entry.data.get("mac_address", "")
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, entry.entry_id)},
                name=f"EPS Smart Pool Control - {mac}",
                manufacturer="Europe Pool Supplies BV",
                model=f"Smart Pool Control - {mac}",
            )

    def _get_nested_value(self, data: dict, key_path: str) -> object:
        """Access nested dictionary fields using a dot-separated string."""
        if not data:
            return None

        keys = key_path.split(".")
        value: object = data
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value

    def _is_module_enabled(self, data_key: str) -> bool:
        """Return False when the module's status.status is -1 (hardware not present on this device)."""
        module_data = self.coordinator.data.get(data_key) if self.coordinator.data else None
        if not isinstance(module_data, dict):
            return True
        return self._get_nested_value(module_data, "status.status") != -1
