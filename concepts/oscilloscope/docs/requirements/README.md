# Oscilloscope HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| OSC-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| OSC-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| OSC-003 | It shall mount through the OpenDAP HAT Standard. | must | Confirmed |
| OSC-004 | It may include on-board AI features. | should | Draft |
| OSC-005 | The HAT shall be an oscilloscope based on the DS212. | must | Confirmed |
| OSC-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| OSC-007 | The HAT shall stream samples over High-Speed USB from its own MCU or FPGA. | must | Draft |
