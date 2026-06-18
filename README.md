# EPS Smart Pool Control

EPS Smart Pool Control is a custom component for Home Assistant that lets you monitor and control your pool, including water temperatures, pH, RX/chlorine levels, pump status, and filter schedules.

The devices and API are made and maintained by [Europe Pool Supplies (EPS)](https://epsbv.eu/). This custom HA integration is independent — I have no connection with them, I'm just a happy user of their devices.

> **Version 1.0.0** migrates to the EPS V2 API (`api.smartpoolconnect.eu`). If you are on an older version of this integration (≤ 0.0.8), you were using the V1 API which is no longer supported here. Upgrade to 1.0.0 and reconfigure with your MAC address.

## Features

- Real-time water, ambient, and IMX temperatures
- pH and RX/chlorine actual and target values
- Filter pump current and speed
- Pump mode and backwash status
- Pool volume
- Lighting and heating status
- Pool online/offline connectivity sensor
- Writable number and switch entities: pH target, RX target, water temperature target, filter schedules, pump force-on

## Example data

![Pool Control Device](https://github.com/robsonke/eps-smart-pool-control/blob/master/assets/eps-pool-example.jpg)

## Supported devices

- EPS One Touch (Salt)

Other EPS devices using the V2 API should also work. Open an issue and share your API response if you want your device explicitly listed.

## Installation

Requirements:
- API key (provided by EPS — contact their support team)
- MAC address of your pool device (visible in the EPS online portal or on the device label)

Steps:
1. Ensure you have [HACS](https://hacs.xyz/) installed in your Home Assistant setup.
2. Go to the HACS store and search for `EPS Smart Pool Control`.
3. Click the integration and select **Install**.
4. Restart Home Assistant.
5. Go to **Settings → Integrations → Add Integration**.
6. Search for **EPS Smart Pool Control** and follow the setup wizard.
7. Enter your API key and device MAC address (format: `00:14:2D:A7:56:2A`).

## Migrating from 0.0.8 (V1 API)

1. Remove the existing EPS Smart Pool Control integration from **Settings → Integrations**.
2. Install version 1.0.0 via HACS.
3. Re-add the integration and enter your API key and **MAC address** (previously called "serial number").

Because the V2 API has a different data structure, all entity IDs and sensor names have changed. After re-adding the integration you will need to:

- **Dashboards**: remove old EPS entities and re-add the new ones.
- **Automations and scripts**: update any entity references — the old entity IDs no longer exist.
- **History**: previous sensor history is not carried over to the new entities.

The old entities will show as unavailable in HA until you remove them via **Settings → Entities**.

## Contributing

Contributions are welcome — open a PR or issue.

## Local development

Follow the [HA custom component development guide](https://developers.home-assistant.io/docs/development_environment/).

```bash
# Lint and format
ruff check custom_components/
ruff format custom_components/

# Or via pre-commit
pre-commit run --all-files
```

## Disclaimer

Developed against an EPS One Touch (Salt) device. Behaviour may differ for other device types — especially for modules your device doesn't have (cover, deck, aux outputs). Entities for unsupported modules are automatically disabled when the device reports `-1`.

## License

MIT

## API example (V2)

The V2 API returns a single pool object per device. Below is a representative (redacted) response for `GET /pool/{pid}`.

```json
{
    "pid": "**redacted**",
    "name": "Pool",
    "status": "online",
    "activity_at": 1748684434000,
    "ph": {
        "metrics": { "actual": 7.3 },
        "config": { "target": 7.4 },
        "status": { "status": 0 }
    },
    "cl": {
        "metrics": { "actual": 720.0 },
        "config": { "rx": { "target": 700.0 } },
        "status": { "status": 0 }
    },
    "filter": {
        "metrics": { "pump_current": 1.2, "pump_speed": 2 },
        "config": {
            "always_active": false,
            "schedule_1": { "enabled": false },
            "schedule_2": { "enabled": false },
            "schedule_3": { "enabled": true }
        },
        "status": { "pump_status": 2 }
    },
    "temperature": {
        "metrics": { "water_temp": 26.0, "ambient_temp": 22.5, "imx_temp": 51.7 },
        "config": { "target": 28.0 },
        "status": { "status": 0 }
    },
    "lighting": {
        "status": { "status": 0 }
    },
    "backwash": {
        "status": { "status": 0 }
    },
    "spec": {
        "pool_volume": 27
    }
}
```
