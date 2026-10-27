# NAS HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| NAS-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| NAS-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| NAS-003 | It shall mount through the HAT Case Standard. | must | Confirmed |
| NAS-004 | It may include on-board AI features. | should | Draft |
| NAS-005 | The HAT shall provide SSD storage. | must | Confirmed |
| NAS-006 | The HAT shall provide Ethernet ports. | must | Confirmed |
| NAS-007 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| NAS-008 | The HAT shall present its SSD as USB mass storage (UAS) and its Ethernet ports as USB network functions, behind a USB 3 hub. | must | Draft |
