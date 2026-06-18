# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Lint and format:**
```bash
# Run linter
ruff check custom_components/

# Run formatter
ruff format custom_components/

# Run both (via pre-commit)
pre-commit run --all-files
```

**Install dependencies (for development):**
```bash
pip install -r requirements.txt
```

No test suite exists yet — testing is done by loading the integration in a real Home Assistant instance.

## Architecture

This is a [Home Assistant](https://www.home-assistant.io/) custom component (`iot_class: cloud_polling`) that integrates with the EPS Smart Pool Control API at `https://api.smartpoolcontrol.eu/publicapi/`.

### Data flow

`EpsDataUpdateCoordinator` (in [coordinator.py](custom_components/eps_smart_pool_control/coordinator.py)) is the central data manager. It polls 4 API endpoints every 5 minutes and stores results as a dict:
```python
{
    "realtimedata": {...},   # water/ambient/solar temps, pH, RX, errors
    "status": {...},         # cover, pump, filter, lighting states
    "configuration": {...},  # device capabilities and pool volume
    "settings": {...},       # nested settings_rx, settings_ph, settings_filterschedule*, etc.
}
```
Write operations use `set_value(endpoint, nested_data)`, which fetches the current state, merges the change, then PUTs to `/{endpoint}/{pool_id}`.

### Entity pattern

`EpsEntity` ([eps_entity.py](custom_components/eps_smart_pool_control/eps_entity.py)) is the base class. It provides:
- `device_info` — groups all entities under one device per serial number
- `_get_nested_value(data, key_path)` — resolves dot-separated paths like `"settings_rx.rx_value_target"` into nested dicts

Each platform file (`sensor.py`, `binary_sensor.py`, `number.py`, `switch.py`) creates entity instances by passing `data_key` (top-level coordinator dict key) and `api_field` (dot-path within that key).

### Entity types and status

| Platform | Purpose | Write support |
|---|---|---|
| `sensor.py` | Read-only values (temperatures, pH, RX, pump mode/speed, cover) | No |
| `binary_sensor.py` | Boolean states (errors, flow, pool online check) | No |
| `number.py` | RX target, pH target, water temperature target | Disabled by default |
| `switch.py` | Filter schedules, pump force-on | Disabled by default |

Number and switch entities are registered with `_attr_entity_registry_enabled_default = False` because the write API is not yet confirmed working.

`EpsPoolOnlineBinarySensor` is a special subclass that derives connectivity from the `date_time` field in `realtimedata` — it returns `True` if the last API timestamp is within 4 hours.

### Sensor values with `-1`

Status API fields return `-1` to indicate "unsupported" on the connected device. `EpsSensor.entity_registry_enabled_default` disables the entity automatically when the current value is `-1`.

### Config flow

Setup requires two fields: `api_key` and `serialnumber`. Both are stored in `entry.data` and used in every API call as query parameters.

## Code style

- Python 3.12, `ruff` with `select = ["ALL"]` (line length 200)
- Type annotations required; `typing.Any` is allowed
- Max function args: 10, max complexity: 25
