"""UniFi Hotspot Manager button platform."""
from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
)
from .coordinator import UnifiVoucherCoordinator
from .entity import UnifiVoucherEntity


@dataclass
class UnifiVoucherButtonDescriptionMixin:
    """Mixin to describe a UniFi Hotspot Manager button entity."""

    press_action: Callable[[UnifiVoucherCoordinator], Coroutine]


@dataclass
class UnifiVoucherButtonDescription(
    ButtonEntityDescription,
    UnifiVoucherButtonDescriptionMixin,
):
    """UniFi Hotspot Manager button description."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Entity,
) -> None:
    """Do setup buttons from a config entry created in the integrations UI."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entity_descriptions = [
        # TODO
        #UnifiVoucherButtonDescription(
        #    key=ATTR_REBOOT,
        #    translation_key=ATTR_REBOOT,
        #    device_class=ButtonDeviceClass.RESTART,
        #    press_action=lambda coordinator: coordinator.async_reboot(),
        #),
    ]

    async_add_entities(
        [
            UnifiVoucherButton(
                coordinator=coordinator,
                entity_description=entity_description,
            )
            for entity_description in entity_descriptions
        ],
        update_before_add=True,
    )


class UnifiVoucherButton(UnifiVoucherEntity, ButtonEntity):
    """Representation of a UniFi Hotspot Manager button."""

    def __init__(
        self,
        coordinator: UnifiVoucherCoordinator,
        entity_description: UnifiVoucherButtonDescription,
    ) -> None:
        """Initialize the button class."""
        super().__init__(
            coordinator=coordinator,
            entity_type="button",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description

    async def async_press(self) -> None:
        """Trigger the button action."""
        await self.entity_description.press_action(self.coordinator)
