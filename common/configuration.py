# ! This file contains the device configurations for the experiments

# * Stuff like the IPs of the devices, ZMQ Ports and Which device is collecting power for which other device etc is here

import getpass
from .experiments import valid_datasets as VALID_DATASETS
from .experiments import valid_fusions as VALID_FUSION_ALGOS
from .experiments import fusion_translator
from .experiments import Experiment


FUSION_ALGOS_TRANSLATOR = fusion_translator

IP_CLIENTS = {
    "rpi1": "10.8.1.38",
    "rpi2": "10.8.1.43",
    "rpi3": "10.8.1.192",
    "rpi4": "10.8.1.41",
}

IP_AGGREGATOR = "10.8.1.45"

AGGREGATOR_FLOWER_SERVER_PORT = 7011

AGGREGATOR_USERNAME = getpass.getuser()

AGGREGATOR_ZMQ_BROADCAST_PORT = 6010

ZMQ_STOP_POWER_COLLECTION = 300

IP_POWER_COLLECTORS = {
    "pi3": "10.8.1.200",
}

UM25C_ADDR_FOR_POWER_COLLECTORS = {
    "pi3": "98:DA:F0:00:4A:13",
}

POWER_COLLECTOR_CONNECTED_DEVICE = {
    "pi3": "rpi3",
}
