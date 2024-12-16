"""The sensor implementation for the EPS Smart Pool Control integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up EPS Smart Pool Control sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    # consider making the sensor conditionally to the device config, with fields such as:
    # - water_level_sensor_available
    # - deck_available
    # - clm_sensor_available

    sensors = [
        EpsSensor(coordinator, "eps_pool_water_temperature", "Water Temperature", "°C", "realtimedata", "water_temperature", "mdi:thermometer"),
        EpsSensor(coordinator, "eps_pool_ambient_temperature", "Ambient Temperature", "°C", "realtimedata", "ambient_temperature", "mdi:thermometer"),
        EpsSensor(coordinator, "eps_pool_solar_temperature", "Solar Temperature", "°C", "realtimedata", "solar_temperature", "mdi:thermometer"),
        EpsSensor(coordinator, "eps_pool_rx_level", "RX Level", None, "realtimedata", "rx_actual", "mdi:water-percent"),
        EpsSensor(coordinator, "eps_pool_ph_level", "pH Level", None, "realtimedata", "ph_actual", "mdi:water-percent"),
        EpsSensor(coordinator, "eps_pool_filterpump_current", "Filter Pump", None, "realtimedata", "filterpump_current", "mdi:water-pump"),
        EpsSensor(coordinator, "eps_imx_temperature", "IMX Temperature", "°C", "realtimedata", "imx_temperature", "mdi:thermometer"),
        EpsSensor(coordinator, "eps_main_temperature", "Main Temperature", "°C", "realtimedata", "main_temperature", "mdi:thermometer"),
        EpsSensor(coordinator, "eps_pool_volume_m3", "Pool Volume", "M3", "configuration", "volume_pool_m3", "mdi:image-size-select-small"),
    ]

    async_add_entities(sensors, update_before_add=True)

class EpsSensor(CoordinatorEntity, SensorEntity):
    """Representation of an EPS Smart Pool Control sensor."""

    def __init__(self, coordinator: EpsDataUpdateCoordinator, sensor_type: str, name: str, unit_of_measurement: str, data_key: str, api_field: str, icon: str):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._icon = icon

        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_unit_of_measurement = unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._data_key][self._api_field]

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
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        entry = self.coordinator.config_entry
        return {
            "identifiers": {(DOMAIN, entry.entry_id, entry.data.get("serialnumber"))},
            "name": f"EPS Smart Pool Control - {entry.data.get("serialnumber")}",
            "manufacturer": "Europe Pool Suppplies BV",
            "model": f"Smart Pool Control - {entry.data.get("serialnumber")}",
            "via_device": (DOMAIN, entry.entry_id),
        }
