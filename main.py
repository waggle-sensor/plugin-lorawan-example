import logging
import time
from waggle.plugin import Plugin


def main():

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
            if msg.meta.get("applicationName") == "Smart_Agriculture" and msg.meta.get("deviceName") == "E5 Mini Livestock Counter" and msg.meta.get("Location_tag") == "West Barn":

                metadata = {
                    "deviceName": msg.meta.get("deviceName"),
                    "applicationName": msg.meta.get("applicationName"),
                    "tenantName": msg.meta.get("tenantName")
                }

                plugin.publish("lorawan.test.Livestock_Count", int(msg.value), timestamp=time.time_ns(), meta=metadata)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass