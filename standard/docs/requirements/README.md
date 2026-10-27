# HAT Case Standard requirements

Requirements for the HAT Case Standard.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| HCS-001 | The standard shall cover both sides of the HAT Case: the device (T1) side and the accessory side. | must | Confirmed |
| HCS-002 | The standard shall be usable by third-party accessory developers. | must | Confirmed |
| HCS-003 | A HAT shall replace the basic back cover of the core with a HAT case. | must | Confirmed |
| HCS-004 | Each exposed high-speed interface (PCIe, USB, camera, …) shall target the theoretical maximum the hardware and software can deliver, with no cap set up front. Actual speeds are measured at the end. | must | Confirmed |
| HCS-005 | Any compromise on the exposed ports shall be fully justified. | must | Confirmed |
| HCS-006 | The HAT interface shall use a single interconnect type for every signal: either all pogo pins or all connectors, ideally of the same part. | must | Confirmed |
| HCS-007 | A HAT shall identify itself through an on-board EEPROM. | must | Withdrawn (identity is carried in USB descriptors, HCS-029) |
| HCS-008 | There shall be no central registry of manufacturer or vendor IDs. | must | Confirmed |
| HCS-009 | The EEPROM shall carry a capability manifest in a standard schema. | must | Confirmed |
| HCS-010 | The capability manifest shall be signed, and Blackbird OS shall verify it. | must | Confirmed |
| HCS-011 | The capability manifest shall work with the Blackbird OS package repository mechanism (reverse-domain, well-known HTTP, through the package endpoint). | must | Confirmed |
| HCS-012 | The device-side piece shall be fixed to the T1; only the HAT is swapped. | must | Confirmed |
| HCS-013 | The standard shall support HATs carrying microcontrollers, FPGAs or another SoC, which Blackbird OS can flash, operate and debug. | must | Confirmed |
| HCS-014 | HATs shall be passive at the interface: flat contact pads on the HAT, springs only on the device side. | must | Draft |
| HCS-015 | Power classes: A and B (the HAT draws power) and F (the HAT is a power source). | must | Withdrawn (power roles and levels follow USB PD, HCS-030) |
| HCS-016 | Power-up sequence: presence detect → 3.3 V → read EEPROM → apply overlay → 5 V → switches and high-speed links. | must | Withdrawn |
| HCS-017 | The EEPROM shall use the OpenDAP HAT identity format: reverse-domain ID, power class, Ed25519 signature and the hash of the capability manifest. | must | Withdrawn (no EEPROM; the identity record is read over USB, HCS-029) |
| HCS-018 | The device-side piece shall be fixed with four M2 screws, and a spring-loaded steel slider lock shall hold the HAT, released by a button on the right edge. | should | Withdrawn |
| HCS-019 | The lock may use a metal part, as the exception to polymer-first cases. | should | Confirmed |
| HCS-020 | The device-side piece of the HAT case shall be screwed to the T1. | must | Confirmed |
| HCS-021 | The standard shall be hardware-agnostic on both sides: it shall not depend on the board or SoC behind the device side, nor on the HAT's hardware, and shall stay valid if the device's board changes completely. Signals are defined by function and interface class, never by a specific SoC pin. | must | Confirmed |
| HCS-022 | The interface shall keep a few reserved contacts for future revisions, without displacing essential signals to get them. | must | Withdrawn (no reserved contacts; growth comes through USB, HCS-028) |
| HCS-023 | The device-side piece (pogo field and its flat cable) shall be an independent accessory of the HAT standard, fitted to the T1 by the user or at assembly and then fixed to it (HCS-012, HCS-020). A T1 without it works fully, and the back cover closes it. | must | Confirmed |
| HCS-024 | The HAT standard is OpenDAP's own. It takes inspiration from established standards (Raspberry Pi HAT+ and others) and should support them where that costs little, for example by keeping the identity layout compatible with HAT+ so existing tools can read it. | should | Confirmed |
| HCS-025 | The standard shall define compatibility levels (L1 Core, L2 Control and audio, L3 High-speed extension): devices declare the level they implement, HATs the level they need, and a HAT works on any device of its level or higher (ADR 0003, ADR 0005). | must | Withdrawn (no compatibility levels, HCS-028) |
| HCS-026 | USB 3 shall be the base of the HAT interface (L1). The high-speed extension shall carry PCIe or MIPI CSI-2 (camera in) on the same reused contacts, selected by the function the HAT declares in its identity record, not both side by side. | must | Withdrawn (no PCIe or CSI-2 extension; USB only, HCS-027) |
| HCS-027 | Every HAT capability shall go through USB, using standard USB device classes or a vendor class whose host side is Open Source. A HAT that needs more shall carry its own processing behind its USB port. | must | Confirmed |
| HCS-028 | The HAT connector shall carry only what USB defines: SuperSpeed TX and RX, the USB 2.0 pair, VBUS and GND (repeated only as current and signal integrity require), and CC. No other signal, no reserved contacts and no compatibility levels. | must | Confirmed |
| HCS-029 | A HAT shall identify itself through its USB descriptors, which lead to its signed capability manifest. Presence shall be USB attach, and wake shall be USB remote wakeup. | must | Confirmed |
| HCS-030 | Charging and voltage management on the HAT interface shall follow USB Power Delivery: power roles (sink, source, dual-role), current and voltage are negotiated on CC, within each side's capability and the BRD-049 margins. | must | Confirmed |
| HCS-031 | Every HAT shall meet the minimum conditions of the HAT interface: standard USB classes, its own processing, the identity capability, the USB power rules, and firmware that can be recovered over USB with no working application firmware. | must | Draft |
| HCS-032 | The standard shall include a blank HAT case: a HAT case with no HAT hardware that closes the back of a T1 fitted with the device-side piece when no HAT is attached. It is separate from the hardware HATs. | must | Confirmed |

## Open questions

- The [HAT interface v2](../specs/interface-v2.md) (Draft, [ADR 0006](../adr/0006-hats-are-usb-only.md)) defines 20 contacts on a 2 × 10 pogo field. The pad map freezes after the signal-integrity coupon (ADR 0004). Open: the identity capability's UUID and byte layout, voltage ratings above 5 V for the pogo part, remote wakeup from each device's suspend, and the conformance suite.
- Mechanical details of the device-side piece and the HAT case.

## Context

- HCS-017 and HCS-024: the standard is OpenDAP's own; compatibility with Raspberry Pi HAT+ and other standards is a *should*, not a constraint.
- HCS-022 is must: contacts cannot be added once third parties build HATs.
- The connection from the board to a HAT has two stages: a flat cable from the board to the device-side piece of the HAT case, then from that piece to the HAT hardware.
- The second stage is all pogo pins ([ADR 0001](../adr/0001-all-pogo-interface-with-fixed-device-side-piece.md)). An early estimate was about 120–128 contacts; two rows would be about 81 mm long, more than the device width, so the first proposal was a 4 × 32 grid at 1.27 mm (about 41 × 4 mm). Note: superseded. Interface v1 reduced the count, the ADR 0002 amendment set a 4 × 25 = 100 field, and [ADR 0004](../adr/0004-pogo-part-and-field-geometry.md) fixes it at 2.54 mm along the body's length with Harwin P70 springs and Mill-Max 0965 as the second source; the pinout is in [interface v1](../specs/interface-v1.md). Note (ADR 0005): the field is now 4 × 17 = 68 at 2.54 mm.
- HCS-026: contacts were already reduced through the compatibility levels and pin reuse, yet the design still used too many in places; the base is USB 3, and the extension is PCIe or CSI-2 on the same reused high-speed contacts, selected by declared function (DSI out is not part of it). They also clarified board BRD-042: a standard high-speed switch is acceptable if it does not limit the link and uses standard parts and protocols. Result: [ADR 0005](../adr/0005-interface-v1-1-shared-extension-and-contact-reduction.md): 100 → 68 pogo contacts (L1 29, L2 45, L3 68 cumulative), one DF40 100 per cable end instead of a 100 and a 50, line out removed, SWD as a GPIO alternate.
- HCS-007 requires an on-board EEPROM; the dedicated ID bus comes from ADR 0002 item 2. ADR 0005 keeps it: moving the EEPROM onto the general I2C would save two contacts but make the identity read, which gates `HAT_5V`, depend on every third-party device on that bus.
- The flat cable from the board to the device-side piece is specified by the `board` repository.
- The device-side piece goes wherever it fits best inside the T1. The HAT Case Standard is defined once the rest of the device is settled.
- HCS-027 to HCS-030: HATs are USB only; the connector carries only what USB defines, with identity in USB descriptors, presence as attach and wake as remote wakeup; charging and voltage management follow USB Power Delivery, so CC is part of the connector. Result: [ADR 0006](../adr/0006-hats-are-usb-only.md) and [interface v2](../specs/interface-v2.md): 68 → 20 pogo contacts. Withdrawn the same day: HCS-007, HCS-015, HCS-017, HCS-022, HCS-025, HCS-026. HCS-013 stands: HAT chips are flashed, operated and debugged over USB. HCS-024 stands; its example (an identity layout readable by HAT+ tools) no longer applies, as there is no EEPROM. HCS-031 (Draft) records the minimum conditions of interface v2 §8.
- HCS-006, HCS-014 ([RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md)): the pogo field stays the HAT connector of interface v2 ([ADR 0001](../adr/0001-all-pogo-interface-with-fixed-device-side-piece.md) confirmed); the Mill-Max 0965 becomes the primary pogo part and the Harwin P70 the alternate ([ADR 0004](../adr/0004-pogo-part-and-field-geometry.md) amendment). A USB-C port is offered as a reference HAT, the USB-C port HAT ([reference designs](../../reference-designs/README.md)), also the prototyping path for HAT makers (HCS-002).
- HCS-032: three back closures exist: the basic back cover (no device-side piece, HCS-023), the blank HAT case (device-side piece fitted, no HAT) and a hardware HAT in its HAT case (HCS-003).
