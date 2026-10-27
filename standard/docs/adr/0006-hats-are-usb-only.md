# ADR 0006: HATs are USB only

- **Status:** Accepted
- **Date:** 2026-10-25
- **Basis:** the maintainers' decisions of 2026-10-25: HATs are USB only; charging and voltage management follow the USB Power Delivery standard, so `CC` is part of the connector
- **Supersedes:** [ADR 0002](0002-interface-v1-native-high-speed-management-over-usb.md), [ADR 0003](0003-compatibility-levels.md), [ADR 0005](0005-interface-v1-1-shared-extension-and-contact-reduction.md). **Amends:** [ADR 0004](0004-pogo-part-and-field-geometry.md) (field size; part, second source and pitch stand).
- **Specification:** [HAT interface v2](../specs/interface-v2.md) (Draft)

## Context

Interface v1.1 used 68 pogo contacts in three levels: USB 3 with its USB 2.0 pair, a PCIe or CSI-2 extension behind two switches on the T1, an I2S port on the device's DAC clock, four GPIO with SWD, reset, a general I2C, an ID EEPROM bus, presence, interrupt and eight reserved contacts.

Facts checked against each reference HAT (CAM-005, NAS-005/006, RAD-005, OSC-005, VNA-005, REC-005, PWR-005):

- Each one reaches its function over one USB 3 Gen 1 port with its USB 2.0 pair when the HAT carries its own processing: a camera at 4K30 NV12 uses 2.99 Gb/s of about 3.2 Gb/s practical (UVC), or about 80 Mb/s with its own encoder (EST); a 2.5GbE port needs 2.35 Gb/s per direction behind a UAS bridge and a NIC; the radio streams 320 Mb/s on High-Speed USB 2.0; 8 channels at 192 kHz and 32 bit are 49 Mb/s (USB Audio Class 2, asynchronous).
- USB 3 Gen 1 and PCIe Gen 2 x1 both carry 4 Gb/s after 8b/10b coding.
- Every function v1.1 carried on native lines has a USB form: UVC, Mass Storage (UAS), CDC ECM/NCM, USB Audio Class 2, HID, DLN2 (GPIO, I2C, SPI, ADC), DFU, CMSIS-DAP; identity in BOS descriptors; presence as USB Type-C attach; wake as USB remote wakeup.
- Without `CC`, a USB device cannot be detected before VBUS is applied, so the exposed field would carry 5 V with no HAT, and two power sources could meet on VBUS. With `CC`, VBUS stays at vSafe0V until a sink attaches, and USB PD negotiates current, voltage and power roles.

## Decision

1. **HATs are USB only.** Every HAT capability goes through USB, with standard USB device classes or a vendor class whose host side is Open Source. A HAT that needs more carries its own processing behind its USB port. The device is always the USB host.
2. **The HAT connector carries only what USB defines:** `SSTX±`, `SSRX±`, `D±`, `VBUS`, `GND` and `CC`. `VBUS` and `GND` are repeated only as current and signal integrity require. No PCIe, CSI-2, I2S, master clock, GPIO, SWD, reset, I2C, ID, presence or interrupt lines, no reserved contacts and no compatibility levels.
3. **Power follows USB Power Delivery.** `CC` is required. Power roles (sink, source, dual-role), current, voltage and charging are what USB Type-C and USB PD negotiate, within each side's capability and the contact ratings. The interface rating is 3.0 A on `VBUS` in either direction, the most USB defines without an electronically marked cable; Extended Power Range is not part of v2. The device stays USB host in every power role.
4. **Identity** is carried in USB descriptors: an OpenDAP HAT identity BOS Platform Capability on at least one of the HAT's USB devices, leading to a signed identity record and the capability manifest (HCS-009, HCS-010). There is no ID EEPROM. **Presence** is attach on `CC`. **Wake** is USB remote wakeup, and attach or detach on `CC`.
5. **Firmware recovery** is over USB: every programmable chip on a HAT has a ROM USB bootloader or a DFU bootloader that an application update cannot overwrite (HCS-013).
6. **Pogo field: 2 × 10 = 20 contacts at 2.54 mm** with the ADR 0004 part (Harwin P70, Mill-Max 0965 second source): the three pairs along one row, fenced by grounds (G S S G S S G S S G); `VBUS` ×4 and its returns in the other row; `CC` at the corner between grounds. `VBUS` ×4 and return ×4 follow the BRD-049 count rule at 3.0 A on a 2.0 A contact (38 % continuous, 50 % with one contact open, 75 % at the 4.5 A fault ceiling with one open).
7. **Interface v2** (Draft) replaces v1.1; v1 is kept as history. It is a new major revision: v1 and v2 HATs and devices do not mate.

## Consequences

| | v1.1 | v2 |
|---|---|---|
| Pogo contacts | 68 (L1 29) | **20** |
| High-speed pairs | 8 | 3 |
| Native low-speed signals | 22 | 1 (`CC`) |
| Reserved | 8 | 0 |
| Field span | 40.64 × 7.62 mm | 22.86 × 2.54 mm |
| Spring force, P70 | ≈ 60 N | ≈ 18 N |
| Flat cable on the T1 | DF40C-100, 87 of 96 used | DF40C-50, 42 of 46 used |
| ESD on the device-side piece (T1) | 12 parts | 2 parts |

- **Every reference HAT works** with its processing on the HAT: the camera carries an ISP or an encoder, the NAS a USB 3 hub, a UAS bridge and a NIC, the recorder a USB Audio controller, the powerbank a USB PD source.
- **Compromises (HCS-005):** HAT audio runs on the HAT's own clock, bit-perfect on that clock, and is no longer sample-synchronous with the device's playback; NVMe behind UAS has lower IOPS than native PCIe (**UNVERIFIED** by how much); a 4K30 uncompressed camera stream uses about 93 % of a USB 3 Gen 1 link; recovery needs a USB bootloader on every HAT chip instead of SWD from the device; before enumeration only `CC` and PD messages are available.
- On the T1, the SoC's PCIe and CSI-2 receivers have no HAT consumer; the board records what follows (RFC 0014).
- Requirements: HCS-007, HCS-015, HCS-017, HCS-022, HCS-025 and HCS-026 are withdrawn; HCS-027 to HCS-031 are added.
- **Signal integrity stays UNVERIFIED** until the ADR 0004 coupon qualifies USB 3 Gen 1 and USB 2.0 through the 2 × 10 field.
- Cross-repository changes (board, every HAT repository): [RFC 0014](https://github.com/opendap-project/rfcs/blob/main/text/0014-hat-interface-v2-usb-only.md).
