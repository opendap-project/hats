# Outdoor HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| OUT-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Draft |
| OUT-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Draft |
| OUT-003 | It shall mount through the OpenDAP HAT Standard. | must | Draft |
| OUT-004 | It may include on-board AI features. | should | Draft |
| OUT-005 | The HAT shall extend the device for use beyond infrastructure: two-way satellite messaging with an emergency SOS, multi-band GNSS (at least L1 and L5), LoRa mesh messaging, and its own battery that powers the HAT and charges the device. | must | Draft |
| OUT-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md) (HCS-027 to HCS-031). | must | Draft |
| OUT-007 | The HAT shall be a dual-role USB PD HAT that sources the device within its input capability, reports its battery over PD, powers its own radios from its own battery, and keeps the device as USB host. | must | Draft |
| OUT-008 | The emergency SOS shall work from the HAT alone, with the device asleep, off or without software running: its own button, position, satellite link and battery. | must | Draft |
| OUT-009 | Mesh messaging, position logging and the satellite message queue shall keep running while the device sleeps. | must | Draft |
| OUT-010 | The HAT should offer cellular connectivity (5G with LTE fallback, SMS, voice and eSIM) as a population option on a socket that every unit carries. | should | Draft |
| OUT-011 | The HAT should carry a barometric altimeter, a magnetometer and a flashlight. | should | Draft |
| OUT-012 | The HAT shall be charged through its own USB-C receptacle, including from solar panels, and shall be able to power another USB-C device. | must | Draft |
| OUT-013 | The HAT case should reach IP67. | should | Draft |
| OUT-014 | The HAT battery shall be a standard commercial cell, replaceable by the user with common tools, with a published pack specification. | must | Draft |
| OUT-015 | Every transmitter shall follow the device's certification rules for each certified variant (t1 T1-077): no transmitter without a grant for its declared markets, RF exposure tested as a body-worn device together with the device, and every power or duty limit documented and visible. | must | Draft |

## Context

- OUT-001 to OUT-015: recorded as **Draft** when the repository was created ([RFC 0016](https://github.com/opendap-project/rfcs/blob/main/text/0016-outdoor-hat.md)).
- OUT-007: the HAT runs its radios from its own battery because a satellite transmit peak exceeds what the device offers a HAT: 5 V at up to 1.5 A ([interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md) §5.2). The T1 accepts only 5 V from a HAT.
- OUT-005: GNSS and satellite messaging are on a HAT because the T1 body has no room for another antenna next to its own ([board ADR 0018](https://github.com/opendap-project/board/blob/main/docs/adr/0018-antennas-and-certification-route.md)).
- OUT-009: LoRa mesh lives on this HAT, on its own microcontroller and battery, because it has to keep relaying while the device sleeps.
- OUT-010: cellular serves only where coverage exists; the module is fitted as a population option (board BRD-053) on a socket that every unit carries.
- OUT-013: the rating of the device with this HAT is the lower of the two; the HAT cannot raise the T1's own rating (T1-017).
