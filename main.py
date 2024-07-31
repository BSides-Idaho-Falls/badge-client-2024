import uasyncio as asyncio
from library import badge, atomics


if __name__ == '__main__':
    if atomics.WDT_ENABLED:
        from machine import WDT
        atomics.wdt = WDT(timeout=8388)
    asyncio.run(badge.start_main())
