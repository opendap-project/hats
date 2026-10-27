# Radio HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| RAD-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| RAD-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| RAD-003 | It shall mount through the HAT Case Standard. | must | Confirmed |
| RAD-004 | It may include on-board AI features. | should | Draft |
| RAD-005 | The HAT shall be a software-defined radio based on HackRF Pro. | must | Confirmed |
| RAD-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| RAD-007 | The HAT shall stream over High-Speed USB 2.0, as its HackRF Pro base does; the SuperSpeed pads of the interface are left unconnected. | must | Draft |
| RAD-008 | The HAT targets radio and RF security research: software-defined radio, sub-GHz capture and replay, and RFID/NFC research (reading, emulation and cloning at LF 125 kHz and HF 13.56 MHz). | must | Draft |
| RAD-009 | The HAT's SDR shall cover 100 kHz–6 GHz operating frequency at up to 20 Msps, as the HackRF Pro base provides, on a 50 Ω SMA port. | must | Draft |
| RAD-010 | Functions beyond the SDR (sub-GHz transceiver, RFID/NFC tool, LoRa) shall reach the device as additional USB functions behind an on-HAT USB hub, each with a mainline Linux or open-source host driver (SoapySDR/`hackrf`, CDC-ACM, HID). | must | Draft |
| RAD-011 | The HAT shall be receive-only by default. Any transmission shall require an explicit, logged user action and an on-screen notice of the user's licence and spectrum-law responsibility; Blackbird OS shall show the active region's applicable limits. | must | Draft |
| RAD-012 | The HAT shall carry its own radio and RF-exposure compliance as a separate product with its own declaration of conformity; it shall not be placed on the market as a single combined product with the device. | must | Draft |
| RAD-013 | The HAT should define a receive-only hardware variant (transmit path depopulated) as a population option, for markets where a transmit-capable variant has no certification path. | should | Draft |
| RAD-014 | The HAT shall operate within the device's 5 V HAT power budget (≤ 1.5 A from the T1) without its own battery; lower rails are regulated on the HAT. | must | Draft |
| RAD-015 | The HAT's RFID/NFC research function should be distinct from, and not replace, the device's own NFC reader; the device's NFC remains its tap-to-pair and hand-off reader. | should | Draft |
| RAD-016 | LoRa/Meshtastic messaging is a secondary function of this HAT and, where fitted, should use a pre-certified radio module. | should | Draft |

## Context

- RAD-007 to RAD-016: recorded as **Draft**. RAD-007 amended the same day: the HackRF Pro (Great Scott Gadgets) is a High-Speed USB 2.0 design, so the SuperSpeed pads of [interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) stay unconnected.
- RAD-009: the HackRF Pro operates from 100 kHz to 6 GHz at 20 Msps with 8-bit I/Q samples (Great Scott Gadgets HackRF Pro documentation). 20 Msps × 2 bytes is 320 Mb/s, inside High-Speed USB 2.0. Its hardware is licensed CERN-OHL-P-2.0 and its software GPL (OSHWA certification US002820).
- RAD-010: a USB 2.0 hub keeps the SDR on its own `hackrf` driver and lets each device recover its firmware over USB on its own (HCS-031).
- RAD-011, RAD-012: a wideband transmitter from 1 MHz to 6 GHz has no consumer certification route under US Part 15, the EU Radio Equipment Directive or the Japan Radio Act. The EU Radio Equipment Directive also covers receive-only radio equipment. Showing a region's spectrum limits is a legal limit made visible, not a capability lock (BRD-049).
- RAD-013: whether the transmit path of a HackRF-derived half-duplex chain can be depopulated is **UNVERIFIED**; it is checked at schematic capture.
- RAD-014: interface v2 gives a HAT 5 V at up to 1.5 A from the T1. The HAT's whole-board power draw is **UNVERIFIED** until it is measured on the first prototype.
- RAD-015: the device's NFC reader is a fixed-function reader for tap-to-pair and hand-off; the HAT's tool adds low-level access for research (sniffing, emulation, cloning) at LF and HF.
