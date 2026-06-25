# Release Notes

## v1.0.1 — 2026-06-25

Maintenance release after repository rename. No functional changes.

- Repository renamed from `schneider_selogic_hacs` to `schneider_selogic` (HACS naming policy)
- Updated documentation and issue tracker URLs in `manifest.json`

---

## v1.0.0 — 2026-06-25

First stable release of the Schneider SELogic Home Assistant integration.

---

### English

#### Overview

This release brings a production-ready custom integration for Schneider Electric SELogic / PM2xxx power meters over Modbus/TCP. It supports flexible sensor selection, optimized polling, reconfiguration, energy-dashboard metrics, and bilingual UI translations.

#### Highlights

- **Modbus/TCP integration** for Schneider SELogic / PM2xxx series meters
- **37 selectable sensors** — voltage, current, power, power factor, frequency, energy, and demand
- **Smart polling** — only reads Modbus register blocks required by enabled sensors
- **Reconfigure flow** — update IP, port, slave ID, scan interval, and sensor list without re-adding the device
- **Energy dashboard support** — energy sensors expose `total_increasing` state class
- **Translations** — English and Simplified Chinese (`zh-Hans`)
- **HACS ready** with validation workflows
- **MIT License**

#### Supported devices

Designed for meters following the Schneider PMC register map, including:

- EM6400 NG
- PM2120 / PM2130 / PM2220 / PM2230

Register mapping follows *Public_EM6400_PM2xxx PMC Register List* (Modbus address = PMC register − 1).

#### Sensors

**Enabled by default (15):**

- Phase and line voltages (Ua–Uc, Uab–Uca)
- Phase and neutral currents (Ia–In)
- Power factor per phase and average (PFa–PF)
- Frequency (Hz)

**Optional (22):**

- Active / reactive / apparent power (per phase and total)
- Active energy delivered, received, total, and net (kWh)
- Reactive and apparent energy totals (kVARh / kVAh)
- Present and peak demand (kW / kVAR / kVA)

Each sensor includes a `default_enabled` flag in `SENSOR_TYPES` for customizing factory defaults.

#### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| IP | — | Modbus/TCP host |
| Port | 502 | Modbus/TCP port |
| Slave ID | 1 | Modbus unit ID |
| Scan Interval | 30 s | Polling interval |
| Sensors | 15 defaults | Multi-select sensor list |

#### Requirements

- Home Assistant **2023.9.0** or newer
- `pymodbus>=3.10.0`
- Network access to the meter on Modbus/TCP

#### Installation

**HACS:** Add custom repository `https://github.com/magicbear/schneider_selogic` (category: Integration), install, restart, then add the integration via **Settings → Devices & services**.

**Manual:** Copy `custom_components/schneider_selogic` to `config/custom_components/` and restart.

#### Full changelog

- Initial stable release with config flow and sensor platform
- Add selectable sensor list with per-sensor `default_enabled` flag
- Add power, energy, and demand sensors from PMC register map
- Optimize coordinator to skip disabled Modbus register blocks
- Fix reconfigure flow to pre-fill existing settings and update entry in place
- Fix entity `translation_key` for proper en / zh-Hans localization
- Expand README with full configuration and sensor reference
- Add MIT License

#### Links

- Repository: https://github.com/magicbear/schneider_selogic
- Documentation: https://github.com/magicbear/schneider_selogic
- Issues: https://github.com/magicbear/schneider_selogic/issues

---

### 中文

#### 概述

这是施耐德 SELogic / PM2xxx 系列电能表 Home Assistant 集成的首个稳定版本，通过 Modbus/TCP 采集数据，支持传感器自选、读取优化、重新配置、能源面板及中英双语界面。

#### 主要特性

- **Modbus/TCP 接入** — 支持施耐德 SELogic / PM2xxx 系列电能表
- **37 项可选传感器** — 电压、电流、功率、功率因数、频率、电能、需量
- **智能轮询** — 仅读取已启用传感器对应的寄存器块
- **重新配置** — 无需删除集成即可修改 IP、端口、从站地址、扫描间隔和传感器列表
- **能源面板** — 电能传感器支持 `total_increasing`
- **多语言** — 英文、简体中文（`zh-Hans`）
- **HACS 支持**，含验证工作流
- **MIT 开源协议**

#### 支持设备

- EM6400 NG
- PM2120 / PM2130 / PM2220 / PM2230

寄存器地址依据 *Public_EM6400_PM2xxx PMC Register List*（Modbus 地址 = PMC 寄存器 − 1）。

#### 传感器

**默认启用（15 项）：** 三相电压/线电压、三相电流及 N 线、功率因数、频率

**可选（22 项）：** 有功/无功/视在功率、有功/无功/视在电能、当前及峰值需量

可在 `SENSOR_TYPES` 中通过 `default_enabled` 自定义新安装的默认勾选项。

#### 配置项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| IP 地址 | — | Modbus/TCP 主机 |
| 端口 | 502 | Modbus/TCP 端口 |
| 从站地址 | 1 | Modbus 设备 ID |
| 扫描间隔 | 30 秒 | 轮询间隔 |
| 传感器 | 15 项默认 | 多选列表 |

#### 系统要求

- Home Assistant **2023.9.0** 及以上
- `pymodbus>=3.10.0`
- 可通过 Modbus/TCP 访问电能表

#### 安装

**HACS：** 添加自定义仓库 `https://github.com/magicbear/schneider_selogic`（类别：集成），安装并重启后，在 **设置 → 设备与服务** 中添加集成。

**手动：** 将 `custom_components/schneider_selogic` 复制到 `config/custom_components/` 并重启。

#### 完整更新记录

- 首个稳定版，包含配置流程与传感器平台
- 新增可选传感器列表及 `default_enabled` 默认控制
- 新增功率、电能、需量传感器（PMC 寄存器表）
- 协调器优化：跳过未启用传感器对应的 Modbus 读取
- 修复重新配置流程：回填已有配置并原地更新条目
- 修复实体 `translation_key`，正确加载中英文翻译
- 完善 README 安装、配置与传感器说明
- 添加 MIT License

#### 链接

- 仓库：https://github.com/magicbear/schneider_selogic
- 文档：https://github.com/magicbear/schneider_selogic
- 反馈：https://github.com/magicbear/schneider_selogic/issues