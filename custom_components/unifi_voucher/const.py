"""Constants for UniFi Hotspot Manager integration."""
from logging import getLogger

from homeassistant.const import (
    Platform,
)

LOGGER = getLogger(__package__)

DOMAIN = "unifi_voucher"
MANUFACTURER = "Ubiquiti Networks"

PLATFORMS = [
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SENSOR,
]

UPDATE_INTERVAL = 300

CONF_SITE_ID = "site_id"
CONF_WLAN_NAME = "wlan_name"
CONF_VOUCHER_NUMBER = "voucher_number"
CONF_VOUCHER_QUOTA = "voucher_quota"
CONF_VOUCHER_EXPIRE = "voucher_expire"

ATTR_EXTRA_STATE_ATTRIBUTES = "extra_state_attributes"
ATTR_LAST_PULL = "last_pull"
ATTR_AVAILABLE = "available"
ATTR_VOUCHER = "voucher"

DEFAULT_SITE_ID = "default"
DEFAULT_HOST = ""
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""
DEFAULT_PORT = 443
DEFAULT_VERIFY_SSL = False
DEFAULT_VOUCHER = {
    CONF_VOUCHER_NUMBER: {
        "default": 1,
        "min": 1,
        "max": 10000,
    },
    CONF_VOUCHER_QUOTA: {
        "default": 1,
        "min": 0,
        "max": 10000,
    },
    CONF_VOUCHER_EXPIRE: {
        "default": 480,
        "min": 1,
        "max": 1000000,
        "step": 1,
        "scale": 60,
    },
}
