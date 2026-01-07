# In switch.py
"""The switch implementation for the EPS Smart Pool Control integration."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import EpsDataUpdateCoordinator
from .eps_entity import EpsEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control switch based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    switches = [
        EpsSwitch(
            coordinator,
            "eps_filterschedule1_enabled",
            "Filter Schedule 1",
            "settings",
            "settings_filterschedule1.filterschedule1_enabled",
            "mdi:pump",
        ),
        EpsSwitch(
            coordinator,
            "eps_filterschedule2_enabled",
            "Filter Schedule 2",
            "settings",
            "settings_filterschedule2.filterschedule2_enabled",
            "mdi:pump",
        ),
        EpsSwitch(
            coordinator,
            "eps_filterschedule3_enabled",
            "Filter Schedule 3",
            "settings",
            "settings_filterschedule3.filterschedule3_enabled",
            "mdi:pump",
        ),
        EpsSwitch(
            coordinator,
            "eps_filter_pump_force",
            "Filter Pump Force On",
            "settings",
            "settings_filter.filter_pump_force_on",
            "mdi:pump",
        ),
    ]

    async_add_entities(switches, update_before_add=True)


class EpsSwitch(EpsEntity, SwitchEntity):
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
        self._switch_type = switch_type
        self._attr_name = name
        self._icon = icon
        self.entity_id = f"switch.{self._switch_type}"
        # disable these switch entities for now, till we have an API method to set them
        self._attr_entity_registry_enabled_default = False

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        return self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the switch."""
        return f"{self.coordinator.config_entry.entry_id}_{self._switch_type}"

    @property
    def icon(self) -> str:
        """Return the icon of the switch."""
        return self._icon

    # async def async_turn_on(self, **kwargs) -> None:
    #     """Turn the switch on."""
    #     await self.coordinator.api.update_setting(
    #         self._settings_group, {self._api_field: True}
    #     )
    #     await self.coordinator.async_request_refresh()

    # async def async_turn_off(self, **kwargs) -> None:
    #     """Turn the switch off."""
    #     await self.coordinator.api.update_setting(
    #         self._settings_group, {self._api_field: False}
    #     )
    #     await self.coordinator.async_request_refresh()
