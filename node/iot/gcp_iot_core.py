import os
import logging
from google.cloud import iot_v1

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GCP IoT Core class
class GCP IoTCore:
    def __init__(self, project_id: str, location: str, registry_id: str):
        self.project_id = project_id
        self.location = location
        self.registry_id = registry_id
        self.client = iot_v1.DeviceManagerClient()

    def create_device(self, device_id: str):
        try:
            self.client.create_device(self.project_id, self.location, self.registry_id, device_id)
            logger.info(f'Created device {device_id} in GCP IoT Core')
        except Exception as e:
            logger.error(f'Error creating device {device_id} in GCP IoT Core: {e}')

    def send_command(self, device_id: str, command: str):
        try:
            self.client.send_command_to_device(self.project_id, self.location, self.registry_id, device_id, command)
            logger.info(f'Sent command {command} to device {device_id}')
        except Exception as e:
            logger.error(f'Error sending command {command} to device {device_id}: {e}')

if __name__ == '__main__':
    project_id = os.environ['GCP_PROJECT_ID']
    location = os.environ['GCP_LOCATION']
    registry_id = os.environ['GCP_REGISTRY_ID']
    gcp_iot_core = GCP IoTCore(project_id, location, registry_id)
    gcp_iot_core.create_device('my_device')
    gcp_iot_core.send_command('my_device', 'predict')
