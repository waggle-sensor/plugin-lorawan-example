import logging
import time
import argparse
from waggle.plugin import Plugin


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--app-name",
        default="Smart_Agriculture",
        help="The chirpstack application name",
    )
    parser.add_argument(
        "--device-name",
        default="E5 Mini Livestock Counter",
        help="The chirpstack LoRa end device name",
    )
    parser.add_argument(
        "--location-tag",
        default="West Barn",
        help="The value of chirpstack tag that details the location of the device",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    logging.info("Subcribing to lorawan.data...")

    with Plugin() as plugin:

        plugin.subscribe("lorawan.data")

        while True:
            msg = plugin.get()

            if msg.meta.get("applicationName") == args.app_name and msg.meta.get("deviceName") == args.device_name and msg.meta.get("Location_tag") == args.location_tag:

                metadata = {
                    "deviceName": msg.meta.get("deviceName"),
                    "Location_tag": msg.meta.get("Location_tag"),
                    "applicationName": msg.meta.get("applicationName"),
                    "tenantName": msg.meta.get("tenantName")
                }

                plugin.publish("lorawan.test.Livestock_Count", int(msg.value), timestamp=time.time_ns(), meta=metadata)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass