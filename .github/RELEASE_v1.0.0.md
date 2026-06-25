## Schneider SELogic for Home Assistant — v1.0.0

First stable release. Modbus/TCP integration for Schneider SELogic / PM2xxx power meters.

### Highlights

- 37 selectable sensors (voltage, current, power, PF, frequency, energy, demand)
- Smart polling — only reads Modbus blocks for enabled sensors
- Reconfigure flow with pre-filled settings
- Energy dashboard support (`total_increasing`)
- English & Simplified Chinese translations
- Hassfest & HACS Action validated · MIT License

### Supported devices

EM6400 NG · PM2120 · PM2130 · PM2220 · PM2230

### Requirements

- Home Assistant 2023.9.0+
- pymodbus >= 3.10.0

### Install (HACS)

1. Add custom repo: `https://github.com/magicbear/schneider_selogic_hacs` (Integration)
2. Install **Schneider SELogic** and restart HA
3. Add integration via **Settings → Devices & services**

Full release notes: [RELEASE_NOTES.md](https://github.com/magicbear/schneider_selogic_hacs/blob/v1.0.0/RELEASE_NOTES.md)