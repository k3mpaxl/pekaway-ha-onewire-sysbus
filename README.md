# 1-Wire SysBus Temperature Sensors — Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-%E2%89%A52024.10-blue)](https://www.home-assistant.io/)
[![Validate](https://github.com/k3mpaxl/pekaway-ha-onewire-sysbus/actions/workflows/validate.yml/badge.svg)](https://github.com/k3mpaxl/pekaway-ha-onewire-sysbus/actions/workflows/validate.yml)

Read **DS18B20** 1-Wire temperature sensors directly from the Linux sysfs bus (`/sys/bus/w1/devices`).

> Part of the [Pekaway VAN PI CORE](https://github.com/k3mpaxl/pekaway-vanpi-homeassistant) integration family.
>
> Based on the work of [thecode](https://github.com/thecode/ha-onewire-sysbus).

## Features

- Automatic sensor discovery (`28-*` prefix)
- Up to 5 DS18B20 sensors
- Configurable mount directory

## Prerequisites

| | |
|---|---|
| **Hardware** | DS18B20 sensors on 1-Wire bus |
| **Raspberry Pi** | `dtoverlay=w1-gpio` in `config.txt` |
| **Home Assistant** | ≥ 2024.10 |

## Installation via HACS

1. **HACS** → **Integrations** → three dots → **Custom repositories**
2. Add: `https://github.com/k3mpaxl/pekaway-ha-onewire-sysbus` → **Integration**
3. Install **1-Wire SysBus**, restart Home Assistant.

## Setup

1. **Settings → Devices & Services → + Add Integration**
2. Search for **1-Wire SysBus**
3. Enter the sysfs mount directory (default `/sys/bus/w1/devices`)
4. Detected sensors are added automatically.

## Removal

1. **Settings → Devices & Services** → click the integration → **Delete**
2. Optionally uninstall via HACS.

## License

MIT — see [LICENSE](./LICENSE).
