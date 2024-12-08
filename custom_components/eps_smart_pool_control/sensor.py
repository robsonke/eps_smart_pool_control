from config.custom_components.eps_smart_pool_control.coordinator import (
    EpsDataUpdateCoordinator,
)
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up EPS Smart Pool Control sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    # Skipped:
    # {'tds_ppm': 0, 'pollution_degree_ppm': 0, 'conductivity': 0.0, 'clm_ppm': 0.0}

    # binary sensor for error

    sensors = [
        EpsSensor(coordinator, "pool_water_temperature", "Water Temperature", "°C", "water_temperature"),
        EpsSensor(coordinator, "pool_ambient_temperature", "Ambient Temperature", "°C", "ambient_temperature"),
        EpsSensor(coordinator, "pool_solar_temperature", "Solar Temperature", "°C", "solar_temperature"),
        EpsSensor(coordinator, "pool_rx_level", "RX Level", None, "rx_actual"),
        EpsSensor(coordinator, "pool_ph_level", "pH Level", None, "ph_actual"),
        EpsSensor(coordinator, "pool_filterpump_current", "Filterpump Current", None, "filterpump_current"),
        EpsSensor(coordinator, "imx_temperature", "IMX Temperature", "°C", "imx_temperature"),
        EpsSensor(coordinator, "main_temperature", "Main Temperature", "°C", "main_temperature"),
    ]

    async_add_entities(sensors, update_before_add=True)

class EpsSensor(CoordinatorEntity, SensorEntity):
    """Representation of an EPS Smart Pool Control sensor."""

    def __init__(self, coordinator: EpsDataUpdateCoordinator, sensor_type: str, name: str, unit_of_measurement: str, api_field: str):
        """Initialize the sensor."""
        super().__init__(coordinator)

        self.api_field = api_field

        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_unit_of_measurement = unit_of_measurement

    # @callback
    # def _handle_coordinator_update(self) -> None:
    #     """Handle updated data from the coordinator."""
    #     #print(self.coordinator.data)
    #     self._attr_is_on = self.coordinator.data[self.api_field]
    #     self.async_write_ha_state()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.api_field]

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this entity."""
        return f"{self.coordinator.config_entry.entry_id}_{self._sensor_type}"

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
