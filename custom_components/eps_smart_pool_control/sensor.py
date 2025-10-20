"""The sensor implementation for the EPS Smart Pool Control integration."""

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import EpsDataUpdateCoordinator
from .eps_entity import EpsEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    # consider making the sensor conditionally to the device config, with fields such as:
    # - water_level_sensor_available
    # - deck_available
    # - clm_sensor_available

    sensors = [
        EpsSensor(
            coordinator,
            "eps_pool_water_temperature",
            "Water Temperature",
            "°C",
            "realtimedata",
            "water_temperature",
            "mdi:thermometer",
            "temperature",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_ambient_temperature",
            "Ambient Temperature",
            "°C",
            "realtimedata",
            "ambient_temperature",
            "mdi:thermometer",
            "temperature",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_solar_temperature",
            "Solar Temperature",
            "°C",
            "realtimedata",
            "solar_temperature",
            "mdi:thermometer",
            "temperature",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_rx_level",
            "RX Level",
            "mV",
            "realtimedata",
            "rx_actual",
            "mdi:water-percent",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_ph_level",
            "pH Level",
            None,
            "realtimedata",
            "ph_actual",
            "mdi:water-percent",
            "ph",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_filterpump_current",
            "Filter Pump",
            None,
            "realtimedata",
            "filterpump_current",
            "mdi:water-pump",
        ),
        EpsSensor(
            coordinator,
            "eps_imx_temperature",
            "IMX Temperature",
            "°C",
            "realtimedata",
            "imx_temperature",
            "mdi:thermometer",
            "temperature",
        ),
        EpsSensor(
            coordinator,
            "eps_main_temperature",
            "Main Temperature",
            "°C",
            "realtimedata",
            "main_temperature",
            "mdi:thermometer",
            "temperature",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_volume_m3",
            "Pool Volume",
            "m³",
            "configuration",
            "volume_pool_m3",
            "mdi:image-size-select-small",
            "volume_storage",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_cover",
            "Pool Cover",
            None,
            "status",
            "cover",
            "mdi:arrow-expand-horizontal",
            device_class=SensorDeviceClass.ENUM,
            options=["unknown", "open", "closed", "opening", "closing", "semi open"],
        ),
        EpsSensor(
            coordinator,
            "eps_pool_pump_speed",
            "Pump Speed",
            None,
            "status",
            "pumpspeed",
            "mdi:speedometer",
            device_class=SensorDeviceClass.ENUM,
            options=["unknown", "low", "medium", "high"],
        ),
        EpsSensor(
            coordinator,
            "eps_pool_pump_mode",
            "Pump Mode",
            None,
            "status",
            "pump",
            "mdi:water-pump",
            device_class=SensorDeviceClass.ENUM,
            options=[
                "unknown",
                "scheme 1 active",
                "scheme 2 active",
                "scheme 3 active",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "always on active",
            ],
        ),
        EpsSensor(
            coordinator,
            "eps_pool_backwash",
            "Backwash",
            None,
            "status",
            "backwash",
            "mdi:skip-backward",
            None,
        ),
        # Three temporary sensors, which are normally numbers
        EpsSensor(
            coordinator,
            "eps_pool_rx_target_value",
            "RX Target",
            None,
            "settings",
            "settings_rx.rx_value_target",
            "mdi:water-percent",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_pk_target_value",
            "PH Target",
            None,
            "settings",
            "settings_ph.ph_value_target",
            "mdi:water-percent",
        ),
        EpsSensor(
            coordinator,
            "eps_pool_temperature_water_target",
            "Water Temperature Target",
            None,
            "settings",
            "settings_temperature.temperature_water_target",
            "mdi:thermometer-water",
        ),
    ]

    async_add_entities(sensors, update_before_add=True)


class EpsSensor(EpsEntity, SensorEntity):
    """Representation of an EPS Smart Pool Control sensor."""

    def __init__(
        self,
        coordinator: EpsDataUpdateCoordinator,
        sensor_type: str,
        name: str,
        unit_of_measurement: str,
        data_key: str,
        api_field: str,
        icon: str,
        device_class: str | None = None,
        options: list[str] | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._icon = icon
        self._device_class = device_class
        self._options = options

        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_unit_of_measurement = unit_of_measurement
        self.entity_id = f"sensor.{self._sensor_type}"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        value = self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)
        if self._options and isinstance(value, int):
            try:
                return self._options[value]
            except IndexError:
                return "unknown"
        return value

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional state attributes."""
        attributes = {}

        # Add extra attributes in case of ENUM sensor
        if self._options:
            value = self._get_nested_value(self.coordinator.data[self._data_key], self._api_field)
            if value is not None:
                attributes["raw_value"] = value
            attributes["options"] = self._options
        return attributes

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this entity."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return self._icon

    @property
    def unit(self) -> str:
        """Unit of this sensor."""
        return self._attr_unit_of_measurement

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this sensor."""
        return self._attr_unit_of_measurement

    @property
    def device_class(self) -> str | None:
        """Return the device class of this sensor."""
        return self._device_class
