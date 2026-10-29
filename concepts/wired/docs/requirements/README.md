# Wired HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| WIR-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Draft |
| WIR-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Draft |
| WIR-003 | It shall mount through the OpenDAP HAT Standard. | must | Draft |
| WIR-004 | It may include on-board AI features. | should | Draft |
| WIR-005 | The HAT shall be a bench for physical-interface R&D: it exercises wired ports beyond USB as bus master/host, target/client-device and passive monitor, across the levels from fundamental buses to Gigabit Ethernet. | must | Draft |
| WIR-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| WIR-007 | The HAT shall use the device's SuperSpeed (USB 3 Gen 1) HAT link, with a USB hub when it carries several functions; functions that need only USB 2.0 use the USB 2.0 pair. | must | Draft |
| WIR-008 | The HAT shall exercise the fundamental interfaces as master and as target, each with a mainline Linux or open-source host driver: I2C/SMBus, SPI/QSPI, UART, 1-Wire, JTAG/SWD, GPIO/PWM, CAN FD and RS-232/485. | must | Draft |
| WIR-009 | The HAT's external I/O shall be level-shifted across 1.2–5 V and protected (ESD clamp, over-voltage and current limit); a programmable supply with a current-limit fuse shall be able to power a target. | must | Draft |
| WIR-010 | The HAT shall provide reconfigurable-logic interfacing and timing-accurate logic analysis, and passive High-Speed USB 2.0 analysis, through open gateware and open host software. | must | Draft |
| WIR-011 | The HAT should provide an Ethernet tap and active in-line MITM up to Gigabit, with galvanic isolation and a relay bypass, through a mainline Linux host driver. | should | Draft |
| WIR-012 | Every programmable chip on the HAT shall be recoverable over USB with no working firmware (a ROM USB loader or a protected DFU bootloader), per HCS-031. | must | Draft |
| WIR-013 | The HAT shall operate within the device's 5 V HAT power budget (≤ 1.5 A from the T1) without its own battery; its subsystems are power-gated per mode and its lower rails are regulated on the HAT. | must | Draft |
| WIR-014 | SFP optical / SerDes links and SuperSpeed USB 3 analysis shall be a population option, fitted only where the FPGA SerDes, the HAT link bandwidth and the enclosure allow. | should | Draft |

## Context

- Name confirmed by the maintainers on 2026-10-26: OpenDAP Wired HAT, prefix WIR.
- WIR-001 to WIR-004 follow the common HAT pattern (complete project; custom software on popular Open Source for its domain; OpenDAP HAT Standard; optional on-board AI), as the other HATs do.
- WIR-007: the board routes USB3 HOST1 (SuperSpeed pairs and the USB 2.0 D± pair) to the HAT port ([board pinout v1](https://github.com/opendap-project/t1/blob/main/board/docs/specs/pinout-v1.md), [RFC 0014](https://github.com/opendap-project/rfcs/blob/main/text/0014-hat-interface-v2-usb-only.md)); the T1's HAT port is USB 3 Gen 1 (5 Gb/s, ≈ 3.2 Gb/s per direction, [interface v2](https://github.com/opendap-project/hats/blob/main/standard/docs/specs/interface-v2.md)). The HAT uses SuperSpeed for its analysis and Gigabit Ethernet roles.
- WIR-009: the level-shift and protection model follows open interface explorers (Glasgow Interface Explorer: per-pin level shifter, ESD diodes, per-bank sense ADC; Bus Pirate 6: 1.2–5 V buffered I/O, a 1–5 V programmable supply and a 0–500 mA current-limit fuse).
- WIR-011: an unpowered passive tap cannot monitor 1000BASE-T (Throwing Star LAN Tap degrades it to 100BASE-TX), so Gigabit monitoring is the active MITM path, through a Gigabit Ethernet bridge with a mainline Linux driver (for example lan78xx). The relay bypass keeps the monitored link up on power loss.
- WIR-014: the ECP5 SerDes supports 1000BASE-X on the open Yosys/nextpnr/Trellis toolchain but is undocumented (**UNVERIFIED** for this use), and an SFP cage does not fit a thin HAT; both are a population option until a SerDes bring-up.
