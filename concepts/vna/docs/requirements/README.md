# VNA HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| VNA-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| VNA-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| VNA-003 | It shall mount through the OpenDAP HAT Standard. | must | Confirmed |
| VNA-004 | It may include on-board AI features. | should | Draft |
| VNA-005 | The HAT shall be a vector network analyzer based on NanoVNA. | must | Confirmed |
| VNA-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| VNA-007 | The HAT shall use CDC-ACM, as its base design does. | must | Draft |
