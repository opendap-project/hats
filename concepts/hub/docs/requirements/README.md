# HUB HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| HUB-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Draft |
| HUB-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Draft |
| HUB-003 | It shall mount through the OpenDAP HAT Standard. | must | Draft |
| HUB-004 | It may include on-board AI features. | should | Draft |
| HUB-005 | The HAT shall be a media ingest hub for content professionals: it reads removable camera and recorder media and copies it to verified destinations without a computer. | must | Draft |
| HUB-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| HUB-007 | The HAT shall use the device's SuperSpeed (USB 3 Gen 1) HAT link, with a USB 3 hub carrying its functions. | must | Draft |
| HUB-008 | The HAT shall provide a full-size SD and a microSD slot, each UHS-II (SD 4.0) and backward compatible with UHS-I, presented to the device as USB mass storage through a mainline Linux driver. | must | Draft |
| HUB-009 | The HAT shall provide a downstream USB-C host port (USB 3 Gen 1) for external drives, camera connections and other readers, powered within its USB 3 allocation. | must | Draft |
| HUB-010 | The HAT should carry an internal M.2 2230 NVMe SSD as a copy destination, presented as USB mass storage (UAS). | should | Draft |
| HUB-011 | The HAT should provide a Gigabit Ethernet port through a mainline Linux driver. | should | Draft |
| HUB-012 | The HAT should provide a USB-C power input (USB PD sink) that powers the HAT and its downstream port and charges the device at 5 V, per interface v2 §5.2. | should | Draft |
| HUB-013 | Its software shall verify every copy by checksum, read back from each destination, and record the copy in an ASC MHL (version 2) hash list. | must | Draft |
| HUB-014 | The HAT shall run a single-destination copy from a card within the device's 5 V HAT power budget (≤ 1.5 A from the T1) without its own battery; modes beyond that budget run only on its own power input. Its subsystems are power-gated per mode and its lower rails are regulated on the HAT. | must | Draft |
| HUB-015 | Every programmable chip on the HAT shall be recoverable over USB with no working firmware (a ROM USB loader or a protected DFU bootloader), per HCS-031. | must | Draft |
| HUB-016 | A CFexpress Type A slot should be a population option, fitted only where the measured card power and the enclosure's thermal limit allow it. | should | Draft |
| HUB-017 | A 3G-SDI input, with video presented as USB Video Class and its embedded audio as USB Audio Class, should be a population option for monitoring, fitted only where the enclosure's thermal limit allows it. | should | Draft |
