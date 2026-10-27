# Shared Transfer UI

Edit source files here. Pico and BL616 generators synchronize this source into their bundled snapshots before producing firmware assets, website receiver and offline ZIP. Both use one USB/file protocol; chunk size is device-negotiated. Do not edit generated transfer/index.html independently.

Validation: identical receiver hashes including ZIP contents; Pico 16384-byte and BL616 8192-byte protocol mocks; 4096-byte reverse transfer, empty file, CRC error and offline browser checks passed. Hardware throughput/stability is separate.
