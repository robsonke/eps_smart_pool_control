"""The number implementation for the EPS Smart Pool Control integration."""

from config.custom_components.eps_smart_pool_control.eps_entity import EpsEntity
from homeassistant.components.number import NumberEntity
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
    """Set up EPS Smart Pool Control number based on a config entry."""
    # coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    # Temporary disabled, the POST/PUT API calls are not available anymore
    numbers = [
        # EpsNumber(
        #     coordinator,
        #     "eps_pool_rx_target_value",
        #     "RX Target",
        #     "settings",
        #     "settings_rx.rx_value_target",
        #     "mdi:water-percent",
        #     500,
        #     1000,
        # ),
        # EpsNumber(
        #     coordinator,
        #     "eps_pool_pk_target_value",
        #     "PH Target",
        #     "settings",
        #     "settings_ph.ph_value_target",
        #     "mdi:water-percent",
        #     0,
        #     14,
        # ),
        # EpsNumber(
        #     coordinator,
        #     "eps_pool_temperature_water_target",
        #     "Water Temperature Target",
        #     "settings",
        #     "settings_temperature.temperature_water_target",
        #     "mdi:thermometer-water",
        #     0,
        #     40,
        # ),
    ]

    async_add_entities(numbers, update_before_add=True)


class EpsNumber(EpsEntity, NumberEntity):
    """Representation of an EPS Smart Pool Control Number."""

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
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._sensor_type = sensor_type
        self._attr_name = name
        self._icon = icon
        self._min_value = min_value
        self._max_value = max_value
        self.entity_id = f"number.{self._sensor_type}"

    @property
    def state(self) -> float | None:
        """Return the state of the sensor."""
        return self._get_nested_value(
            self.coordinator.data[self._data_key], self._api_field
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the value through the api."""
        keys = self._api_field.split(".")
        nested_data = {}
        for index, key in enumerate(keys):
            if index == 0:
                nested_data[key] = {}
            elif index == len(keys) - 1:
                # last element, set the value
                nested_data[keys[index - 1]][key] = value
            else:
                nested_data[keys[index - 1]][key] = {}
        await self.coordinator.set_value(self._data_key, nested_data)
        await self.coordinator.async_request_refresh()

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the binary sensor."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return self._icon

    @property
    def native_min_value(self) -> float:
        """Return the minimum value of the number entity."""
        return self._min_value

    @property
    def native_max_value(self) -> float:
        """Return the maximum value of the number entity."""
        return self._max_value
