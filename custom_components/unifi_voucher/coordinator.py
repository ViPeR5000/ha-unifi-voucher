"""DataUpdateCoordinator for UniFi Hotspot Manager."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
import homeassistant.util.dt as dt_util

from .const import (
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_VERIFY_SSL,
    DEFAULT_SITE_ID,
    CONF_SITE_ID,
    ATTR_AVAILABLE,
    ATTR_LAST_PULL,
)
from .api import (
    UnifiVoucherApiClient,
    UnifiVoucherListRequest,
    UnifiVoucherCreateRequest,
    UnifiVoucherApiAuthenticationError,
    UnifiVoucherApiConnectionError,
    UnifiVoucherApiError,
)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class UnifiVoucherCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the UniFi Hotspot Manager."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        update_interval: timedelta = timedelta(seconds=UPDATE_INTERVAL),
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.config_entry = config_entry
        self.api = UnifiVoucherApiClient(
            hass,
            host=config_entry.data.get(CONF_HOST, DEFAULT_HOST),
            username=config_entry.data.get(CONF_USERNAME, ""),
            password=config_entry.data.get(CONF_PASSWORD, ""),
            port=int(config_entry.data.get(CONF_PORT, DEFAULT_PORT)),
            site_id=config_entry.data.get(CONF_SITE_ID, DEFAULT_SITE_ID),
            verify_ssl=config_entry.data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
        )
        self._last_pull = None

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        _available = False
        _data = {}
        try:
            self._last_pull = dt_util.now()
            _available = True
            
            foo = await self.api.request(UnifiVoucherListRequest.create())
            LOGGER.debug(foo)
            
        # TODO
        #except (UnifiVoucherClientTimeoutError, UnifiVoucherClientCommunicationError, UnifiVoucherClientAuthenticationError) as exception:
        #    LOGGER.error(str(exception))
        except Exception as exception:
            LOGGER.exception(exception)

        _data.update(
            {
                ATTR_LAST_PULL: self._last_pull,
                ATTR_AVAILABLE: _available,
            }
        )
        return _data
