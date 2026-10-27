# ADR 0001: All-pogo interface with a fixed device-side piece

- **Status:** Accepted
- **Date:** 2026-10-21
- **Reaffirmed by:** [ADR 0007](0007-pogo-field-kept-for-interface-v2-mill-max-0965-primary.md) (2026-10-25, interface v2)

## Context

The HAT interface must use a single interconnect type for every signal (HCS-006), be easy for third-party manufacturers (HCS-002) and target the maximum each high-speed interface allows (HCS-004).

## Decision

- Every signal of the HAT interface goes through **pogo pins**: power, analog, low-speed and high-speed.
- The pogo pins sit on the **device-side piece, which is fixed to the T1**. Only the HAT is swapped.
- The HAT side carries flat contact pads.
