from rich.console import Console

from open_gopro.communicator_interface import GoProBle
from open_gopro.models.response import BleRespBuilder
from open_gopro.constants import GoProUUIDs
from open_gopro.logger import setup_logging

console = Console()

data = bytes(
    [
        0x20,
        0x60,  # Packet length
        0x3C,  # ID
        0x00,  # Status
        # Model Number Length (4)
        0x04,
        # Model Number (55)
        0x00,
        0x00,
        0x00,
        0x37,
        # Model Name Length (11)
        0x0B,
        # Mode Name (Hero 9 Black)
        0x48,
        0x45,
        0x52,
        0x4F,
        0x39,
        0x20,
        0x42,
        0x6C,
        0x61,
        0x63,
        0x80,
        # Board Type
        0x6B,
        # Board Type length (4)
        0x04,
        # Board Type (0x05)
        0x30,
        0x78,
        0x30,
        0x35,
        # FW Version length (16)
        0x0F,
        # FW Version (HD9.01.01.60.00)
        0x48,
        0x44,
        0x39,
        0x2E,
        0x30,
        0x31,
        0x2E,
        0x30,
        0x31,
        0x2E,
        0x36,
        0x30,
        0x81,
        0x2E,
        0x30,
        0x30,
        # Serial Number length
        0x0E,
        # Serial Number (C3441324804792)
        0x43,
        0x33,
        0x34,
        0x34,
        0x31,
        0x33,
        0x32,
        0x34,
        0x38,
        0x30,
        0x34,
        0x37,
        0x39,
        0x32,
        # SSID Length (11)
        0x0B,
        # SSID ('HERO9 Black')
        0x82,
        0x48,
        0x45,
        0x52,
        0x4F,
        0x39,
        0x20,
        0x42,
        0x6C,
        0x61,
        0x63,
        0x6B,
        # Mac Len (13
        0x0C,
        # SSID ('d63260b55195')
        0x64,
        0x36,
        0x33,
        0x32,
        0x36,
        0x30,
        0x62,
        0x83,
        0x35,
        0x35,
        0x31,
        0x39,
        0x35,
        # Unknown
        0x01,
        0x00,
        0x01,
        0x01,
        0x01,
        0x00,
        0x07,
        0x5B,
        0x22,
        0x62,
        0x6C,
        0x65,
        0x22,
        0x5D,
        0x84,
        0x01,
        0x01,
    ]
)


def main() -> None:
    setup_logging(__name__)
    builder = BleRespBuilder()
    for packet in (data[i : i + GoProBle.MAX_BLE_PKT_LEN] for i in range(0, len(data), GoProBle.MAX_BLE_PKT_LEN)):
        console.print(f"Accumulating packet: {packet.hex(':')}")
        builder.accumulate(packet)
    builder.set_uuid(GoProUUIDs.CQ_COMMAND_RESP)
    response = builder.build()
    console.print(f"\nExpected packet length: {builder._expected_len} == {hex(builder._expected_len)}")
    console.print(
        f"Response type: {response.identifier} == {int(response.identifier)} == {hex(int(response.identifier))}"
    )
    console.print(f"Status: {response.status} == {response.status.value}\n")
    console.print(str(response))


def entrypoint() -> None:
    main()


if __name__ == "__main__":
    entrypoint()
