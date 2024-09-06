import uasyncio as asyncio
from library import badge, atomics


if __name__ == '__main__':
    if atomics.WDT_ENABLED:
        from machine import WDT
        atomics.wdt = WDT(timeout=8388)
    valid_years = ["2023", "2024"]
    if atomics.BADGE_YEAR not in valid_years:
        print("Invalid badge year. Only 2023 & 2024 badges are supported")
        print("Attempting to run anyway as if it were 2024")
        atomics.BADGE_YEAR = "2024"
    asyncio.run(badge.start_main())
