import asyncio
import logging
from bleak import BleakScanner
import numpy
import matplotlib.pyplot as plot

class BLELocationTracker:
    def __init__(self):
        self.fig, self.ax = plot.subplots(figsize=(10, 10))
        self.line, = self.ax.plot([], [], color='blue', label='Distance')
        self.ax.set_xlim(-10, 10) 
        self.ax.set_ylim(-10, 10) 
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_title('Device Distance')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid()
        self.circle, = self.ax.plot([], [], color='blue', label='Distance')
        self.ax.legend()
      
    async def tracking_loop(self, name: str):
        logging.info(f"tracking device {name=}")
        while True:
            device = await BleakScanner.find_device_by_name(name)
            if device is not None:
                logging.info(f"{device.rssi=}")
                distance = await self.rssi_to_distance(device.rssi)
                logging.info(f"{distance=}")
                await self.plot_distance(distance)
            else:
                logging.warning("Device not found")
            await asyncio.sleep(1)
    
    # https://iotandelectronics.wordpress.com/2016/10/07/how-to-calculate-distance-from-the-rssi-value-of-the-ble-beacon/
    async def rssi_to_distance(self, rssi:int):
        one_meter_rssi = -49 # NOTE: modify this
        n = 2
        distance = 10 ** ((one_meter_rssi - rssi)/(10*n))
        return distance
    
    async def plot_distance(self, distance):
        theta = numpy.linspace(0, 2 * numpy.pi, 100)
        x = distance * numpy.cos(theta) 
        y = distance * numpy.sin(theta)

        self.line.set_xdata(x)
        self.line.set_ydata(y)

        plot.draw()
        plot.pause(0.1) 

async def main():
    logging.basicConfig(level=logging.INFO)
    ble_location_tracker = BLELocationTracker()
    await ble_location_tracker.tracking_loop("Anjuna’s iPhone")

asyncio.run(main())