import uasyncio as asyncio
import time

from library import badge

if __name__ == '__main__':
    while True:
        asyncio.run(badge.start_main())
        print("Restarting main thread...")
        time.sleep(1)
