# EPS Smart Pool Control

EPS Smart Pool Control is a custom component for Home Assistant that allows you to monitor and control various aspects of your pool, including water temperature, pH levels, and pump settings.
The devices and API's are made and maintained by [Europe Pool Supplies (EPS)](https://epsbv.eu/). This custom HA integration is totally independent and I have no connection with them, I'm just a happy user of their devices.
They offer an online portal where you can monitor your pool as well, that's to be found here: https://owner.smartpoolcontrol.eu.

## Features

- Status overview of the most important data fields
- Update of PH and RX target values

## Example data

![Pool Control Device](https://github.com/robsonke/eps-smart-pool-control/blob/master/assets/eps-pool-example.jpg)

### Todo
- Configuration settings (implemented but not able to test)
- Add tests with different sets of mock data
- Customizable settings for lighting, timers, auxiliary controls, temperature, etc


## Disclaimer

This is made with the best intentions but totally focussed on the situation that my device provides. Since I only control Ph and RX values with the EPS One Touch and not use any of the lighs, deck, aux, etc options. I'm open to extend this for other situations, please create an issue and provide your API responses.
And, while developing the initial version, our pool was in winter sleep. I will retest this in Spring 2025.

## Supported devices

- EPS One Touch (Salt)

Note: share your API responses with me and I'll add it. Or create a pr.

## Installation

Requirements:
- API key (provided by EPS, contact their support team)
- Your pool serialnumber (can be found in [the online portal](https://owner.smartpoolcontrol.eu/login/))

Steps:
1. Ensure you have [HACS](https://hacs.xyz/) installed in your Home Assistant setup.
2. Go to the HACS store and search for `EPS Smart Pool Control`.
3. Click on the `EPS Smart Pool Control` integration and select "Install".
4. Restart Home Assistant to load the new integration.
5. Go to the Home Assistant Configuration panel.
6. Click on "Integrations".
7. Click on the "+" button to add a new integration.
8. Search for "EPS Smart Pool Control" and follow the on-screen instructions to complete the setup.

## Usage

Once installed, you can access the EPS Smart Pool Control component from the Home Assistant interface. Use the provided settings to monitor and control your pool's parameters.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.

## API Examples

Below you will find examples of what the API returns in my situation. This can be very different depending on your device type.

### Real-time Data

The real-time data provides current information about your pool's status.
API: https://api.smartpoolcontrol.eu/publicapi/realtimedata

```json
{
    "serialnumber": "**redacted**",
    "water_temperature": 26.0,
    "ambient_temperature": 0.0,
    "solar_temperature": 0.0,
    "filterpump_current": 0.0,
    "ph_actual": 6.6,
    "rx_actual": 750.0,
    "tds_ppm": 0,
    "pollution_degree_ppm": 0,
    "conductivity": 0.0,
    "clm_ppm": 0.0,
    "empty_tank": false,
    "imx_temperature": 51.7,
    "main_temperature": 35.87,
    "date_time": "2024-10-17T14:08:36.170290Z",
    "error": 0
}
```

### Status

The status section provides an overview of the current state of various pool components.
API: https://api.smartpoolcontrol.eu/publicapi/status

```json
{
    "id": 737,
    "serialnumber": "**redacted**",
    "cover": -1,
    "cover_error": 0,
    "filter": 0,
    "temperature": -1,
    "lighting": -1,
    "waterheight": -1,
    "aux1": -1,
    "aux2": -1,
    "aux3": -1,
    "aux4": -1,
    "ph": 201,
    "rx": 201,
    "clm": 1,
    "t_water": 1,
    "t_ambient": 1,
    "t_solar": 1,
    "level": 1,
    "tds": 1,
    "empty": 1,
    "pump": 0,
    "pumpspeed": 0,
    "backwash": 0,
    "flow": 0,
    "datetime": "2024-10-17T14:05:21.054000Z",
    "poolsetting": 737
}
```

### Configuration

The configuration section allows you to set up various parameters for your pool.
API: https://api.smartpoolcontrol.eu/publicapi/configuration

```json
{
    "serialnumber": "**redacted**",
    "is_dirty": false,
    "volume_pool_m3": 27,
    "io_control_available": false,
    "main_eh_control_available": false,
    "tds_sensor_available": false,
    "water_level_sensor_available": false,
    "clm_sensor_available": false,
    "external_off_available": false,
    "deck_available": false,
    "covco_deck_available": false,
    "pump_type": 0,
    "backwash_valve_type": 0,
    "sewer_config": 0,
    "filterpump_stl": false,
    "watertemperature_protection": false
}
```

### Settings

The settings section allows you to customize various aspects of your pool's operation.
API: https://api.smartpoolcontrol.eu/publicapi/settings

```json
{
    "settings_general": {
        "serialnumber": "**redacted**",
        "general_pause": false,
        "general_flow_alarm": true,
        "general_offcontact": 0,
        "general_alarm": 0,
        "general_ph_rx_pump_volume": 0,
        "general_boot_delay": 15,
        "general_standby_time": 300,
        "general_language": 0
    },
    "settings_lighting": {
        "lighting_regulation": false,
        "lighting_active": false,
        "lighting_schedule": false,
        "lighting_start_time": "00:00:00",
        "lighting_stop_time": "00:00:00",
        "lighting_monday": false,
        "lighting_tuesday": false,
        "lighting_wednesday": false,
        "lighting_thursday": false,
        "lighting_friday": false,
        "lighting_saturday": false,
        "lighting_sunday": false,
        "lighting_on_deck_closed": false,
        "lighting_configuration": 0,
        "lighting_colour_stl": 0,
        "lighting_rgb_stl_time": 125,
        "lighting_next_colour": false
    },
    "settings_timerpumps": {
        "timerpumps_timer1_wait_time": 24,
        "timerpumps_timer1_dosing_time": 4,
        "timerpumps_timer2_wait_time": 24,
        "timerpumps_timer2_dosing_time": 4
    },
    "settings_aux1": {
        "aux1_regulation": false,
        "aux1_activate": false,
        "aux1_name": 14,
        "aux1_flow": true,
        "aux1_on_deck_closed": true,
        "aux1_schedule": true,
        "aux1_start_time": "00:00:00",
        "aux1_stop_time": "00:00:00",
        "aux1_monday": false,
        "aux1_tuesday": false,
        "aux1_wednesday": false,
        "aux1_thursday": false,
        "aux1_friday": false,
        "aux1_saturday": false,
        "aux1_sunday": false
    },
    "settings_aux2": {
        "aux2_regulation": false,
        "aux2_activate": false,
        "aux2_name": 14,
        "aux2_flow": false,
        "aux2_on_deck_closed": false,
        "aux2_schedule": false,
        "aux2_start_time": "00:00:00",
        "aux2_stop_time": "00:00:00",
        "aux2_monday": false,
        "aux2_tuesday": false,
        "aux2_wednesday": false,
        "aux2_thursday": false,
        "aux2_friday": false,
        "aux2_saturday": false,
        "aux2_sunday": false
    },
    "settings_aux3": {
        "aux3_regulation": false,
        "aux3_activate": false,
        "aux3_flow": false,
        "aux3_name": 14,
        "aux3_on_deck_closed": false,
        "aux3_schedule": false,
        "aux3_start_time": "00:00:00",
        "aux3_stop_time": "00:00:00",
        "aux3_monday": false,
        "aux3_tuesday": false,
        "aux3_wednesday": false,
        "aux3_thursday": false,
        "aux3_friday": false,
        "aux3_saturday": false,
        "aux3_sunday": false
    },
    "settings_aux4": {
        "aux4_regulation": false,
        "aux4_activate": false,
        "aux4_flow": false,
        "aux4_schedule": false,
        "aux4_start_time": "00:00:00",
        "aux4_stop_time": "00:00:00",
        "aux4_monday": false,
        "aux4_tuesday": false,
        "aux4_wednesday": false,
        "aux4_thursday": false,
        "aux4_friday": false,
        "aux4_saturday": false,
        "aux4_sunday": false,
        "aux4_name": 14,
        "aux4_on_deck_closed": false
    },
    "settings_temperaturesolar": {
        "temperaturesolar_regulation": false,
        "temperaturesolar_temperature_offset": 0.0,
        "temperaturesolar_pump_speed": 2,
        "temperaturesolar_sp_too_high": 0.0,
        "temperaturesolar_sp_high": 0.0
    },
    "settings_temperatureheating": {
        "temperatureheating_regulation": false,
        "temperatureheating_interval": 5,
        "temperatureheating_priority": false,
        "temperatureheating_cooling_period": 120,
        "temperatureheating_pump_speed": 1,
        "temperature_frost_protection": false
    },
    "settings_ecovalve": {
        "filterecovalve_always_active": false,
        "filterecovalve_buffertank": false
    },
    "settings_temperature": {
        "temperature_water_target": 12.0,
        "temperature_frost_protection": false
    },
    "settings_backwash": {
        "filterbackwash_regulation": false,
        "filterbackwash_interval_period": 2,
        "filterbackwash_pump_speed": 2,
        "filterbackwash_backwash_duration": 300,
        "filterbackwash_rinse_duration": 300,
        "filterbackwash_config_rinse": false,
        "filterbackwash_start": false
    },
    "settings_filterschedule1": {
        "filterschedule1_enabled": false,
        "filterschedule1_start_time": "00:00:00",
        "filterschedule1_stop_time": "00:00:00",
        "filterschedule1_monday": false,
        "filterschedule1_tuesday": false,
        "filterschedule1_wednesday": false,
        "filterschedule1_thursday": false,
        "filterschedule1_friday": false,
        "filterschedule1_saturday": false,
        "filterschedule1_sunday": false,
        "filterschedule1_pump_speed": 0
    },
    "settings_filterschedule2": {
        "filterschedule2_enabled": false,
        "filterschedule2_start_time": "00:00:00",
        "filterschedule2_stop_time": "00:00:00",
        "filterschedule2_monday": false,
        "filterschedule2_tuesday": false,
        "filterschedule2_wednesday": false,
        "filterschedule2_thursday": false,
        "filterschedule2_friday": false,
        "filterschedule2_saturday": false,
        "filterschedule2_sunday": false,
        "filterschedule2_pump_speed": 0
    },
    "settings_filterschedule3": {
        "filterschedule3_enabled": false,
        "filterschedule3_start_time": "08:00:00",
        "filterschedule3_stop_time": "20:00:00",
        "filterschedule3_monday": true,
        "filterschedule3_tuesday": true,
        "filterschedule3_wednesday": true,
        "filterschedule3_thursday": true,
        "filterschedule3_friday": true,
        "filterschedule3_saturday": true,
        "filterschedule3_sunday": true,
        "filterschedule3_pump_speed": 2
    },
    "settings_rx": {
        "rx_value_target": 700.0,
        "rx_value_target_ppm": 0.77,
        "rx_dosing_time": 900,
        "rx_pausing_time": 3,
        "rx_overdose_alert": 0,
        "rx_min_water_temp": 12.0
    },
    "settings_ph": {
        "ph_value_target": 7.4,
        "ph_dosing_time": 30,
        "ph_pausing_time": 5,
        "ph_dosing_choice": 1,
        "ph_overdose_alert": 0,
        "ph_hysteresis": 0.2
    },
    "settings_filter": {
        "filter_pump_force_on": false
    },
    "settings_watersuppletion": {
        "watersuppletion_flow_valve": false
    },
    "settings_deck": {
        "deck_open": false,
        "deck_close": false,
        "deck_stop": false
    }
}
```
