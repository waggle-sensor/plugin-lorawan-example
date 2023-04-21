# LoRaWAN Example Usage Instructions

## About The Plugin 

This plugin provides a practical demonstration of how to integrate the lorawan-listener plugin into your application. Specifically, it shows how to consume data from LoRa end devices that are used for livestock counting in a barn. The lorawan-listener plugin is used to retrieve this data. It's important to note that this plugin example will only retrieve data from lorawan-listener if it matches the specified application name, device name, and location tag. Any data that doesn't meet these requirements will be ignored. Once the data has been retrieved, this plugin publishes it under the measurement called 'lorawan.example.livestock.counter'. By following this example, you'll gain a better understanding of how to consume data from lorawan-listener and integrate it into your own application.

## Using the code

Please note that for this plugin to function properly, it is required that the lorawan-listener plugin is running on the same node as well. This means that whenever you schedule this plugin on a node, you must also schedule the lorawan-listener plugin. Additionally, your chirpstack environment must include a tag named 'Location' for your devices. This is necessary in order for the plugin to retrieve the data published by lorawan-listener, as the location tag is used to identify the specific data related to livestock counting in a barn. By ensuring that both the lorawan-listener and this plugin are properly scheduled, and that your chirpstack environment includes the required location tag, you can expect this plugin to function as intended.

This plugin currently only works in the US Region due to regulations in radio channels and [wes-chirpstack](https://github.com/waggle-sensor/waggle-edge-stack/tree/main/kubernetes/wes-chirpstack) being set up for US Region.

## Running lorawan-listener

To run lorawan-example on the node it must be scheduled with lorawan-listener using the [Edge Scheduler (ES)](https://docs.waggle-edge.ai/docs/about/architecture#edge-scheduler-es). There is a [walkthrough example](https://docs.waggle-edge.ai/docs/tutorials/schedule-jobs) on the Sage website under docs that can be followed. The lorawan-listener plugin can also be scheduled using the [Sage Portal's UI to create jobs](https://portal.sagecontinuum.org/create-job). An example of the job's yaml file is found below.

```
name: Lorawan_ExampleJob
plugins:
- name: lorawan-example
  pluginSpec:
    image: registry.sagecontinuum.org/flozano/lorawan-example:0.0.1
    args:
    - --app-name
    - "Smart_Agriculture"
    - --device-name
    - "E5 Mini Livestock Counter"
    - --location-tag
    - "West Barn"
    selector:
      zone: core
- name: lorawan-listener
  pluginSpec:
    image: registry.sagecontinuum.org/flozano/lorawan-listener:0.0.1
    selector:
      zone: core
nodeTags: []
nodes:
  W030: true
scienceRules:
- 'schedule("lorawan-example"): cronjob("lorawan-example", "* * * * *")'
- 'schedule("lorawan-listener"): cronjob("lorawan-listener", "* * * * *")'
successCriteria:
- WallClock('1day')
```

Once the job is scheduled, the node will publish values under the measurement 'lorawan.example.livestock.counter'.

# Arguments

**--app-name**: The chirpstack application name

**--device-name**: The chirpstack LoRa end device name

**--location-tag**: The value of chirpstack tag that details the location of the device
