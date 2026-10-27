# ADR 0007: Pogo field kept for interface v2; Mill-Max 0965 primary

- **Status:** Accepted
- **Date:** 2026-10-25
- **Basis:** [RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md); safe power (BRD-049)
- **Amends:** [ADR 0004](0004-pogo-part-and-field-geometry.md) (primary part, field size); **reaffirms:** [ADR 0001](0001-all-pogo-interface-with-fixed-device-side-piece.md) for interface v2

## Context

[RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md) confirms the pogo field of [ADR 0001](0001-all-pogo-interface-with-fixed-device-side-piece.md) for interface v2 and changes which part is primary.

## Facts

| Part | Rating | Working height | Force | Durability | Device-side land |
|---|---|---|---|---|---|
| Mill-Max 0965-0-15-20-80-14-11-0 | 2 A | 1.93–2.54 mm, recommended 2.24 mm | 30 gf initial, 115 gf at mid stroke | 1,000,000 cycles | Ø 1.83 mm |
| Harwin P70-1000045R | 2.0 A, 30 mΩ maximum | 2.70–3.00 mm, normal 2.90 mm | 0.88 ± 0.29 N at 2.90 mm | 10,000 cycles | Ø 2.20 ± 0.05 mm |

Sources: Mill-Max product data for 0965-0-15-20-80-14-11-0 (read 2026-10-22); Harwin drawing P70-10X0045R, issue 4.

## Decision

**The pogo field stays the HAT connector of interface v2** (USB only, [ADR 0006](0006-hats-are-usb-only.md)); a USB-C receptacle in the device-side piece is not adopted. A USB-C port is offered as a reference HAT instead (the USB-C port HAT, [reference designs](../../reference-designs/README.md)).

1. **Primary: Mill-Max 0965**; **alternate: Harwin P70**. The device-side piece carries every swap of every HAT, so it takes the part rated for 1,000,000 cycles, and the 0965's 0.61 mm working window is twice the P70's 0.30 mm against the pad-plane tolerance (interface v2 §9.1).
2. **The HAT pads are common** to both parts; a HAT does not depend on which part the piece carries. Pad finish and stiffener as in ADR 0004.
3. **The device-side piece is built for one part.** Its land follows the part, and its hard stops set the HAT pad plane at the centre of that part's working window above the piece's land surface: **2.24 mm for the 0965** and **2.85 mm for the P70** (not its 2.90 mm normal height, which leaves 0.10 mm above it). The pad-plane tolerance rule is in interface v2 §9.1.
4. **Field: 2 × 10 = 20** (ADR 0006). 20 is the fewest contacts that meet interface v2 §4 and §5.1: three pairs (6), `CC` (1), `VBUS` ×4 and four returns at 3.0 A (BRD-049 count rule), four pair-fence grounds and one guard ground. A 2 × 8 field does not hold them.
5. **Spring force** of the 20-contact field: 22.6 N at mid stroke with the 0965 (5.9 N at first touch), 17.6 N (11.8–23.4 N) with the P70. The HAT retention is preloaded for **23.4 N**, the higher maximum of the two, with margin (case).

## Consequences

BOM line 67 of the board lists 20 × 0965 with the P70 as the alternate; the case sets the hard-stop datums and the retention preload; the signal-integrity coupon (above) runs with the 0965 first.
