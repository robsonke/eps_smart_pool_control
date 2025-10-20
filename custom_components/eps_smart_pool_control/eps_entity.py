"""Base entity for EPS Smart Pool Control integration."""

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

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        entry = self.coordinator.config_entry
        return DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id, entry.data.get("serialnumber"))},
            name=f"EPS Smart Pool Control - {entry.data.get('serialnumber')}",
            manufacturer="Europe Pool Supplies BV",
            model=f"Smart Pool Control - {entry.data.get('serialnumber')}",
        )

    def _get_nested_value(self, data: dict, key_path: str) -> any:
        """Access nested dictionary fields using a dot-separated string."""
        if not data:
            return None

        keys = key_path.split(".")
        value = data
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value
