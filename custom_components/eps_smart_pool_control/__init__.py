"""The EPS Smart Pool Control integration."""

from __future__ import annotations

from config.custom_components.eps_smart_pool_control.coordinator import (
    EpsDataUpdateCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import COORDINATOR, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EPS Smart Pool Control from a config entry."""
    coordinator = EpsDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    hass.data[DOMAIN][COORDINATOR] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the EPS Smart Pool Control component."""
    hass.data[DOMAIN] = {}
    return True
