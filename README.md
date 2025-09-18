# Meshtastic YAML Configurations for Malaysia (MY_919) and Singapore (SG_923)

These are YAML files for quick/mass deployment of LongFast-only (public, unencrypted) channels to Meshtastic devices.

## Prerequisites

* [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/installation/)
* YAML files from this repository

## Usage

### Standard

Use these if you are frequently within mesh coverage.

* **MY_919**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure MY_919.yaml`
* **SG_923**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure SG_923.yaml`

### MQTT Gateway/Client Proxy

Use these if you are frequently outside of mesh coverage, and your node is connected to Wi-Fi or a phone client app with cellular data.

* **MY_919**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure MY_919_lucifernet_MQTT.yaml`
* **SG_923**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure SG_923_lucifernet_MQTT.yaml`

### RF-only

Use these if you do not want your transmissions uplinked by MQTT gateways. Note that your communications will be isolated to nodes within RF range only, limited by your configured hop limit (default: 3).

* **MY_919**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure MY_919_RF_only.yaml`
* **SG_923**: `meshtastic [-t tcp_node_ip/hostname] [-s com_port/tty_device] --configure SG_923_RF_only.yaml`

## Channels

Only 1 channel (channelNum 0/id 0) is defined, with the following settings:

| Key | Value | Notes |
| - | - | - |
| uplinkEnabled | true | MQTT uplink enabled |
| downlinkEnabled | true | MQTT downlink enabled |
| positionPrecision | 32 | Full precision (reduce as desired) |
| _Other settings_ | _Default LongFast_ | |

## LoRa Settings

| Key | Malaysia | Singapore | Notes |
| - | - | - | - |
| region | MY_919 | SG_923 | |
| channelNum | 16 (922.875 MHz) | 4 (917.875 MHz) | Lock frequency to [default LongFast frequency](https://meshtastic.org/docs/configuration/tips/#default-primary-frequency-slots-by-region) |
| configOkToMqtt | true | true | MQTT uplink enabled on LongFast |
| _Other settings_ | _Default LongFast_ | _Default LongFast_ | |

## MQTT Module Settings

| Key | Malaysia | Singapore | Notes |
| - | - | - | - |
| address | mqtt.lucifernet.com | mqtt.lucifernet.com | Default Meshtastic MQTT server discards high precision (>16 bit) position packets and makes MQTT downlinked packets zero-hop; this server does not (maintaned by 9W2LWK) |
| enabled | true | true | |
| encryptionEnabled | true | true | |
| positionPrecision | 32 | 32 | |
| mapReportingEnabled | true | true | |
| password | large4cats | large4cats | |
| root | msh/MY_919 | msh/SG_923 | |
| username | meshdev | meshdev | |
