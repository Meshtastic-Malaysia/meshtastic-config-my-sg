#!/usr/bin/env python3
"""Generate a minimal Meshtastic channel URL from user input."""

import base64
from meshtastic.protobuf import apponly_pb2, config_pb2

RegionCode = config_pb2.Config.LoRaConfig.RegionCode
ModemPreset = config_pb2.Config.LoRaConfig.ModemPreset

REGIONS = {name: value for name, value in RegionCode.items() if name != "UNSET"}
MODEM_PRESETS = {name: value for name, value in ModemPreset.items()}

DEFAULT_PSK = b"\x01"  # Use the default Meshtastic key


def prompt_choice(prompt, choices: dict, default=None):
    """Prompt user to pick from a numbered list of choices."""
    keys = list(choices.keys())
    print(f"\n{prompt}")
    for i, key in enumerate(keys, 1):
        marker = " (default)" if key == default else ""
        print(f"  {i:2}. {key}{marker}")
    while True:
        raw = input("Enter number or name [default: {}]: ".format(default or "")).strip()
        if not raw and default:
            return choices[default]
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(keys):
                return choices[keys[idx]]
        if raw.upper() in choices:
            return choices[raw.upper()]
        print("  Invalid choice, try again.")


def prompt_int(prompt, default=None, min_val=None, max_val=None):
    """Prompt user for an integer."""
    hint = f" [{min_val}-{max_val}]" if min_val is not None and max_val is not None else ""
    default_hint = f" (default: {default})" if default is not None else ""
    while True:
        raw = input(f"{prompt}{hint}{default_hint}: ").strip()
        if not raw and default is not None:
            return default
        if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
            val = int(raw)
            if (min_val is None or val >= min_val) and (max_val is None or val <= max_val):
                return val
        print("  Invalid value, try again.")


def prompt_bool(prompt, default=True):
    """Prompt user for yes/no."""
    hint = "Y/n" if default else "y/N"
    raw = input(f"{prompt} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "1", "true")


def build_channel_url(
    region: int,
    modem_preset: int,
    channel_name: str = "",
    psk: bytes = DEFAULT_PSK,
    position_precision: int = 32,
    uplink_enabled: bool = False,
    downlink_enabled: bool = False,
    tx_enabled: bool = True,
    tx_power: int = 0,
    hop_limit: int = 3,
    channel_num: int = 0,
    sx126x_rx_boosted_gain: bool = True,
    config_ok_to_mqtt: bool = True,
) -> str:
    cs = apponly_pb2.ChannelSet()

    ch = cs.settings.add()
    ch.psk = psk
    if channel_name:
        ch.name = channel_name
    if uplink_enabled:
        ch.uplink_enabled = True
    if downlink_enabled:
        ch.downlink_enabled = True
    if position_precision != 0:
        ch.module_settings.position_precision = position_precision

    lora = cs.lora_config
    lora.use_preset = True
    lora.region = region
    lora.modem_preset = modem_preset
    if hop_limit != 3:
        lora.hop_limit = hop_limit
    lora.tx_enabled = tx_enabled
    if tx_power != 0:
        lora.tx_power = tx_power
    if channel_num != 0:
        lora.channel_num = channel_num
    if sx126x_rx_boosted_gain:
        lora.sx126x_rx_boosted_gain = True
    if config_ok_to_mqtt:
        lora.config_ok_to_mqtt = True

    encoded = base64.urlsafe_b64encode(cs.SerializeToString()).rstrip(b"=").decode()
    return f"https://meshtastic.org/e/#{encoded}"


def main():
    print("=== Meshtastic Channel URL Generator ===")

    region = prompt_choice("Region", REGIONS, default="MY_919")
    modem_preset = prompt_choice("Modem preset", MODEM_PRESETS, default="LONG_FAST")

    channel_name = input("\nChannel name (leave blank for primary/default): ").strip()

    position_precision = prompt_int(
        "Position precision (bits, 0=disabled, 10=~23km, 32=exact)",
        default=32, min_val=0, max_val=32
    )

    print("\n--- MQTT ---")
    uplink = prompt_bool("Uplink enabled (send to MQTT)", default=False)
    downlink = prompt_bool("Downlink enabled (receive from MQTT)", default=False)

    print("\n--- LoRa ---")
    hop_limit = prompt_int("Hop limit", default=3, min_val=1, max_val=7)
    channel_num = prompt_int("Channel number override (0 = default for preset)", default=0, min_val=0, max_val=7)
    tx_power = prompt_int("TX power in dBm (0 = device max)", default=0, min_val=0, max_val=30)
    rx_boost = prompt_bool("SX126x RX boosted gain", default=True)
    ok_to_mqtt = prompt_bool("Config OK to MQTT (allow nodes to forward packets to MQTT)", default=True)

    url = build_channel_url(
        region=region,
        modem_preset=modem_preset,
        channel_name=channel_name,
        position_precision=position_precision,
        uplink_enabled=uplink,
        downlink_enabled=downlink,
        hop_limit=hop_limit,
        channel_num=channel_num,
        tx_power=tx_power,
        sx126x_rx_boosted_gain=rx_boost,
        config_ok_to_mqtt=ok_to_mqtt,
    )

    print(f"\nChannel URL:\n  {url}\n")


if __name__ == "__main__":
    main()
