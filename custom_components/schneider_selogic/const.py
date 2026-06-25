# const.py

from datetime import timedelta

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

DOMAIN = "schneider_selogic"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
SCAN_INTERVAL = timedelta(seconds=1)  # seconds

CONF_SLAVE_ID = "slave_id"
CONF_SENSORS = "sensors"
DEFAULT_SCAN_INTERVAL = 30

ERRORS_MAP = {
    "cannot_connect": "无法连接",
    "modbus_error": "Modbus通信错误",
    "invalid_auth": "认证错误",
    "unknown": "未知错误",
}

# (name, key, unit, device_class, state_class, default_enabled)
SENSOR_TYPES = [
    ("Voltage A", "Ua", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Voltage B", "Ub", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Voltage C", "Uc", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Voltage AB", "Uab", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Voltage BC", "Ubc", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Voltage CA", "Uca", "V", SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT, True),
    ("Current A", "Ia", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, True),
    ("Current B", "Ib", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, True),
    ("Current C", "Ic", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, True),
    ("Current N", "In", "A", SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT, True),
    ("Active Power A", "Pa", "kW", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, False),
    ("Active Power B", "Pb", "kW", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, False),
    ("Active Power C", "Pc", "kW", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, False),
    ("Active Power Total", "P", "kW", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT, False),
    ("Reactive Power A", "Qa", "kVAR", SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, False),
    ("Reactive Power B", "Qb", "kVAR", SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, False),
    ("Reactive Power C", "Qc", "kVAR", SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, False),
    ("Reactive Power Total", "Q", "kVAR", SensorDeviceClass.REACTIVE_POWER, SensorStateClass.MEASUREMENT, False),
    ("Apparent Power A", "Sa", "kVA", SensorDeviceClass.APPARENT_POWER, SensorStateClass.MEASUREMENT, False),
    ("Apparent Power B", "Sb", "kVA", SensorDeviceClass.APPARENT_POWER, SensorStateClass.MEASUREMENT, False),
    ("Apparent Power C", "Sc", "kVA", SensorDeviceClass.APPARENT_POWER, SensorStateClass.MEASUREMENT, False),
    ("Apparent Power Total", "S", "kVA", SensorDeviceClass.APPARENT_POWER, SensorStateClass.MEASUREMENT, False),
    ("Power Factor A", "PFa", "%", SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, True),
    ("Power Factor B", "PFb", "%", SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, True),
    ("Power Factor C", "PFc", "%", SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, True),
    ("Power Factor Avg", "PF", "%", SensorDeviceClass.POWER_FACTOR, SensorStateClass.MEASUREMENT, True),
    ("Frequency", "Freq", "Hz", SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT, True),
    (
        "Active Energy Delivered",
        "E_in",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Active Energy Received",
        "E_out",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Active Energy Total",
        "E_sum",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Active Energy Net",
        "E_net",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Reactive Energy Total",
        "E_var_sum",
        "kVARh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Apparent Energy Total",
        "E_va_sum",
        "kVAh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        False,
    ),
    (
        "Present Demand",
        "D_P",
        "kW",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
        False,
    ),
    (
        "Peak Demand",
        "D_P_peak",
        "kW",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
        False,
    ),
    (
        "Present Reactive Demand",
        "D_Q",
        "kVAR",
        SensorDeviceClass.REACTIVE_POWER,
        SensorStateClass.MEASUREMENT,
        False,
    ),
    (
        "Present Apparent Demand",
        "D_S",
        "kVA",
        SensorDeviceClass.APPARENT_POWER,
        SensorStateClass.MEASUREMENT,
        False,
    ),
]

SENSOR_OPTIONS = {
    key: name for name, key, _unit, _device_class, _state_class, _default_enabled in SENSOR_TYPES
}
DEFAULT_SENSORS = [
    key
    for _name, key, _unit, _device_class, _state_class, default_enabled in SENSOR_TYPES
    if default_enabled
]

# Modbus address = PMC register - 1
REGISTER_BLOCKS = {
    "voltage": {"address": 3019, "count": 14},
    "current": {"address": 2999, "count": 8},
    "power": {"address": 3053, "count": 24},
    "power_factor": {"address": 3077, "count": 8},
    "frequency": {"address": 3109, "count": 2},
    "energy": {"address": 2675, "count": 24},
    "demand_active": {"address": 3763, "count": 8},
    "demand_reactive": {"address": 3779, "count": 8},
    "demand_apparent": {"address": 3795, "count": 8},
}

SENSOR_BLOCK_INDEX: dict[str, tuple[str, int]] = {
    "Ia": ("current", 0),
    "Ib": ("current", 1),
    "Ic": ("current", 2),
    "In": ("current", 3),
    "Uab": ("voltage", 0),
    "Ubc": ("voltage", 1),
    "Uca": ("voltage", 2),
    "Ua": ("voltage", 4),
    "Ub": ("voltage", 5),
    "Uc": ("voltage", 6),
    "Pa": ("power", 0),
    "Pb": ("power", 1),
    "Pc": ("power", 2),
    "P": ("power", 3),
    "Qa": ("power", 4),
    "Qb": ("power", 5),
    "Qc": ("power", 6),
    "Q": ("power", 7),
    "Sa": ("power", 8),
    "Sb": ("power", 9),
    "Sc": ("power", 10),
    "S": ("power", 11),
    "PFa": ("power_factor", 0),
    "PFb": ("power_factor", 1),
    "PFc": ("power_factor", 2),
    "PF": ("power_factor", 3),
    "Freq": ("frequency", 0),
    "E_in": ("energy", 0),
    "E_out": ("energy", 1),
    "E_sum": ("energy", 2),
    "E_net": ("energy", 3),
    "E_var_sum": ("energy", 6),
    "E_va_sum": ("energy", 10),
    "D_P": ("demand_active", 1),
    "D_P_peak": ("demand_active", 3),
    "D_Q": ("demand_reactive", 1),
    "D_S": ("demand_apparent", 1),
}

BLOCK_SENSOR_KEYS: dict[str, frozenset[str]] = {}
for sensor_key, (block_name, _index) in SENSOR_BLOCK_INDEX.items():
    BLOCK_SENSOR_KEYS.setdefault(block_name, set()).add(sensor_key)
BLOCK_SENSOR_KEYS = {block: frozenset(keys) for block, keys in BLOCK_SENSOR_KEYS.items()}

POWER_FACTOR_SENSOR_KEYS = frozenset({"PFa", "PFb", "PFc", "PF"})