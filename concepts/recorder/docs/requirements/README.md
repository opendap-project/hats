# Recorder HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| REC-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| REC-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| REC-003 | It shall mount through the HAT Case Standard. | must | Confirmed |
| REC-004 | It may include on-board AI features. | should | Draft |
| REC-005 | The HAT shall be an audio recorder inspired by Tascam. | must | Confirmed |
| REC-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| REC-007 | The HAT shall present audio as USB Audio Class 2 (asynchronous), with its own clock and its own monitoring output. | must | Draft |
