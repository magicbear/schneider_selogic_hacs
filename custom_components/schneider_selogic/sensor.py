# sensor.py
import logging
from datetime import timedelta

from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from pymodbus.client import AsyncModbusTcpClient
from .const import (
    BLOCK_SENSOR_KEYS,
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_SLAVE_ID,
    DEFAULT_SENSORS,
    DOMAIN,
    POWER_FACTOR_SENSOR_KEYS,
    REGISTER_BLOCKS,
    SENSOR_BLOCK_INDEX,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = SELogicDataCoordinator(hass, config_entry)

    await coordinator.async_config_entry_first_refresh()

    if not isinstance(coordinator.update_interval, timedelta):
        raise ValueError("Invalid update interval type")

    enabled_sensors = set(config_entry.data.get(CONF_SENSORS, DEFAULT_SENSORS))
    sensors = [
        SELogicSensor(coordinator, name, key, unit, device_class, state_class)
        for name, key, unit, device_class, state_class, _default_enabled in SENSOR_TYPES
        if key in enabled_sensors
    ]

    async_add_entities(sensors)


class SELogicSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, unit, device_class, state_class):
        self.entity_description = SensorEntityDescription(
            key=key,
            translation_key=key.lower(),
            name=None,
            device_class=device_class,
            native_unit_of_measurement=unit,
            has_entity_name=True,
            suggested_display_precision=2,
            state_class=state_class,
        )
        super().__init__(coordinator, key)
        self._attr_device_info = coordinator.device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        """处理来自协调器的更新数据。"""
        self.async_write_ha_state()

    @property
    def native_value(self):
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def unique_id(self):
        return f"{self.entity_description.key.lower()}"


class SELogicDataCoordinator(DataUpdateCoordinator):
    """异步数据协调器"""

    def __init__(self, hass, config_entry):
        host, port, slave_id = config_entry.data[CONF_HOST], config_entry.data[CONF_PORT], config_entry.data[CONF_SLAVE_ID]
        super().__init__(
            hass,
            logger=_LOGGER,
            name="SELogic Power Meter",
            update_interval=timedelta(seconds=config_entry.data[CONF_SCAN_INTERVAL]),
        )
        self.client = AsyncModbusTcpClient(
            host=host,
            port=port,
            timeout=10,
        )
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name="SELogic Power Meter",
            manufacturer=None,
            model=None,
        )
        self.slave_id = slave_id
        self.enabled_sensors = set(config_entry.data.get(CONF_SENSORS, DEFAULT_SENSORS))
        self.data = {}

    def convert_pf(self, pf_register):
        if 0 <= pf_register <= 1:
            return pf_register
        if -2 <= pf_register <= -1:
            return -2 - pf_register
        if -1 < pf_register <= 0:
            return pf_register
        if 1 < pf_register < 2:
            return 2 - pf_register
        raise ValueError("PF register value out of expected range (-2 to 2)")

    def _needs_block_read(self, block_name: str) -> bool:
        block_keys = BLOCK_SENSOR_KEYS.get(block_name, frozenset())
        return bool(self.enabled_sensors & block_keys)

    async def _read_float32_block(self, block_name: str) -> list[float] | None:
        block = REGISTER_BLOCKS[block_name]
        result = await self.client.read_holding_registers(
            address=block["address"],
            count=block["count"],
            device_id=self.slave_id,
        )
        if result.isError():
            self.logger.error("Register read error (%s): %s", block_name, result)
            return None

        values = self.client.convert_from_registers(
            result.registers,
            data_type=self.client.DATATYPE.FLOAT32,
            word_order="big",
        )
        if not isinstance(values, list):
            return [values]
        return values

    def _value_from_block(self, sensor_key: str, values: list[float]) -> float:
        _block_name, index = SENSOR_BLOCK_INDEX[sensor_key]
        value = values[index]
        if sensor_key in POWER_FACTOR_SENSOR_KEYS:
            return self.convert_pf(value) * 100
        return value

    async def _async_update_data(self):
        """异步获取所有数据"""
        try:
            if not self.client.connected:
                await self.client.connect()

            if not self.client.connected:
                raise ConnectionError("Connection lost")

            if self.device_info["model"] is None:
                result = await self.client.read_holding_registers(address=49, count=20, device_id=self.slave_id)
                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info["model"] = self.client.convert_from_registers(
                    result.registers,
                    data_type=self.client.DATATYPE.STRING,
                    word_order="big",
                )

                result = await self.client.read_holding_registers(address=69, count=20, device_id=self.slave_id)
                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info["manufacturer"] = self.client.convert_from_registers(
                    result.registers,
                    data_type=self.client.DATATYPE.STRING,
                    word_order="big",
                )

                result = await self.client.read_holding_registers(address=129, count=2, device_id=self.slave_id)
                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info["serial_number"] = self.client.convert_from_registers(
                    result.registers,
                    data_type=self.client.DATATYPE.UINT32,
                    word_order="big",
                )

                result = await self.client.read_holding_registers(address=135, count=1, device_id=self.slave_id)
                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info["hw_version"] = self.client.convert_from_registers(
                    result.registers,
                    data_type=self.client.DATATYPE.UINT16,
                    word_order="big",
                )

            data = {}
            block_values: dict[str, list[float]] = {}

            for block_name in REGISTER_BLOCKS:
                if not self._needs_block_read(block_name):
                    continue
                values = await self._read_float32_block(block_name)
                if values is None:
                    return None
                block_values[block_name] = values

            for sensor_key in self.enabled_sensors:
                if sensor_key not in SENSOR_BLOCK_INDEX:
                    continue
                block_name, _index = SENSOR_BLOCK_INDEX[sensor_key]
                data[sensor_key] = self._value_from_block(sensor_key, block_values[block_name])

            self.data = data
            self.client.close()
            return self.data
        except Exception as e:
            self.logger.error("Update failed: %s", str(e))
            self.client.close()
            raise