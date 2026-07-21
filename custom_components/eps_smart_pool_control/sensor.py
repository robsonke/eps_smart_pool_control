"""The sensor implementation for the EPS Smart Pool Control integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass

from .eps_entity import EpsEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(_hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control sensor based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data

    sensors = [
        EpsSensor(
            coordinator,
            "eps_pool_water_temperature",
            "Water Temperature",
            "°C",
            "temperature",
            "metrics.water_temp",
            "mdi:thermometer",
            SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        EpsSensor(
            coordinator,
            "eps_pool_ambient_temperature",
            "Ambient Temperature",
            "°C",
            "temperature",
            "metrics.ambient_temp",
            "mdi:thermometer",
            SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        EpsSensor(
            coordinator, "eps_imx_temperature", "IMX Temperature", "°C", "temperature", "metrics.imx_temp", "mdi:thermometer", SensorDeviceClass.TEMPERATURE, state_class=SensorStateClass.MEASUREMENT
        ),
        EpsSensor(coordinator, "eps_pool_rx_level", "RX Level", "mV", "cl", "metrics.actual", "mdi:water-percent", state_class=SensorStateClass.MEASUREMENT),
        EpsSensor(coordinator, "eps_pool_ph_level", "pH Level", None, "ph", "metrics.actual", "mdi:water-percent", SensorDeviceClass.PH, state_class=SensorStateClass.MEASUREMENT),
        EpsSensor(
            coordinator, "eps_pool_filterpump_current", "Filter Pump", "A", "filter", "metrics.pump_current", "mdi:water-pump", SensorDeviceClass.CURRENT, state_class=SensorStateClass.MEASUREMENT
        ),
        EpsSensor(
            coordinator, "eps_pool_volume_m3", "Pool Volume", "m³", "spec", "pool_volume", "mdi:image-size-select-small", SensorDeviceClass.VOLUME_STORAGE, state_class=SensorStateClass.MEASUREMENT
        ),
        EpsSensor(
            coordinator,
            "eps_pool_pump_speed",
            "Pump Speed",
            None,
            "filter",
            "status.pump_speed",
            "mdi:speedometer",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 0: "off", 1: "low", 2: "medium", 3: "high", 4: "max"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_pump_mode",
            "Pump Mode",
            None,
            "filter",
            "status.pump_status",
            "mdi:water-pump",
            device_class=SensorDeviceClass.ENUM,
            options={
                -1: "unsupported",
                0: "off",
                1: "schedule 1",
                2: "schedule 2",
                3: "schedule 3",
                4: "heating",
                5: "solar",
                6: "backwash",
                7: "cooling",
                8: "manual",
                9: "frost",
                10: "active",
                11: "cover",
                12: "valve",
                13: "cover closed",
                14: "invalid",
            },
        ),
        EpsSensor(
            coordinator,
            "eps_pool_backwash",
            "Backwash",
            None,
            "backwash",
            "status.status",
            "mdi:skip-backward",
            device_class=SensorDeviceClass.ENUM,
            options={
                -1: "due",
                0: "off",
                1: "on",
            },
        ),
        EpsSensor(coordinator, "eps_pool_rx_target_value", "RX Target", "mV", "cl", "config.rx.target", "mdi:water-percent"),
        EpsSensor(coordinator, "eps_pool_pk_target_value", "PH Target", None, "ph", "config.target", "mdi:water-percent", SensorDeviceClass.PH),
        EpsSensor(coordinator, "eps_pool_temperature_water_target", "Water Temperature Target", "°C", "temperature", "config.target", "mdi:thermometer-water", SensorDeviceClass.TEMPERATURE),
        EpsSensor(
            coordinator,
            "eps_pool_temperature",
            "Temperature",
            None,
            "temperature",
            "status.status",
            "mdi:thermometer",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 0: "heating off", 1: "no flow", 2: "heating on", 10: "E-zero on"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_lighting",
            "Lighting",
            None,
            "lighting",
            "status.status",
            "mdi:lightbulb",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 0: "off", 1: "unknown", 2: "on"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_ph_status",
            "pH Status",
            None,
            "ph",
            "status.status",
            "mdi:water-percent",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", -28: "dry run", 0: "ph ok", 103: "ph out of range", 104: "104", 201: "no flow"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_cl_status",
            "Cl Status",
            None,
            "cl",
            "status.status",
            "mdi:water-percent",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", -28: "dry run", 0: "cl ok", 103: "cl out of range", 104: "104", 201: "no flow"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_zero_e_status",
            "Zero E Status",
            None,
            "zero_e",
            "status.status",
            "mdi:flash",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 1: "active"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_cover_status",
            "Cover Status",
            None,
            "cover",
            "status.status",
            "mdi:window-shutter",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 1: "open", 2: "closed", 3: "opening", 4: "closing", 5: "semi open"},
        ),
        EpsSensor(
            coordinator,
            "eps_pool_cover_calibration",
            "Cover Calibration",
            None,
            "cover",
            "status.covco",
            "mdi:calibration",
            device_class=SensorDeviceClass.ENUM,
            options={-1: "unsupported", 0: "ok", 1: "calibration needed"},
        ),
    ]

    async_add_entities(sensors, update_before_add=True)


class EpsSensor(EpsEntity, SensorEntity):  # type: ignore[misc]
    """Representation of an EPS Smart Pool Control sensor."""

    def __init__(
        self,
        coordinator: EpsDataUpdateCoordinator,
        sensor_type: str,
        name: str,
        unit_of_measurement: str | None,
        data_key: str,
        api_field: str,
        icon: str,
        device_class: SensorDeviceClass | None = None,
        options: dict[int, str] | None = None,
        state_class: SensorStateClass | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._api_field = api_field
        self._options = options
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_options = list(options.values()) if options else None
        entry_id = coordinator.config_entry.entry_id if coordinator.config_entry else ""
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self.entity_id = f"sensor.{sensor_type}"

    @property
    def native_value(self) -> object:  # type: ignore[override]
        """Return the sensor value, mapped through options for ENUM sensors."""
        value = self._get_nested_value(self.coordinator.data.get(self._data_key, {}), self._api_field)
        if self._options and isinstance(value, int):
            return self._options.get(value, "unknown")
        if isinstance(value, float):
            return round(value, 1)
        return value

    @property
    def extra_state_attributes(self) -> dict[str, object]:  # type: ignore[override]
        """Return raw value and option list for ENUM sensors."""
        attributes: dict[str, object] = {}
        if self._options:
            value = self._get_nested_value(self.coordinator.data.get(self._data_key, {}), self._api_field)
            if value is not None:
                attributes["raw_value"] = value
            attributes["options"] = list(self._options.values())
        return attributes

    @property
    def entity_registry_enabled_default(self) -> bool:  # type: ignore[override]
        """Disable entities belonging to modules the device reports as unsupported (status -1)."""
        return self._is_module_enabled(self._data_key)
