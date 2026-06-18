"""The image platform for the EPS Smart Pool Control integration."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from homeassistant.components.image import ImageEntity

from .eps_entity import EpsEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EpsDataUpdateCoordinator


async def async_setup_entry(_hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up EPS Smart Pool Control image based on a config entry."""
    coordinator: EpsDataUpdateCoordinator = entry.runtime_data
    async_add_entities([EpsPoolImageEntity(coordinator)], update_before_add=True)


class EpsPoolImageEntity(EpsEntity, ImageEntity):  # type: ignore[misc]
    """Image entity showing the pool avatar from the V2 API."""

    _attr_name = "Pool Avatar"
    _attr_content_type = "image/jpeg"

    def __init__(self, coordinator: EpsDataUpdateCoordinator) -> None:
        """Initialize the image entity."""
        EpsEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, coordinator.hass)
        self.entity_id = "image.eps_pool_avatar"
        entry_id = coordinator.config_entry.entry_id if coordinator.config_entry else ""
        self._attr_unique_id = f"{entry_id}_eps_pool_avatar"
        self._attr_image_last_updated = datetime.now(UTC)

    @property
    def image_url(self) -> str | None:  # type: ignore[override]
        """Return the avatar URL from the pool API response."""
        return self.coordinator.data.get("avatar")
