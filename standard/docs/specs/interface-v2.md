# HAT interface v2

- **Revision:** v2.0 (Draft), 2026-10-25. It supersedes the [HAT interface v1](interface-v1.md) (revision v1.1), which stays as history. v2 is a new major revision: a v1 HAT does not fit a v2 device, and the reverse. Nothing was built against v1. Nothing here is built or measured.
- **Status:** Draft. The pad map freezes only after the signal-integrity test coupon (§11).
- **Requirements:** HCS-001 to HCS-031, in particular HCS-027 (USB only), HCS-028 (connector contents), HCS-029 (identity, presence and wake over USB), HCS-030 (power follows USB PD), HCS-031 (HAT minimum conditions, Draft), HCS-004 (no cap on high-speed rates), HCS-005 (compromises justified), HCS-006 (one interconnect type), HCS-013 (programmable HAT chips), HCS-021 (hardware-agnostic) and HCS-023 (device-side piece).
- **Decisions:** [ADR 0001](../adr/0001-all-pogo-interface-with-fixed-device-side-piece.md) (all-pogo interface, fixed device-side piece); [ADR 0004](../adr/0004-pogo-part-and-field-geometry.md) (pogo part and pitch, 2.54 mm); [ADR 0007](../adr/0007-pogo-field-kept-for-interface-v2-mill-max-0965-primary.md) (the pogo field for interface v2, Mill-Max 0965 primary, Harwin P70 alternate); [ADR 0006](../adr/0006-hats-are-usb-only.md) (HATs are USB only; this revision). [ADR 0002](../adr/0002-interface-v1-native-high-speed-management-over-usb.md), [ADR 0003](../adr/0003-compatibility-levels.md) and [ADR 0005](../adr/0005-interface-v1-1-shared-extension-and-contact-reduction.md) are superseded by ADR 0006.
- **Data:** the contact list (§4), the contact ratings and margins (§5.1), the power roles (§5.2) and the pogo field (§9.1) are generated from [`interfaces/hat-v2/`](../../interfaces/hat-v2/) (`contacts.toml`, `power.toml`) between `generated` markers with `python3 tools/hat_interface.py render`; edit the data, not the tables. The identity record's fields (§7) have a schema there too (`identity.schema.json`).
- **Conventions:** **UNVERIFIED** = no primary source checked. **EST** = estimate. "Device" is the product the HAT attaches to (the T1 today); "HAT" is the accessory. *Out* = device to HAT, *in* = HAT to device.

## 1. Scope

This document defines the HAT interface: its contacts, their electrical class and position, power, attach and roles, identification, and the conditions every HAT meets. It names no SoC, SoC ball or SoC peripheral instance (HCS-021). A device implements it with whatever silicon it has and documents that mapping in its own repository; for the T1 the mapping is in the [board](https://github.com/opendap-project/board) repository.

The interface has two stages:

1. the **pogo field** on the device-side piece, against flat pads on the HAT (ADR 0001, HCS-014): 20 contacts in a 2 × 10 grid at 2.54 mm (§9.1). This is the interface a HAT designer works with;
2. on the T1, a **flat cable** from the board to the device-side piece (§9.2). It matters to device and device-side piece designers only.

## 2. The interface is one USB port

- **USB only (HCS-027, ADR 0006).** The HAT connector is one USB port: SuperSpeed, its USB 2.0 pair, VBUS, GND and CC. Every HAT function reaches the device through it, with standard USB device classes, or a vendor class whose host side is Open Source. A HAT that needs more carries its own processing behind its USB port.
- **The device is always the USB host** (data role DFP). The HAT is a USB device, a composite device, or a USB hub with devices behind it.
- **One interface, no levels.** There are no compatibility levels, no optional contact groups and no reserved contacts. Every device offers all 20 contacts; a HAT uses what it needs (a USB 2.0-only HAT leaves the SuperSpeed pads unconnected).
- **Growth** comes from USB itself: new classes, descriptors, link generations and PD messages need no new contact. A change to the contact field is a new major revision of this document.

## 3. Relation to v1

v2 replaces the [HAT interface v1](interface-v1.md) (revision v1.1) as a new major revision. What v1.1 carried and how each function reaches the device in v2 are in [ADR 0006](../adr/0006-hats-are-usb-only.md) (Context, Decision and Consequences) and §10.1.

## 4. Contact list

<!-- generated:contact-list:start -->

| Function | Signals (direction) | Pogo contacts | Electrical class | Notes |
|---|---|---|---|---|
| SuperSpeed | `SSTX±` (out), `SSRX±` (in) | 4 (2 pairs) | USB 3 SuperSpeed, 90 Ω differential | TX AC-coupling capacitors on the transmitting side (device for `SSTX`, HAT for `SSRX`) |
| USB 2.0 | `D±` | 2 (1 pair) | USB 2.0, 90 Ω differential | The USB 2.0 half of the same port |
| Configuration channel | `CC` | 1 | USB Type-C CC, USB PD | Required: power follows USB PD (§5). One CC: the field is keyed and never flipped. No VCONN, no SBU (§6) |
| Power | `VBUS` | 4 | 5 V | §5 |
| Ground | `GND` | 9 | — | 4 power returns, 4 pair fence, 1 guard; one net |
| **Total** | | **20** | | |

<!-- generated:contact-list:end -->

**Rates.** The interface sets the lane count and the electrical class, not a rate (HCS-004). The link runs at the highest USB rate both sides and the channel support; the T1's port is USB 3 Gen 1 (5 Gb/s). Rates are measured on hardware at the end.

## 5. Power

Power on the HAT interface follows **USB Power Delivery** (HCS-030, ADR 0006): power roles, current, voltage and charging are what USB Type-C and USB PD negotiate on `CC`, within each side's capability and the contact ratings below. The interface adds no power scheme of its own.

### 5.1 Contact ratings

<!-- generated:power-ratings:start -->

| Rail | Voltage | Direction | Interface rating (continuous) | Interface fault ceiling | Pogo contacts | DF40 contacts (T1) |
|---|---|---|---|---|---|---|
| `VBUS` | vSafe5V by default; a USB PD Standard Power Range voltage after a contract | out to a sink HAT, in from a source HAT | 3.0 A either direction, at any negotiated voltage | 4.5 A | 4 | 15 |
| `GND` (power return) | — | return | 3.0 A | 4.5 A | 4 (+ 5 fence and guard) | 15 (+ 5 pair grounds) |

<!-- generated:power-ratings:end -->

- **3.0 A** is the highest current USB defines without an electronically marked cable (USB Type-C Current 3.0 A; USB PD up to 3 A), so a contract never needs more than the contacts carry. USB PD Extended Power Range is not part of v2.
- **Voltage:** every side starts at vSafe5V; a higher Standard Power Range voltage applies only after both sides agree it in a PD contract. The contacts and the device-side protection are rated for the highest voltage the device sources or accepts; neither pogo part's data gives a voltage rating (**UNVERIFIED** above 5 V).
- **Margin rule (board BRD-049):** each contact at or below 70 % of its rating in continuous use, and at or below 100 % at the fault ceiling, also with one contact open. Count rule: the fewest contacts at ≤ 70 % plus one for redundancy.

<!-- generated:power-margins:start -->

| Contact | Rating | Rail | Continuous per contact | With one contact open | At the fault ceiling | Ceiling, one contact open |
|---|---|---|---|---|---|---|
| Pogo (Mill-Max 0965 or Harwin P70-1000045R) | 2 A (both parts) | `VBUS` ×4, return ×4 | 0.75 A (38 %) | 1.00 A (50 %) | 1.13 A (56 %) | 1.50 A (75 %) |
| DF40 (Hirose catalog 2020, p. 2) | 0.3 A | `VBUS` ×15, `GND` ×15 | 0.20 A (67 %) | — | 0.30 A (100 %) | — |

<!-- generated:power-margins:end -->

### 5.2 Power roles and levels (HCS-030)

<!-- generated:power-roles:start -->

| HAT role | What it does | Negotiation |
|---|---|---|
| **Sink** | Draws power from the device | Type-C current (Default, 1.5 A, 3.0 A at 5 V) or a PD contract the device offers |
| **Source** | Powers or charges the device (for example a powerbank) | The HAT offers its PD source capabilities; the device takes a contract within its input capability |
| **Dual-role** | Either, as agreed (for example a HAT with its own battery) | PD power role swap |

<!-- generated:power-roles:end -->

- **Levels** are those USB defines: without PD, USB default (USB 3.x: 150 mA unconfigured, 900 mA configured; USB 2.0 only: 100 / 500 mA) and Type-C Current 1.5 A and 3.0 A at 5 V; with PD, any Standard Power Range contract up to 3.0 A. BC 1.2 is not part of the interface.
- A device offers on `CC` only what it can supply at that moment, and accepts only what its input path is rated for. A HAT never draws more than its contract. A HAT that needs more than a device offers declares its need in its identity record (§7), and Blackbird OS says clearly what it cannot power (T1-045: never silent).
- **The T1** sources 5 V at Default and 1.5 A (1.5 A while its main USB-C is not sourcing power: the two share one 5 V budget, board power tree §4.6), and sinks from a source HAT within its input path (board power tree §4.6–§4.7). It does not source 3.0 A or voltages above 5 V. **It accepts 5 V only from a HAT** (board decision, 2026-10-25, RFC 0015): its sink capabilities on the HAT port list vSafe5V alone, because its HAT `VBUS` input path is rated for 5 V: the `VBUS` TVS has a 5 V stand-off and 7.5 V minimum breakdown, the port controller's `CC` pins a 6.0 V absolute maximum, and the input mux turns the HAT input off above 5.60–6.31 V (board BOM v1, lines 41, 45, 65). A source HAT offering higher PD voltages still charges the T1 at 5 V, up to 3.0 A within the T1's input limit.

### 5.3 Duties

- **Device:** USB PD on the HAT port (Type-C port controller and policy engine), dual-role power, always USB host (§6.3). VBUS stays at vSafe0V until a HAT is attached (§6.1). The device limits VBUS out with a current limiter whose minimum trip covers the current it offers and whose maximum trip, tolerance included, stays inside the 4.5 A fault ceiling, and limits VBUS in from a source HAT the same way. It discharges VBUS on detach. It never sources VBUS while a HAT supplies it (a hardware interlock, not a software order). Its VBUS and `CC` protection is rated for the highest voltage it sources or accepts.
- **HAT:** a sink HAT presents Rd on `CC` and draws within its contract. Its VBUS input capacitance follows USB (at most 10 µF at attach; more only behind a soft start). Lower rails are regulated on the HAT.

## 6. Attach, roles and wake

### 6.1 Attach sequence

1. **No HAT:** the device presents Rp (or toggles as a dual-role port) on CC; VBUS is at vSafe0V, so the exposed field carries no power.
2. **Attach:** a sink HAT's Rd appears on CC. After the Type-C attach debounce (tCCDebounce), all contacts are mated; the device applies vSafe5V within its Type-C current offer. A PD contract (another current, voltage or power role) may follow.
3. **Enumeration:** the HAT's USB devices enumerate on the device's HAT port.
4. **Identity:** Blackbird OS reads the identity capability (§7), verifies the signed record and manifest, and loads the HAT's software.
5. **Detach:** CC opens; the device removes VBUS and discharges it to vSafe0V; USB sees the disconnect.

### 6.2 CC

- One `CC` contact, required on every device and every HAT: the interface's power follows USB PD (§5).
- A sink HAT whose needs fit Type-C current at 5 V may present Rd alone (5.1 kΩ to `GND`); every other HAT, and every source or dual-role HAT, runs USB PD on `CC`. A device always runs USB PD on its HAT port.
- No VCONN: the interface has no cable and no e-marker. No second CC: the field is keyed (ADR 0001) and never flipped.

### 6.3 Roles

- **The device stays USB host** (data role DFP) in every power role. After attach, power and data roles are set with PD (power role swap from a dual-role attach, or data role swap), so a source HAT's USB functions enumerate on the device as on any other HAT. A source HAT without PD could power the device but would have no USB data on it, so source and dual-role HATs support PD.
- Battery status of a source or dual-role HAT is available over PD (Battery_Capabilities, Battery_Status) before and without USB enumeration; a HAT may also present a USB HID power device.
- A device that can be powered from a HAT presents Rd when its own battery is flat (dead-battery behaviour), so a source HAT can charge it.

### 6.4 Wake and events

- **Wake:** a HAT wakes the device with USB remote wakeup. A device also wakes on a CC attach or detach.
- **Events:** a HAT reports events through USB interrupt endpoints of its functions (for example HID).
- **T1:** remote wakeup from the T1's deep suspend is **UNVERIFIED** (§11).

## 7. Identification

A HAT is whatever enumerates behind the device's HAT port. It identifies itself through its USB descriptors (HCS-029), with no registry of vendor IDs (HCS-008):

- **Identity capability.** At least one USB device on the HAT carries an **OpenDAP HAT identity** BOS Platform Capability descriptor (bDevCapabilityType `0x05`, PLATFORM), identified by a UUID that this document assigns at freeze. Its data carries the capability version, a vendor request code and the identity record length. The device carrying it reports bcdUSB ≥ 0x0201 so its BOS descriptor is read.
- **Identity record.** A vendor control request (device-to-host, vendor type, the request code from the capability) returns the **OpenDAP HAT identity record** (HCS-017 successor, Draft): the HAT's reverse-domain ID, the interface revision (`2`), the power role and the power it needs (§5.2), the hash of its capability manifest and an Ed25519 signature over the record. Blackbird OS verifies it before it loads the HAT's software (HCS-010).
- **Capability manifest** (HCS-009, HCS-011): the record points to the manifest by hash; the manifest is resolved through the Blackbird OS package mechanism, or read from the HAT with the same vendor request. It lists the HAT's USB functions (VID/PID, classes), its power needs and its software.
- **Which device carries it:** any device on the HAT whose descriptors the maker controls: the HAT's MCU, or a hub or bridge whose descriptors can be customised. The pattern is the one other BOS platform capabilities use (for example WebUSB).
- USB VID/PID values are those of the parts the HAT uses or the maker's own; OpenDAP does not allocate them.

The byte layout of the capability and the record, the UUID and the vendor request indexes are open (§11).

## 8. HAT minimum conditions (HCS-031, Draft)

Every HAT meets these conditions:

1. **USB only.** Every function reaches the device through the HAT's USB port, with standard USB device classes that have mainline Linux drivers, or a vendor class whose host side is Open Source.
2. **Own processing.** A HAT carries whatever turns its function into a USB function: an ISP or encoder for a camera (UVC), a UAS bridge for storage, a NIC for networking (CDC ECM/NCM or a mainline NIC driver), a USB Audio controller for audio, an MCU or FPGA for instruments.
3. **One port, a hub when needed.** A HAT with one function connects it directly; several functions are one composite device or sit behind a standard USB hub (USB hub class). A SuperSpeed function and USB 2.0 functions together use a USB 3 hub.
4. **Identity** as in §7, on at least one of its USB devices.
5. **Power** as in §5: Rd on `CC` (or USB PD), a draw within its contract, USB input capacitance rules; a source or dual-role HAT supports USB PD.
6. **Recoverable firmware.** Every programmable chip on the HAT can be reflashed over USB with no working application firmware: a ROM USB bootloader, or a DFU bootloader that an application update cannot overwrite. Blackbird OS flashes, operates and debugs it through USB (HCS-013): DFU, the vendor's ROM loader, or a debug probe function on the HAT (CMSIS-DAP) for chips without either.
7. **Remote wakeup** for a HAT that must wake the device.

Common classes:

| Function | USB class | Linux (mainline) |
|---|---|---|
| Storage | Mass Storage (UAS, BOT) | `uas`, `usb-storage` |
| Video in | UVC | `uvcvideo` |
| Audio, MIDI | USB Audio Class 2 (asynchronous), USB MIDI | `snd-usb-audio` |
| Networking | CDC ECM, CDC NCM | `cdc_ether`, `cdc_ncm` |
| Serial | CDC-ACM | `cdc-acm` |
| Input, sensors, battery | HID | `usbhid`, `hid-sensor-hub` |
| GPIO, I2C, SPI, ADC | DLN2 | `dln2` (MFD) |
| Instruments | USBTMC | `usbtmc` |
| Display | GUD | `gud` |
| Firmware update | DFU | user space (`dfu-util`) |
| Debug probe | CMSIS-DAP | user space (OpenOCD, probe-rs) |

## 9. Contact positions

### 9.1 Pogo field (20 contacts, 2 × 10 at 2.54 mm)

Positions are given looking at the pogo tips on the device-side piece: row A nearest the flat-cable tail, row B beside it; columns 1 to 10. The HAT pad map is the mirror image of this table. Every position uses the same pogo part (HCS-006), at **2.54 mm**: the **Mill-Max 0965** (primary) or the **Harwin P70** (alternate) on the same HAT pads (ADR 0004 and its amendment). Contact span 22.86 × 2.54 mm. 20 is the fewest contacts that meet §4 and §5.1; a 2 × 8 field does not hold them (ADR 0004 amendment).

<!-- generated:pogo-field:start -->

| Col | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Row A** | GND | SSTX+ | SSTX− | GND | SSRX+ | SSRX− | GND | D+ | D− | GND |
| **Row B** | VBUS | GND | VBUS | GND | VBUS | GND | VBUS | GND | GND | CC |

<!-- generated:pogo-field:end -->

Layout rules:

- **Pairs along row A**, both contacts of a pair in adjacent columns, a `GND` on each side in the row; adjacent pairs share that ground (G S S G S S G S S G).
- **Next to a pair contact** (in row B) sit only `GND` and `VBUS`. `CC` sits at the corner, between two grounds.
- **Every `VBUS` next to a `GND`.**
- Whether the field needs more grounds is decided by the coupon (§11).

**Spring force** (derived from the part data, ADR 0004 amendment): 20 × 115 gf = **22.6 N** at mid stroke with the 0965 (20 × 30 gf = 5.9 N at first touch); 20 × 0.88 ± 0.29 N = 17.6 N (11.8–23.4 N) with the P70. The HAT retention and the case carry it, preloaded for 23.4 N with margin.

**Pad-plane tolerance rule.** Hard stops on the device-side piece, not the springs, set the HAT pad plane, at the centre of the populated part's working window above the piece's land surface:

| Part | Working window | Hard-stop height | Half window | Allowed pad-plane deviation, RSS |
|---|---|---|---|---|
| Mill-Max 0965 (primary) | 1.93–2.54 mm | 2.24 mm | ±0.30 mm | ≤ 0.20 mm |
| Harwin P70 (alternate) | 2.70–3.00 mm | 2.85 mm | ±0.15 mm | ≤ 0.10 mm |

- The pad-plane deviation is the RSS of every contributor between a pin's land and the HAT pad it meets: the stop height, the pin's seating on its land, the piece's flatness over the field and the HAT's bow over the pad area. **1.5 × the RSS stays within the half window** of the populated part.
- The HAT carries a stiffener under its pad area (HCS-014), so its bow over the field is part of that budget, not of the springs' travel.
- The case drawing sets each contributor and checks the sum (**UNVERIFIED** until it exists).

### 9.2 Flat cable (T1; DF40C-50, 46 usable positions)

One Hirose DF40C-50 pair at each end carries signals and power; it has the locking feature that the 100-position size lacks. The board and the device-side piece carry the DF40C-50DS-0.4V(51) receptacle and the cable the DF40C-50DP-0.4V(51) header at each end (board [HAT flat cable](https://github.com/opendap-project/board/blob/main/docs/specs/hat-flat-cable.md) spec). On the T1 the ESD protection of the field (`VBUS` TVS, SuperSpeed, `D±` and `CC` arrays) sits on the device-side piece next to the field, where a discharge enters; none is repeated on the board side of the cable. Numbering follows the Hirose DF40 drawings: contacts 1, 3, 5 … on row A, 2, 4, 6 … on row B (**UNVERIFIED** against the drawing; confirm before the FPC layout). Contacts 1, 2, 49 and 50 are metal fittings and carry nothing (DF40 catalog 2020, p. 10, note 3). The connector is not polarized (p. 10, note 5): both cable ends are keyed mechanically.

| Row A | Signal | Row B | Signal |
|---|---|---|---|
| 1 | metal fitting | 2 | metal fitting |
| 3–31 (odd) | VBUS (×15) | 4–32 (even) | GND (×15) |
| 33 | GND | 34 | CC |
| 35 | SSTX+ | 36 | spare |
| 37 | SSTX− | 38 | spare |
| 39 | GND | 40 | spare |
| 41 | SSRX+ | 42 | GND |
| 43 | SSRX− | 44 | D+ |
| 45 | GND | 46 | D− |
| 47 | spare | 48 | GND |
| 49 | metal fitting | 50 | metal fitting |

Count: power 30 (`VBUS` 15 facing 15 `GND`) + 3 pairs (6) with 5 pair grounds + `CC` = 42 used; 4 spare (8.7 %). Power conductors are sized for 3.0 A continuous and 4.5 A fault (board BOM line 102).

## 10. Reference HATs on v2

Expected architecture. The reference HATs' requirements name the HAT type only; the architecture below is engineering judgement, not a requirement.

| HAT | What it carries over USB | Link use (EST) |
|---|---|---|
| Camera (CAM-005) | UVC from an ISP bridge (sensor → ISP → UVC over SuperSpeed), or a camera SoC with its own encoder (UVC 1.5 or bulk); a microphone as UAC2 in the same composite device; DFU | 4K30 NV12 2.99 Gb/s of ≈ 3.2 Gb/s; H.265 ≈ 80 Mb/s |
| NAS (NAS-005, NAS-006) | A USB 3 hub with a UAS NVMe bridge and a 2.5GbE NIC; fan and sensors on an MCU (HID or DLN2) | 2.35 Gb/s per 2.5GbE port of ≈ 3.2 Gb/s per direction |
| Radio (RAD-005) | The radio's native High-Speed USB 2.0 stream on `D±`; any SuperSpeed function behind a USB 3 hub | 320 Mb/s (20 Msps × 2 × 8 bit) |
| Oscilloscope (OSC-005) | High-Speed bulk stream from the HAT's MCU or FPGA; DFU | ≤ 160 Mb/s |
| VNA (VNA-005) | CDC-ACM at full speed; DFU | < 1 Mb/s |
| Recorder (REC-005) | UAC2 asynchronous capture, up to 8 channels at 192 kHz, 32 bit; the HAT's clock is master; monitoring on the HAT's own output | 49 Mb/s |
| USB-C port ([RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md); [reference designs](../../reference-designs/README.md)) | A USB 3 hub with one downstream USB-C receptacle (USB 3 Gen 1 and USB 2.0, reversible) and its own USB PD controller; the identity capability on the hub or a device behind it; a dual-role HAT that powers what is plugged in and passes a charger's power to the device | Shared by what is plugged in, up to the port's ≈ 3.2 Gb/s per direction |
| Powerbank (PWR-005) | Source or dual-role HAT: USB PD source, charging the device within its input capability; battery status over PD; optional HID power device | — |

### 10.1 Compromises (HCS-005)

| Property | v1.1 | v2 |
|---|---|---|
| HAT audio synchronous with the device's playback | I2S on the DAC clock | Each USB audio HAT runs on its own clock (asynchronous, bit-perfect on that clock); playing a HAT input through the device's own outputs needs resampling |
| Native NVMe | PCIe x1 | NVMe behind a UAS bridge: same link rate class (5 Gb/s), lower IOPS (**UNVERIFIED** by how much) |
| Raw camera sensor into the device's ISP | CSI-2, 4 lanes | The HAT carries its ISP or encoder; a 4K30 uncompressed stream uses ≈ 93 % of a USB 3 Gen 1 link |
| Recovery of a bricked HAT chip | SWD from the device | ROM USB loader or protected DFU required on every programmable chip (§8) |
| Signals before USB enumerates | ID EEPROM, presence, interrupt, I2C | CC attach, current advertisement and PD messages only |

## 11. Open points

1. **Signal-integrity coupon** (ADR 0004): USB 3 Gen 1 and USB 2.0 through the 2 × 10 field, the device-side piece and, on the T1, the DF40C-50 and the FPC; whether the field needs more grounds. An estimate puts the bare pin pair (Ø 1.50 mm barrels at 2.54 mm) between 72 Ω and 134 Ω differential depending on the housing dielectric, around the 90 Ω target, and the ≈ 4.5 mm path is electrically short at the 2.5 GHz Nyquist but not at its third harmonic (EST).
2. **Identity format** (HCS-017 successor): capability UUID, byte layout, vendor request indexes, hash algorithm.
3. **Remote wakeup** from each device's deep suspend (T1: **UNVERIFIED**).
4. **Voltage ratings above 5 V** for the pogo parts and the device-side piece (neither part's data gives one).
5. **DF40 contact numbering** (§9.2) against the Hirose drawing.
6. **Conformance suite** (toolkit-verify): CC behaviour, VBUS limits and discharge, identity capability, USB compliance of the field.
7. **HAT pad diameter** and the piece's hard-stop and pad-plane contributors on the case drawing (§9.1).

## 12. Sources

- OpenDAP HAT Standard requirements: [`../requirements/README.md`](../requirements/README.md); ADR [0001](../adr/0001-all-pogo-interface-with-fixed-device-side-piece.md), [0004](../adr/0004-pogo-part-and-field-geometry.md), [0006](../adr/0006-hats-are-usb-only.md).
- [HAT interface v1](interface-v1.md) (superseded, revision v1.1).
- USB 3.2, USB 2.0, USB Type-C Cable and Connector, and USB Power Delivery specifications (USB-IF): current advertisement (Default, 1.5 A, 3.0 A), vSafe0V and vSafe5V, attach debounce, power and data role swaps, BOS descriptors and the PLATFORM capability type.
- Board repository: [BOM v1](https://github.com/opendap-project/board/blob/main/docs/specs/bom-v1.md), [power tree v0](https://github.com/opendap-project/board/blob/main/docs/specs/power-tree-v0.md) (§4.6, §4.7).
- Parts library: Harwin P70-1000045R (2.0 A, 0.88 N ± 0.29 N, Ø 2.20 mm pad, Ø 1.50 mm barrel), Hirose DF40C-50 (0.3 A per contact, corner metal fittings, lock).
- Mill-Max 0965-0-15-20-80-14-11-0 product data (2 A, working height 1.93–2.54 mm, 30 / 115 gf, 1,000,000 cycles, Ø 1.83 mm land), read 2026-10-22.
- [RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md) (HAT connector and the USB-C port HAT).
