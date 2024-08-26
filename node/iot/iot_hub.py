import os
import logging
from azure.iot.hub import IoTHubRegistryManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IoT Hub class
class IoTHub:
    def __init__(self, iot_hub_name: str, connection_string: str):
        self.iot_hub_name = iot_hub_name
        self.connection_string = connection_string
        self.registry_manager = IoTHubRegistryManager.from_connection_string(connection_string)

    def create_device(self, device_id: str):
        try:
            self.registry_manager.create_device(device_id)
            logger.info(f'Created device {device_id} in IoT Hub')
        except Exception as e:
            logger.error(f'Error creating device {device_id} in IoT Hub: {e}')

    def send_command(self, device_id: str, command: str):
        try:
            self.registry_manager.send_command(device_id, command)
            logger.info(f'Sent command {command} to device {device_id}')
        except Exception as e:
            logger.error(f'Error sending command {command} to device {device_id}: {e}')

if __name__ == '__main__':
    iot_hub_name = os.environ['IOT_HUB_NAME']
    connection_string = os.environ['IOT_HUB_CONNECTION_STRING']
    iot_hub = IoTHub(iot_hub_name, connection_string)
    iot_hub.create_device('my_device')
    iot_hub.send_command('my_device', 'predict')
