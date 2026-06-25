# Schneider SELogic Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![GitHub License](https://img.shields.io/github/license/magicbear/schneider_selogic_hacs)

Home Assistant custom integration for Schneider Electric SELogic / PM2xxx series power meters over **Modbus/TCP**.

[English](#english) | [中文](#中文)

---

## English

### Features

- **Modbus/TCP polling** via `pymodbus`
- **Configurable sensor list** — choose which measurements to expose
- **Optimized reads** — only queries Modbus register blocks required by enabled sensors
- **Reconfigure flow** — update connection settings and sensor selection without re-adding the device
- **Energy dashboard ready** — energy sensors use `total_increasing` state class
- **Translations** — English and Simplified Chinese (`zh-Hans`)

### Supported devices

Designed for Schneider power meters that follow the PMC register map, including:

- EM6400 NG
- PM2120 / PM2130 / PM2220 / PM2230

Register addresses are based on *Public_EM6400_PM2xxx PMC Register List* (Modbus address = PMC register − 1).

### Requirements

- Home Assistant **2023.9.0** or newer
- Network access to the meter on Modbus/TCP (default port **502**)

### Installation

#### HACS (recommended)

1. Open **HACS → Integrations → ⋮ → Custom repositories**
2. Add repository: `https://github.com/magicbear/schneider_selogic_hacs`
3. Category: **Integration**
4. Install **Schneider SELogic**, restart Home Assistant
5. Go to **Settings → Devices & services → Add integration** and search for **Schneider SELogic**

#### Manual

Copy `custom_components/schneider_selogic` into your Home Assistant `config/custom_components/` directory and restart.

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| IP | — | Modbus/TCP host address |
| Port | `502` | Modbus/TCP port |
| Slave ID | `1` | Modbus unit / device ID |
| Scan Interval | `30` | Polling interval in seconds |
| Sensors | see below | Multi-select list of enabled sensors |

On first setup, the integration validates connectivity by reading the meter name register.

Use **Configure** on an existing entry to change settings or sensor selection later.

### Sensors

Each sensor can be enabled individually. `default_enabled` in `SENSOR_TYPES` controls which sensors are pre-selected on new setups.

#### Enabled by default

| Sensor | Unit | Description |
|--------|------|-------------|
| Voltage A / B / C | V | Phase-to-neutral voltage |
| Voltage AB / BC / CA | V | Line-to-line voltage |
| Current A / B / C / N | A | Phase and neutral current |
| Power Factor A / B / C / Avg | % | Power factor per phase and total |
| Frequency | Hz | Line frequency |

#### Optional (disabled by default)

| Sensor | Unit | PMC Reg. | Description |
|--------|------|----------|-------------|
| Active Power A / B / C / Total | kW | 3054–3060 | Real power |
| Reactive Power A / B / C / Total | kVAR | 3062–3068 | Reactive power |
| Apparent Power A / B / C / Total | kVA | 3070–3076 | Apparent power |
| Active Energy Delivered | kWh | 2676 | Energy into load (consumption) |
| Active Energy Received | kWh | 2678 | Energy out of load (export) |
| Active Energy Total | kWh | 2680 | Delivered + received |
| Active Energy Net | kWh | 2682 | Delivered − received |
| Reactive Energy Total | kVARh | 2688 | Reactive energy sum |
| Apparent Energy Total | kVAh | 2696 | Apparent energy sum |
| Present Demand | kW | 3766 | Current active power demand |
| Peak Demand | kW | 3770 | Peak active power demand |
| Present Reactive Demand | kVAR | 3782 | Current reactive demand |
| Present Apparent Demand | kVA | 3798 | Current apparent demand |

To change defaults for new installations, edit `default_enabled` in `custom_components/schneider_selogic/const.py`.

### Translations

Entity names are translated via `translation_key` in `translations/`:

- `en.json` — English
- `zh-Hans.json` — Simplified Chinese

Set Home Assistant language to **简体中文** to see Chinese entity names.

### Troubleshooting

| Error | Meaning |
|-------|---------|
| Unable to connect | TCP connection to host/port failed |
| Modbus communication error | Connected but register read failed |
| Unknown error | Unexpected failure during validation |

Check IP, port, slave ID, firewall rules, and that Modbus/TCP is enabled on the meter.

### Links

- [Documentation](https://github.com/magicbear/schneider_selogic)
- [Issue tracker](https://github.com/magicbear/schneider_selogic/issues)

---

## 中文

### 功能

- 通过 **Modbus/TCP**（`pymodbus`）轮询电能表数据
- **可选传感器列表** — 按需勾选要显示的测量项
- **读取优化** — 仅读取已启用传感器对应的寄存器块
- **重新配置** — 无需删除集成即可修改 IP、端口、传感器等
- **能源面板支持** — 电能传感器使用 `total_increasing`
- **多语言** — 英文、简体中文（`zh-Hans`）

### 支持设备

适用于施耐德 PMC 寄存器表的电能表，例如：

- EM6400 NG
- PM2120 / PM2130 / PM2220 / PM2230

寄存器地址依据 *Public_EM6400_PM2xxx PMC Register List*（Modbus 地址 = PMC 寄存器 − 1）。

### 安装要求

- Home Assistant **2023.9.0** 及以上
- 可通过 Modbus/TCP 访问电能表（默认端口 **502**）

### 安装步骤（HACS）

1. 进入 **HACS → 集成 → 右上角 ⋮ → 自定义仓库**
2. 仓库地址：`https://github.com/magicbear/schneider_selogic_hacs`
3. 类别选择：**集成**
4. 安装 **Schneider SELogic** 并重启 Home Assistant
5. 进入 **设置 → 设备与服务 → 添加集成**，搜索 **Schneider SELogic**

### 配置项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| IP 地址 | — | Modbus/TCP 主机地址 |
| 端口 | `502` | Modbus/TCP 端口 |
| 从站地址 | `1` | Modbus 设备 ID |
| 扫描间隔 | `30` | 轮询间隔（秒） |
| 传感器 | 见下文 | 多选启用项 |

首次配置时会读取表计名称寄存器以验证连接。已有条目可通过 **配置** 修改参数。

### 传感器

每项传感器可单独开关。`SENSOR_TYPES` 中的 `default_enabled` 控制新安装时的默认勾选项。

**默认启用：** 三相电压/线电压、三相电流及 N 线电流、功率因数、频率（共 15 项）

**默认关闭：** 有功/无功/视在功率、有功/无功/视在电能、需量等（可在配置页勾选）

修改默认选项：编辑 `custom_components/schneider_selogic/const.py` 中对应传感器的 `default_enabled`。

### 常见问题

| 错误 | 含义 |
|------|------|
| 无法连接 | TCP 连接失败 |
| Modbus 通信错误 | 已连接但寄存器读取失败 |
| 未知错误 | 验证过程中发生意外错误 |

请检查 IP、端口、从站地址、防火墙及表计 Modbus/TCP 是否已开启。

### 链接

- [文档](https://github.com/magicbear/schneider_selogic)
- [问题反馈](https://github.com/magicbear/schneider_selogic/issues)