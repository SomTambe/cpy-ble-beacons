# cpy-ble-beacons
CircuitPython BLE library for making it easy to work with BLE beacons on the nRF52840 boards.

Low level access to BLE payloads was quite difficult with the existing `adafruit_ble` library simply because it has enigmatic documentation, and rather than banging my head on the wall for understanding the library, I thought it would be better and quick to write methods using the `_bleio` low level Bluetooth API.

This is purely for beaconing purposes, and I have not written anything related to GATT protocols yet. I may add some features related to this in the near future.

Advertising Data elements available right now:
- Flags
- Shortened local names
- Complete local names

Plan to add:
- Manufacturer specific payload
- 16-bit UUIDs
- 128-bit UUIDs

I currently use this for my experiments, so it's not actually stable. Maybe sometime later I will put up some really nice docs for the library which will make it more usable.
