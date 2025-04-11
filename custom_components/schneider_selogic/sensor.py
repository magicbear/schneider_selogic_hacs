# sensor.py
import logging
from datetime import timedelta

from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.constants import Endian
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_SLAVE_ID, CONF_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = [
    ("Voltage A", "Ua", "V", SensorDeviceClass.VOLTAGE),
    ("Voltage B", "Ub", "V", SensorDeviceClass.VOLTAGE),
    ("Voltage C", "Uc", "V", SensorDeviceClass.VOLTAGE),
    ("Voltage AB", "Uab", "V", SensorDeviceClass.VOLTAGE),
    ("Voltage BC", "Ubc", "V", SensorDeviceClass.VOLTAGE),
    ("Voltage CA", "Uca", "V", SensorDeviceClass.VOLTAGE),
    ("Current A", "Ia", "A", SensorDeviceClass.CURRENT),
    ("Current B", "Ib", "A", SensorDeviceClass.CURRENT),
    ("Current C", "Ic", "A", SensorDeviceClass.CURRENT),
    ("Current N", "In", "A", SensorDeviceClass.CURRENT),
    ("Power Factor A", "PFa", "%", SensorDeviceClass.POWER_FACTOR),
    ("Power Factor B", "PFb", "%", SensorDeviceClass.POWER_FACTOR),
    ("Power Factor C", "PFc", "%", SensorDeviceClass.POWER_FACTOR),
    ("Power Factor Avg", "PF", "%", SensorDeviceClass.POWER_FACTOR),
    ("Frequency", "Freq", "Hz", SensorDeviceClass.FREQUENCY),

]


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = SELogicDataCoordinator(hass, config_entry)

    # 确保协调器已初始化
    await coordinator.async_config_entry_first_refresh()

    # 确保update_interval类型正确
    if not isinstance(coordinator.update_interval, timedelta):
        raise ValueError("Invalid update interval type")

    sensors = []
    for name, key, unit, device_class in SENSOR_TYPES:
        sensors.append(
            SELogicSensor(coordinator, name, key, unit, device_class)
        )

    async_add_entities(sensors)


class SELogicSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, unit, device_class):
        super().__init__(coordinator, key)
        self._attr_device_info = coordinator.device_info
        self._attr_translation_key = key
        self.entity_description = SensorEntityDescription(
            key=key,
            name=name,
            device_class=device_class,
            native_unit_of_measurement=unit,
            has_entity_name=True,
            suggested_display_precision=2
        )

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
            timeout=10
        )
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name= "SELogic Power Meter",
            manufacturer=None,
            model=None
        )
        self.slave_id = slave_id
        self.data = {}

    def convert_pf(self, pf_register):
        if 0 <= pf_register <= 1:
            return pf_register
        elif -2 <= pf_register <= -1:
            return -2 - pf_register
        elif -1 < pf_register <= 0:
            return pf_register
        elif 1 < pf_register < 2:
            return 2 - pf_register
        else:
            raise ValueError("PF register value out of expected range (-2 to 2)")

    async def _async_update_data(self):
        """异步获取所有数据"""
        try:
            # 连接检查
            if not self.client.connected:
                await self.client.connect()

            if not self.client.connected:
                raise Exception("Connection lost")

            if self.device_info['model'] is None:
                result = await self.client.read_holding_registers(address=49, count=20, slave=self.slave_id)

                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info['model'] = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.STRING, word_order=Endian.BIG)

                result = await self.client.read_holding_registers(address=69, count=20, slave=self.slave_id)

                if result.isError():
                    self.logger.error("Status register read error: %s", result)
                    return None

                self.device_info['manufacturer'] = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.STRING, word_order=Endian.BIG)

            # 读取 Voltage
            result = await self.client.read_holding_registers(address=3019, count=14, slave=self.slave_id)

            if result.isError():
                self.logger.error("Status register read error: %s", result)
                return None

            voltages = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.FLOAT32, word_order=Endian.BIG)

            # 读取Current
            result = await self.client.read_holding_registers(address=2999, count=8, slave=self.slave_id)

            if result.isError():
                self.logger.error("Status register read error: %s", result)
                return None

            currents = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.FLOAT32, word_order=Endian.BIG)

            # 读取Current
            result = await self.client.read_holding_registers(address=3077, count=8, slave=self.slave_id)

            if result.isError():
                self.logger.error("Status register read error: %s", result)
                return None

            powerfactor = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.FLOAT32, word_order=Endian.BIG)

            # 读取Current
            result = await self.client.read_holding_registers(address=3109, count=2, slave=self.slave_id)

            if result.isError():
                self.logger.error("Status register read error: %s", result)
                return None

            freq = self.client.convert_from_registers(result.registers, data_type=self.client.DATATYPE.FLOAT32, word_order=Endian.BIG)

            # 构造完整数据集
            self.data = {
                'Ia': currents[0],
                'Ib': currents[1],
                'Ic': currents[2],
                'In': currents[3],
                'Uab': voltages[0],
                'Ubc': voltages[1],
                'Uca': voltages[2],
                'Ua': voltages[4],
                'Ub': voltages[5],
                'Uc': voltages[6],
                'PFa': self.convert_pf(powerfactor[0])*100,
                'PFb': self.convert_pf(powerfactor[1])*100,
                'PFc': self.convert_pf(powerfactor[2])*100,
                'PF': self.convert_pf(powerfactor[3])*100,
                'Freq': freq
            }

            self.client.close()
            return self.data
        except Exception as e:
            self.logger.error("Update failed: %s", str(e))
            self.client.close()
            raise

